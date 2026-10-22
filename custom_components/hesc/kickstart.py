"""Home battery <-> EV (kickstart).

Line-by-line port of v2.0.0's Node-RED function node "Home battery and EV (kickstart)" (every
input round). While the home batteries charge, a charger in solar mode sees no surplus and never
starts: (1) kickstart: start the charger once the sun left today is clearly more than the home
batteries still need; as soon as the home battery control sees the EV: pause, and once the pause has
arrived, back to solar mode (v3, practice test 15-10-2026; v2 handed back without a pause); (2) when the EV charges
on sun and the sun left today is only just enough for the home batteries: pause, then back to
solar mode. In shadow mode it only writes what it would do. Proven identical to the original node
on random runs (`tests/integration/test_kickstart_parity.py`).
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .inputs import js_parse_float
from .jscompat import (
    UNDEFINED,
    iso,
    js_json,
    js_number_str,
    js_round,
    js_to_fixed,
    local_date,
    local_hhmm,
)
from .price_forecast import date_parse

_BINARY = re.compile(r"^(binary_sensor|switch|input_boolean)\.")
BAD = ("unknown", "unavailable", "none", "")
MARGIN = 3
# Kickstart hand-back (v3, practice test 15-10-2026): pause at least PAUSE_MIN, the charger's start/stop
# switch off for PAUSE_SETTLE, at most PAUSE_MAX; press "back to solar" again once after RESUME_RETRY_S.
PAUSE_MIN, PAUSE_SETTLE, PAUSE_MAX = 30000, 15000, 180000
RESUME_RETRY_S = 180
# Start command: second try / give up when the charger's power still shows nothing. v2 used 30 s / 120 s, but the
# Wallbox cloud integration showed the charge in HA only after more than 2 minutes (practice test 15-10-2026: app
# "manual charging" at ~11:52, HA at ~11:53, HESC gave up at 11:52:36). Hence 90 s / 240 s; since 3.0.0 the
# give-up is 360 s (practice test 19-10-2026: the charge showed in HA only after ~4 minutes).
START_RETRY_S, START_FAIL_S = 90, 360
STATUS_EVERY = 15 * 60000  # v2.0.1-dev2: numbers-only status changes at most this often


def _s(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return js_number_str(v)
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    return str(v)


def _fx(v: float, n: int) -> float:
    """+v.toFixed(n)"""
    return float(js_to_fixed(v, n))


def _dparse(v: Any) -> float:
    if isinstance(v, datetime):
        return v.timestamp() * 1000
    if v is None or v is UNDEFINED:
        return math.nan
    return date_parse(v if isinstance(v, str) else _s(v))


def _act(action: str, entity: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"payload": {"action": action, "target": {"entity_id": [entity]}, "data": data or {}}}


@dataclass
class Result:
    status: list[dict[str, Any]] = field(default_factory=list)  # out1: HA actions for the status text
    actions: list[dict[str, Any]] = field(default_factory=list)  # out2: charger actions
    history: list[dict[str, Any]] = field(default_factory=list)  # out3: history lines
    flow: dict[str, Any] = field(default_factory=dict)  # hescKick
    node_status: str = ""


def run(S: dict[str, Any], flow: dict[str, Any], now: int) -> Result:
    """One run of the node. flow: hescKick and hescPlan (read only)."""
    def st(i: Any) -> Any:
        return S[i].get("state") if i and i in S else UNDEFINED

    def attr(i: Any, a: str) -> Any:
        if i and i in S and S[i].get("attributes") is not None:
            return S[i]["attributes"].get(a, UNDEFINED)
        return UNDEFINED

    def num(v: Any) -> float | None:
        return js_parse_float(v)

    def on(i: Any) -> bool:
        return st(i) == "on"

    def low(v: Any) -> str:
        return ("" if v is None or v is UNDEFINED else _s(v)).lower().strip()

    def txt(i: Any) -> str:
        v = st(i)
        return "" if (v is UNDEFINED or v is None or v in BAD) else _s(v).strip()

    def lst(v: str) -> list[str]:
        return [x.strip() for x in (v or "").split(",") if x.strip()]

    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    tz = pa.get("tz") or "Europe/Amsterdam"

    def day_key(t: float) -> str:
        return local_date(t, tz)

    def press(ent: str) -> dict[str, Any]:
        return _act("button.press" if ent.startswith("button.") else ent.split(".")[0] + ".turn_on", ent)

    soc_txt = txt("input_text.hesc_ev_soc_sensor")
    C = {
        "on": on("input_boolean.hesc_kick_enabled"),
        "hescOn": st("input_boolean.hesc_enabled") != "off",
        "shadow": st("input_boolean.hesc_shadow_mode") != "off",
        "socIds": lst(txt("input_text.hesc_home_battery_soc_sensors")),
        "pwIds": lst(txt("input_text.hesc_home_battery_power_sensors")),
        "kwh": num(st("input_number.hesc_home_battery_kwh")) or 0,
        "maxDay": num(st("input_number.hesc_kick_max_per_day")) or 3,
        "minEv": num(st("input_number.hesc_kick_min_ev_kwh")) or 2,
        "gap": 30 * 60000,
        "tStable": (num(st("input_number.hesc_t_stable")) or 5) * 60000,
        "startStop": txt("input_text.hesc_charger_start_stop_entity"),
        "solarBack": txt("input_text.hesc_charger_resume_entity"),
        "modeEnt": txt("input_text.hesc_charger_mode_entity"),
        "ecoVals": [low(x) for x in lst(txt("input_text.hesc_charger_eco_value") or "eco_mode")],
        "evConn": txt("input_text.hesc_ev_connected_sensor"),
        "offVals": [low(x) for x in lst(txt("input_text.hesc_ev_disconnected_values") or "off,disconnected,ready,available,unplugged")],
        "evSoc": "sensor.hesc_ev_soc" if (soc_txt and num((S.get("sensor.hesc_ev_soc") or {}).get("state")) is not None) else soc_txt,
        "fullSoc": num(st("input_number.hesc_ev_full_soc")) or 80,
        "fcNow": txt("input_text.hesc_forecast_now_sensor"),
        "fcAttr": txt("input_text.hesc_forecast_attribute"),
        "today": txt("input_text.hesc_solar_today_sensor"),
        "pStart": num(st("input_number.hesc_p_start")) or 2000,
        "hbcEv": txt("input_text.house_battery_strategy_ev_sensor_entity_id"),
    }
    sw_dom = C["startStop"].split(".")[0] if C["startStop"] else ""
    can_act = bool(C["startStop"]) and not C["startStop"].startswith("button.") and bool(C["solarBack"])

    # EV
    if _BINARY.match(C["evConn"]):
        ev_conn = on(C["evConn"])
    else:
        sv = st(C["evConn"])
        ev_conn = bool(C["evConn"]) and not (sv is UNDEFINED or sv is None or sv in BAD) and low(sv) not in C["offVals"]
    soc = num(st(C["evSoc"])) if C["evSoc"] else None
    pw_id = txt("input_text.hesc_ev_power_sensor")
    pw_raw = num(st(pw_id))
    ev_pow = None if pw_raw is None else (pw_raw * 1000 if low(attr(pw_id, "unit_of_measurement")) == "kw" else pw_raw)
    ev_charging = ev_pow is not None and ev_pow > (num(st("input_number.hesc_ev_active_w")) or 400)
    eco_mode = not C["modeEnt"] or low(st(C["modeEnt"])) in C["ecoVals"]
    hbc_sees_ev = (on(C["hbcEv"]) or low(st(C["hbcEv"])) == "true") if C["hbcEv"] else ev_charging

    # home batteries
    socs = [v for v in (num(st(i)) for i in C["socIds"]) if v is not None]
    home_soc = sum(socs) / len(socs) if socs else None
    pws = [v for v in (num(st(i)) for i in C["pwIds"]) if v is not None]
    home_w = sum(pws) if pws else None
    home_need = None if home_soc is None else max(0, 100 - home_soc) / 100 * C["kwh"]

    # sun left today
    fc_key = {"estimate": "pv_estimate", "estimate10": "pv_estimate10", "estimate90": "pv_estimate90"}.get(C["fcAttr"], "pv_estimate10")
    sun_kwh = 0.0
    today_k = day_key(now)
    rows = attr(C["today"], "detailedForecast")
    for r in (rows if isinstance(rows, list) else []):
        t = _dparse(r.get("period_start", UNDEFINED) if isinstance(r, dict) else UNDEFINED)
        e = t + 30 * 60000
        v = (num(r.get(fc_key, UNDEFINED)) if isinstance(r, dict) else None) or 0
        if math.isnan(t) or e <= now or day_key(t) != today_k:
            continue
        sun_kwh += max(v - 0.4, 0) * 0.5 * (e - max(t, now)) / (30 * 60000)
    spare = None if home_need is None else sun_kwh - 1.2 * home_need
    fc_caut = num(attr(C["fcNow"], C["fcAttr"]) if C["fcAttr"] else st(C["fcNow"])) if C["fcNow"] else None
    sun_up = st("sun.sun") == "above_horizon"

    # other HESC parts
    P = flow.get("hescPlan") or {}
    plan_owns = on("input_boolean.hesc_plan_owns_charging") or P.get("charging") is True
    park = P.get("park")
    park_busy = bool(park and park.get("solar") and not park.get("backDone"))
    plan_d: Any = {}
    raw = attr("sensor.hesc_charge_plan", "plan")
    try:
        plan_d = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except ValueError:
        plan_d = {}
    plan_goal = num(plan_d.get("goal", UNDEFINED)) if isinstance(plan_d, dict) and plan_d.get("active") is True else None
    release_busy = on("input_boolean.hpvc_external_release_request") or on("input_boolean.hesc_owns_hpvc_off")

    # state
    K = json.loads(js_json(flow.get("hescKick") or {}))
    if K.get("day") != today_k:
        K = {"day": today_k, "count": 0, "lastAt": 0, "homeFirst": False, "seq": None, "back": None,
             "chgSince": None, "evSince": None, "last": K.get("last") or {}}
    if not K.get("last"):
        K["last"] = {}
    res = Result()

    def hist(o: dict[str, Any]) -> None:
        d = {"ts": iso(now), "type": "home_battery_ev", "shadow": C["shadow"]}
        d.update(o)
        d["ctx"] = {"ev_w": ev_pow, "ev_soc": soc, "home_soc": None if home_soc is None else js_round(home_soc), "home_w": home_w,
                    "need_kwh": None if home_need is None else _fx(home_need, 1), "sun_left_kwh": _fx(sun_kwh, 1), "fc_now": fc_caut,
                    "mode": st(C["modeEnt"]) if C["modeEnt"] else None, "sw": st(C["startStop"]) if C["startStop"] else None,
                    "hbc_ev": st(C["hbcEv"]) if C["hbcEv"] else None}
        res.history.append({"payload": js_json(d)})

    def sw(s: str) -> None:
        res.actions.append(_act(sw_dom + ".turn_" + s, C["startStop"]))

    def to_solar_mode() -> None:
        """Put the charger back into its solar mode explicitly.

        v2 only presses the "back to solar" entity. On a Wallbox that entity resumes the
        schedule but does not undo the full-power charge that the kickstart's start command
        triggered, so the EV keeps charging from the grid until it is full (seen in a practice
        test: 11.1 kW for 46 min, 6.5 of 8.8 kWh from the grid). Selecting the eco
        value on the mode entity is what actually returns the charger to solar charging.
        """
        if not C["modeEnt"]:
            return
        if low(st(C["modeEnt"])) in C["ecoVals"]:
            return
        opts = attr(C["modeEnt"], "options")
        opts = opts if isinstance(opts, list) else []
        pick = next((o for o in opts if low(o) in C["ecoVals"]), None)
        if not pick:
            pick = C["ecoVals"][0]
        res.actions.append(_act(C["modeEnt"].split(".")[0] + ".select_option", C["modeEnt"], {"option": pick}))

    if home_w is not None and home_w > 500:
        K["chgSince"] = K.get("chgSince") or now
    else:
        K["chgSince"] = None
    if ev_charging:
        K["evSince"] = K.get("evSince") or now
    else:
        K["evSince"] = None

    why = ""
    if K.get("seq") and now - K["seq"]["t0"] > 15 * 60000:
        hist({"event": "kick_abandoned", "phase": K["seq"].get("phase", UNDEFINED)})
        K["seq"], K["lastAt"] = None, now

    if K.get("seq"):
        q = K["seq"]
        if not ev_conn:
            hist({"event": "kick_end", "result": "EV unplugged", "phase": q.get("phase", UNDEFINED)})
            K["seq"], K["lastAt"] = None, now
        elif q.get("phase") == "start":
            s = (now - q["t0"]) / 1000
            if s >= 20 and (hbc_sees_ev or ev_charging):
                # v3 (practice test, Wallbox Pulsar Plus): the start command is a manual
                # full-power charge that "back to solar" alone does not undo. Pause first, then hand back
                # to solar while the home battery control still holds the home batteries (see "pause").
                sw("off")
                q["phase"], q["tp"], q["kickPause"] = "pause", now, True
                hist({"event": "kick_pause", "after_s": js_round(s), "hbc_saw_ev": hbc_sees_ev})
            elif s >= START_RETRY_S and not q.get("retried") and not ev_charging and st(C["startStop"]) != "on":
                sw("on")
                q["retried"] = True
                hist({"event": "kick_start_retry"})
            elif s >= START_FAIL_S:
                sw("off")
                q["phase"], q["tp"], q["failedStart"] = "pause", now, True
                hist({"event": "kick_start_failed", "after_s": js_round(s)})
            why = "Kickstart: charger started, waiting until the home battery control sees the EV"
        elif q.get("phase") == "pause":
            if q.get("kickPause"):
                # Hand back as soon as the pause has really arrived at the charger (its start/stop switch off
                # for PAUSE_SETTLE), not before: pressed 6 s after the pause the Wallbox stayed paused, 16 s
                # after it worked (15-10). Not later either: the home battery control must still hold the home
                # batteries, so the charger finds the surplus and charges on in its solar mode.
                if st(C["startStop"]) != "on":
                    # since 3.0.0: count from the moment Home Assistant saw the switch go off, not from
                    # the round that noticed it (practice test 19-10: the hand-back came ~45 s late and
                    # the home battery control had already let go of the home batteries)
                    seen = _dparse((S.get(C["startStop"]) or {}).get("last_changed"))
                    q["offSince"] = q.get("offSince") or (int(seen) if not math.isnan(seen) and seen <= now else now)
                else:
                    q["offSince"] = None
                settled = now - q["tp"] >= PAUSE_MIN and q.get("offSince") and now - q["offSince"] >= PAUSE_SETTLE
                late = now - q["tp"] >= PAUSE_MAX
                if settled or late:
                    res.actions.append(press(C["solarBack"]))
                    to_solar_mode()
                    q["phase"], q["tr"], q["sawIdle"] = "watch", now, False
                    hist({"event": "kick_to_solar", "after_pause_s": js_round((now - q["tp"]) / 1000),
                          "pause_seen": bool(settled)})
            elif now - q["tp"] >= 40000:
                res.actions.append(press(C["solarBack"]))
                to_solar_mode()
                q["phase"], q["tr"], q["sawIdle"] = "watch", now, False
                hist({"event": "kick_to_solar"})
            why = "Kickstart: charger paused, back to solar mode in a moment"
        elif q.get("phase") == "watch":
            s = (now - q["tr"]) / 1000
            if not ev_charging:
                q["sawIdle"] = True
            if not eco_mode:
                # The charger did not take the solar mode the first time; keep asking while we watch,
                # otherwise it charges on at full power until the EV is full.
                to_solar_mode()
            if (q.get("kickPause") and not ev_charging and not q.get("resumeRetried") and s >= RESUME_RETRY_S
                    and not q.get("failedStart")):
                # "Back to solar" did not get the charger out of its pause (seen once on 15-10): press it once more.
                res.actions.append(press(C["solarBack"]))
                q["resumeRetried"] = True
                hist({"event": "kick_resume_retry"})
            if q.get("failedStart"):
                hist({"event": "kick_end", "result": "start refused"})
                K["seq"], K["lastAt"] = None, now
            elif ev_charging and (q.get("sawIdle") or s >= 360):
                hist({"event": "kick_end", "result": "ok", "minutes": _fx((now - q["t0"]) / 60000, 1)})
                K["seq"], K["lastAt"] = None, now
                K["last"]["ok"] = now
            elif s >= 480:
                hist({"event": "kick_end", "result": "no solar start"})
                K["seq"], K["lastAt"] = None, now
            why = "Kickstart: waiting for the charger to start on sun"
    elif K.get("back"):
        if not K["back"].get("done") and now - K["back"]["t0"] >= 60000:
            res.actions.append(press(C["solarBack"]))
            to_solar_mode()
            K["back"]["done"] = True
            hist({"event": "home_first_to_solar"})
        if K["back"].get("done"):
            K["back"] = None
        why = "Home batteries first: EV paused, charger back to waiting for sun"
    else:
        room = K["count"] < C["maxDay"] and now - (K.get("lastAt") or 0) >= C["gap"]
        common = (C["on"] and C["hescOn"] and can_act and ev_conn and not plan_owns and not park_busy and not release_busy
                  and home_need is not None and C["kwh"] > 0)
        ev_needs = soc is None or soc < C["fullSoc"] - 1
        if not C["on"]:
            why = "Off"
        elif not C["today"]:
            # without a solar forecast there is no "sun left today" to weigh
            why = "Off: needs a solar forecast (sun left today)"
        elif not can_act:
            why = "Not set up: start/stop switch and back-to-solar entity needed"
        elif home_need is None or C["kwh"] <= 0:
            why = "Not set up: home battery size and level sensors needed"
        elif not ev_conn:
            why = "No EV connected"
        elif plan_owns or park_busy:
            why = "Charge plan has the charger"
        elif release_busy:
            why = "HPVC release running"
        elif not sun_up:
            why = "Sun down"
        elif ev_charging:
            plan_needs = plan_goal is not None and soc is not None and soc < plan_goal - MARGIN
            tight = home_need > 0.5 and sun_kwh <= 1.2 * home_need
            if common and eco_mode and tight and not plan_needs and K.get("evSince") and now - K["evSince"] >= 10 * 60000 and room:
                if C["shadow"]:
                    hist({"event": "home_first_would", "reason": "shadow mode"})
                    K["lastAt"] = now
                else:
                    sw("off")
                    K["back"] = {"t0": now, "done": False}
                    K["count"] += 1
                    K["lastAt"], K["homeFirst"] = now, True
                    hist({"event": "home_first", "reason": "sun left today (" + js_to_fixed(sun_kwh, 1) + " kWh) only just enough for the home batteries ("
                          + js_to_fixed(home_need, 1) + " kWh)"})
                why = "Home batteries first: EV paused"
            else:
                why = ("EV charging · sun left " + js_to_fixed(sun_kwh, 1) + " kWh, home batteries need " + js_to_fixed(home_need, 1) + " kWh"
                       + (" (plan needs the EV charge)" if plan_needs else ""))
        elif not eco_mode:
            why = "Charger not in solar mode"
        elif not ev_needs:
            why = "EV full (" + _s(js_round(soc)) + "%)"
        elif K.get("homeFirst"):
            why = "Home batteries first for the rest of today"
        elif spare < C["minEv"]:
            why = "Sun left today for the home batteries (" + js_to_fixed(sun_kwh, 1) + " kWh left, " + js_to_fixed(home_need, 1) + " kWh needed)"
        elif fc_caut is None or fc_caut < C["pStart"]:
            why = ("Waiting: forecast now " + ("-" if fc_caut is None else _s(js_round(fc_caut))) + " W, start at " + _s(C["pStart"]) + " W")
        elif not K.get("chgSince"):
            why = "Waiting: home batteries not taking the sun"
        elif now - K["chgSince"] < C["tStable"]:
            why = "Waiting: home batteries charging, check again in " + _s(math.ceil((C["tStable"] - (now - K["chgSince"])) / 60000)) + " min"
        elif K["count"] >= C["maxDay"]:
            why = "Done for today (" + _s(K["count"]) + " of " + _s(C["maxDay"]) + ")"
        elif not room:
            why = "Waiting until " + local_hhmm((K.get("lastAt") or 0) + C["gap"], tz) + " (30 min between kickstarts)"
        elif common:
            if C["shadow"]:
                hist({"event": "kick_would", "reason": "shadow mode"})
                K["lastAt"] = now
                why = "[shadow] would kickstart now"
            else:
                sw("on")
                K["seq"] = {"phase": "start", "t0": now, "retried": False}
                K["count"] += 1
                K["lastAt"] = now
                hist({"event": "kick_start", "reason": "home batteries take " + _s(js_round(home_w)) + " W, sun left " + js_to_fixed(sun_kwh, 1)
                      + " kWh, home batteries need " + js_to_fixed(home_need, 1) + " kWh", "attempt": K["count"]})
                why = "Kickstart: charger started"
        else:
            why = "Waiting"

    state_txt = ("[shadow] " if C["shadow"] and C["on"] else "") + why + (
        " · today " + _s(K["count"]) + " of " + _s(C["maxDay"]) if C["on"] and K["count"] else "")
    # v2.0.1-dev2 (port of the v2.0.1 node, 12-10-2026): fewer writes to Home Assistant. A new situation is
    # written at once; when only the numbers in the text change (forecast, kWh, minutes), at most every 15 minutes.
    kind_txt = re.sub(r"[0-9]+([.,][0-9]+)?", "#", state_txt)
    if (K["last"].get("status", UNDEFINED) != state_txt and "input_text.hesc_kick_status" in S
            and (K["last"].get("kind", UNDEFINED) != kind_txt or now - (K["last"].get("statusAt") or 0) >= STATUS_EVERY)):
        K["last"]["status"], K["last"]["kind"], K["last"]["statusAt"] = state_txt, kind_txt, now
        res.status.append(_act("input_text.set_value", "input_text.hesc_kick_status", {"value": state_txt[:255]}))
    res.flow = {"hescKick": K}
    res.node_status = state_txt[:60]
    return res
