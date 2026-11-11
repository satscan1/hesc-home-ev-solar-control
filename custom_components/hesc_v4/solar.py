"""Solar charging and the HPVC release, ported line by line from v2.0.0.

Source: the "Evaluate HESC" function node in reference/v2.0.0/hesc_flow.json (v2 engine).
The function below takes the same inputs as that node (all Home Assistant states, the
node's flow context `hesc` and the clock) and returns the same outputs (four message
lists: status, HPVC, ownership, history), the new context and the node status text.

It is pure: it reads nothing and writes nothing itself. While shadow mode is on it
produces no HPVC commands, exactly like v2.

Design choice: v2's plan B (switch HPVC off and set the inverters to full,
`input_boolean.hesc_release_legacy`) is left out of v3; v3 needs HPVC 1.5.1 or newer (external
release). Identical to v2 with plan B off.

JavaScript details that change texts or numbers (Math.round, toFixed, number-to-text,
JSON.stringify, `undefined`) go through jscompat, so the output is identical to v2's.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .inputs import js_parse_float, low
from .jscompat import UNDEFINED, iso, js_json, js_number_str, js_round, js_to_fixed, local_date, local_hhmm

BAD = ("unknown", "unavailable", "none", "")
REQ = "input_boolean.hpvc_external_release_request"
HPVC_NORMAL = ("PV dynamically adjusted", "Monitoring low price", "PV full / price OK", "PV restored", "PV minimum limit")
LABELS = {
    "IDLE": "Idle",
    "WAIT_ACK": "Release requested, waiting for HPVC",
    "WAIT_START": "Release — waiting for EV",
    "CHARGING": "Release — EV charging",
}
_BINARY = re.compile(r"^(binary_sensor|switch|input_boolean)\.")
_HHMM_PREFIX = re.compile(r"^\d{1,2}:\d{2} ")


def _s(v: Any) -> str:
    """JavaScript string concatenation of a value."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return js_number_str(v)
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    return str(v)


@dataclass
class Result:
    """What the v2 node returns, plus its side effects on context and status."""

    status: list[dict[str, Any]] = field(default_factory=list)
    hpvc: list[dict[str, Any]] = field(default_factory=list)
    ownership: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    runtime: dict[str, Any] = field(default_factory=dict)
    node_status: str = ""

    @property
    def outputs(self) -> list[list[dict[str, Any]]]:
        return [self.status, self.hpvc, self.ownership, self.history]


def evaluate(S: Mapping[str, Mapping[str, Any]], context: dict[str, Any] | None, now: int) -> Result:
    """One decision round (v2 runs it every 30 s). `S` maps entity_id -> {state, attributes}."""
    res = Result()
    PA = ((S.get("sensor.hesc_prices") or {}).get("attributes")) or {}
    TZ = PA.get("tz") or "Europe/Amsterdam"

    def st(eid: str | None) -> Any:
        if not eid or eid not in S:
            return None
        return S[eid].get("state")

    def attr(eid: str | None, a: str) -> Any:
        if not eid or eid not in S:
            return None
        return (S[eid].get("attributes") or {}).get(a)

    num = js_parse_float

    def txt(eid: str | None) -> str:
        v = st(eid)
        return "" if v is None or v in BAD else str(v).strip()

    def nset(eid: str, d: float) -> float:
        v = num(st(eid))
        return d if v is None else v

    def on(eid: str | None) -> bool:
        return st(eid) == "on"

    def lst(v: Any) -> list[str]:
        return [x for x in (low(p) for p in str(v or "").split(",")) if x]

    def pw(eid: str | None) -> float | None:
        v = num(st(eid))
        if v is None:
            return None
        u = low(attr(eid, "unit_of_measurement"))
        return v * 1000 if u == "kw" else (v / 1000 if u == "mw" else v)

    # ---- configuration (HA helpers) ----
    soc_cfg = txt("input_text.hesc_ev_soc_sensor")
    C = {
        "enabled": on("input_boolean.hesc_enabled"),
        "shadow": st("input_boolean.hesc_shadow_mode") != "off",
        "useIrr": on("input_boolean.hesc_use_irradiance"),
        "fcNow": txt("input_text.hesc_forecast_now_sensor"),
        "fc30": txt("input_text.hesc_forecast_30m_sensor"),
        "fcAttr": txt("input_text.hesc_forecast_attribute"),
        "irr": txt("input_text.hesc_irradiance_sensor"),
        "pv": txt("input_text.hesc_pv_power_sensor"),
        "grid": txt("input_text.hesc_grid_power_sensor"),
        "evConn": txt("input_text.hesc_ev_connected_sensor"),
        "evPow": txt("input_text.hesc_ev_power_sensor"),
        "evGreen": txt("input_text.hesc_ev_green_energy_sensor"),
        "mode": txt("input_text.hesc_charger_mode_entity"),
        "ecoVals": lst(txt("input_text.hesc_charger_eco_value") or "eco_mode"),
        "solarSw": txt("input_text.hesc_charger_solar_switch_entity"),
        "offVals": lst(
            txt("input_text.hesc_ev_disconnected_values")
            or "off,disconnected,ready,available,no_ev_connected,unplugged,not_connected,no car,idle,ev disconnected"
        ),
        "hpvcEn": txt("input_text.hesc_hpvc_enabled_entity") or "input_boolean.hpvc_enabled",
        "hpvcLim": txt("input_text.hesc_hpvc_limited_entity") or "binary_sensor.hpvc_pv_limited",
        "hpvcStatus": "input_text.hpvc_status",
        "evSoc": "sensor.hesc_ev_soc"
        if (soc_cfg and num((S.get("sensor.hesc_ev_soc") or {}).get("state")) is not None)
        else soc_cfg,
        "evFullSoc": nset("input_number.hesc_ev_full_soc", 80),
        "pStart": nset("input_number.hesc_p_start", 2000),
        "pHold": nset("input_number.hesc_p_hold", 1500),
        "irrStart": nset("input_number.hesc_irr_start", 220),
        "irrHold": nset("input_number.hesc_irr_hold", 160),
        "tStable": nset("input_number.hesc_t_stable", 5) * 60000,
        "tStart": nset("input_number.hesc_t_start", 10) * 60000,
        "tDip": nset("input_number.hesc_t_dip", 5) * 60000,
        "tStop": nset("input_number.hesc_t_stop", 5) * 60000,
        "tMax": nset("input_number.hesc_t_max", 240) * 60000,
        "cooldown": nset("input_number.hesc_cooldown", 30) * 60000,
        "maxAttempts": nset("input_number.hesc_max_attempts", 3),
        "ackTimeout": 5 * 60000,
        "activeW": nset("input_number.hesc_ev_active_w", 400),
        "standalone": on("input_boolean.hesc_standalone"),
    }

    # ---- live values ----
    def fc_val(eid: str) -> float | None:
        if not eid:
            return None
        return num(attr(eid, C["fcAttr"])) if C["fcAttr"] else num(st(eid))

    g = pw(C["grid"])
    if C["evConn"] and _BINARY.match(C["evConn"]):
        ev_conn = on(C["evConn"])
    else:
        sc = st(C["evConn"])
        ev_conn = bool(C["evConn"]) and sc is not None and sc not in BAD and low(sc) not in C["offVals"]
    L = {
        "fcNow": fc_val(C["fcNow"]),
        "fc30": fc_val(C["fc30"]),
        "fcMedian": num(st(C["fcNow"])),
        "irr": num(st(C["irr"])) if (C["useIrr"] and C["irr"]) else None,
        "pv": pw(C["pv"]),
        "grid": None if g is None else (-g if on("input_boolean.hesc_grid_export_positive") else g),
        "evConn": ev_conn,
        "evPow": pw(C["evPow"]),
        "evGreen": num(st(C["evGreen"])) if C["evGreen"] else None,
        "mode": st(C["mode"]),
        "solarSwOn": (not C["solarSw"]) or on(C["solarSw"]),
        "hpvcOn": on(C["hpvcEn"]),
        "hpvcLimited": on(C["hpvcLim"]),
        "sun": st("sun.sun") == "above_horizon",
        "hpvcStatus": txt(C["hpvcStatus"]),
        "evSoc": num(st(C["evSoc"])) if C["evSoc"] else None,
        "relIface": REQ in S and bool(S[REQ]),
        "relReq": on(REQ),
        "relActive": on("binary_sensor.hpvc_external_release_active"),
    }

    def bad_state(v: Any) -> bool:
        return v is None or v in BAD

    missing: list[str] = []
    if L["fcNow"] is None:
        missing.append("forecast now")
    if L["fc30"] is None:
        missing.append("forecast +30m")
    if L["pv"] is None:
        missing.append("PV power")
    if L["evPow"] is None:
        missing.append("EV power")
    if not C["evConn"] or bad_state(st(C["evConn"])):
        missing.append("EV connected")
    if not C["mode"] or bad_state(L["mode"]):
        missing.append("charger mode")
    if not C["standalone"] and bad_state(st(C["hpvcEn"])):
        missing.append("HPVC enabled")
    irr_used = C["useIrr"] and bool(C["irr"]) and L["irr"] is not None
    in_solar = low(L["mode"]) in C["ecoVals"] and L["solarSwOn"]
    valid = not missing

    # ---- persistent runtime context ----
    today = local_date(now, TZ)
    X = context or {
        "state": "IDLE", "since": now, "stableSince": None, "dipSince": None, "stopSince": None,
        "cooldownUntil": 0, "lastTick": now, "rel": None, "eco": None, "acc": None, "day": None, "last": {},
    }
    if not X.get("day") or X["day"].get("date") != today:
        X["day"] = {"date": today, "releases": 0, "success": 0, "failed": 0, "ecoSessions": 0,
                    "fcWh": 0, "pvWh": 0, "evWh": 0, "greenKwh": 0}
    dtH = min(max((now - (X.get("lastTick") or now)) / 3600000, 0), 0.05)
    X["lastTick"] = now

    ev_waiting = L["evConn"] and in_solar and L["evPow"] is not None and L["evPow"] <= C["activeW"]
    ev_charging = L["evPow"] is not None and L["evPow"] > C["activeW"]
    hpvc_blocks = L["hpvcOn"] and L["hpvcLimited"]
    ev_full = L["evSoc"] is not None and L["evSoc"] >= C["evFullSoc"] - 1
    msgs1, msgs2, msgs3, msgs4 = res.status, res.hpvc, res.ownership, res.history

    def act(action: str, entity: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"payload": {"action": action, "target": {"entity_id": [entity]}, "data": data or {}}}

    fc_low = min(L["fcNow"], L["fc30"]) if (L["fcNow"] is not None and L["fc30"] is not None) else None
    fc_start_ok = fc_low is not None and fc_low >= C["pStart"]
    fc_hold_ok = fc_low is not None and fc_low >= C["pHold"]
    irr_start_ok = not irr_used or L["irr"] >= C["irrStart"]
    irr_hold_ok = not irr_used or L["irr"] >= C["irrHold"]

    def hist(o: dict[str, Any]) -> None:
        msgs4.append({"payload": js_json({"ts": iso(now), "shadow": C["shadow"], **o})})

    def r0(v: float | None) -> int | None:
        return None if v is None else js_round(v)

    def snapshot() -> dict[str, Any]:
        return {
            "fc_now": r0(L["fcNow"]), "fc_30m": r0(L["fc30"]), "fc_median": r0(L["fcMedian"]), "irr": r0(L["irr"]),
            "pv": r0(L["pv"]), "grid": r0(L["grid"]), "ev": r0(L["evPow"]),
            "mode": UNDEFINED if L["mode"] is None else L["mode"],
            "hpvc_on": L["hpvcOn"], "hpvc_limited": L["hpvcLimited"], "hpvc_status": L["hpvcStatus"],
            "standalone": bool(C["standalone"]),
            "ev_soc": None if L["evSoc"] is None else js_round(L["evSoc"] * 10) / 10,
        }

    def integrate(sess: dict[str, Any] | None) -> None:
        if not sess:
            return
        if L["fcMedian"] is not None:
            sess["fcWh"] += L["fcMedian"] * dtH
        if L["pv"] is not None:
            sess["pvWh"] += L["pv"] * dtH
        if L["evPow"] is not None:
            sess["evWh"] += L["evPow"] * dtH

    def close_session(sess: dict[str, Any], typ: str, why: str) -> None:
        gs = sess.get("greenStart")
        green = max(0, L["evGreen"] - gs) if (gs is not None and L["evGreen"] is not None) else None
        acc = js_round(100 * sess["pvWh"] / sess["fcWh"]) if sess["fcWh"] > 0 else None
        sdm = sess.get("startDelayMin", UNDEFINED)
        forced = sess.get("forced", UNDEFINED)
        hist({
            "type": typ, "reason": why, "start": iso(sess["start"]), "minutes": js_round((now - sess["start"]) / 60000),
            "forecast_wh": js_round(sess["fcWh"]), "pv_wh": js_round(sess["pvWh"]), "actual_vs_forecast_pct": acc,
            "ev_wh": js_round(sess["evWh"]),
            "ev_green_kwh": None if green is None else js_round(green * 100) / 100,
            "ev_started": bool(sess.get("evStarted")),
            "start_delay_min": None if sdm is UNDEFINED else sdm,
            "forced_start": UNDEFINED if forced is UNDEFINED else bool(forced),
            "start_ctx": sess.get("ctx", UNDEFINED), "end_ctx": snapshot(),
        })
        if not sess.get("forced"):
            d = X["day"]
            d["fcWh"] += sess["fcWh"]
            d["pvWh"] += sess["pvWh"]
            d["evWh"] += sess["evWh"]
            if green is not None:
                d["greenKwh"] += green

    def new_session() -> dict[str, Any]:
        return {"start": now, "fcWh": 0, "pvWh": 0, "evWh": 0, "greenStart": L["evGreen"], "evStarted": False, "ctx": snapshot()}

    reason = ""

    def reset_idle() -> None:
        X["state"] = "IDLE"
        X["since"] = now
        X["stableSince"] = None
        X["dipSince"] = None
        X["stopSince"] = None

    def restore(why: str) -> None:
        nonlocal reason
        if not C["shadow"] and L["relReq"]:
            msgs2.append(act("input_boolean.turn_off", REQ))
        if X.get("rel"):
            if X["rel"].get("evStarted"):
                X["day"]["success"] += 1
            elif why != "EV full":
                X["day"]["failed"] += 1
            close_session(X["rel"], "release", why)
            X["rel"] = None
        X["cooldownUntil"] = now + C["cooldown"]
        reset_idle()
        reason = "Release ended: " + why

    def minutes(ms: float) -> str:
        return js_number_str(js_round(ms / 60000))

    # ---- disable / standalone ----
    if not C["enabled"] and X["state"] != "IDLE":
        restore("HESC disabled")
    elif C["standalone"] and X["state"] != "IDLE":
        restore("standalone mode switched on")

    if not C["shadow"] and X["state"] == "IDLE" and L["relReq"]:
        msgs2.append(act("input_boolean.turn_off", REQ))

    # ---- state machine ----
    if C["enabled"] and reason == "":
        state = X["state"]
        if state == "IDLE":
            attempts_left = (X["day"]["releases"] - X["day"]["success"]) < C["maxAttempts"]
            ready = (
                not C["standalone"] and valid and L["sun"] and ev_waiting and hpvc_blocks
                and L["relIface"]
                and not ev_full and fc_start_ok and irr_start_ok and now >= X["cooldownUntil"] and attempts_left
            )
            if ready:
                X["stableSince"] = X.get("stableSince") or now
                if now - X["stableSince"] >= C["tStable"]:
                    X["state"] = "WAIT_ACK"
                    X["since"] = now
                    X["stableSince"] = None
                    if not C["shadow"]:
                        msgs2.append(act("input_boolean.turn_on", REQ))
                    reason = ("Release requested: HESC " + ("would ask" if C["shadow"] else "asked")
                              + " HPVC for full PV, waiting for HPVC to confirm")
                else:
                    reason = ("Conditions met, confirming (" + minutes(now - X["stableSince"]) + "/"
                              + minutes(C["tStable"]) + " min)")
            else:
                X["stableSince"] = None
                if not valid:
                    reason = "Waiting for inputs: " + ", ".join(missing)
                elif not L["sun"]:
                    reason = "Night"
                elif not L["evConn"]:
                    reason = "No EV connected"
                elif not in_solar:
                    reason = "Charger not in solar mode"
                elif ev_charging:
                    reason = "EV is charging"
                elif C["standalone"]:
                    reason = "Standalone (no HPVC): the charger starts on solar by itself"
                elif not hpvc_blocks:
                    reason = "HPVC is not limiting PV — nothing to release"
                elif not L["relIface"]:
                    reason = "HPVC has no external release interface (needs HPVC 1.5.1 or newer)"
                elif ev_full:
                    reason = "EV already full, no release needed"
                elif not fc_start_ok:
                    reason = "Forecast too low (< " + _s(C["pStart"]) + " W)"
                elif not irr_start_ok:
                    reason = "Irradiance too low (< " + _s(C["irrStart"]) + " W/m²)"
                elif now < X["cooldownUntil"]:
                    reason = "Cooldown until " + local_hhmm(X["cooldownUntil"], TZ)
                else:
                    reason = "Maximum release attempts reached today"
        elif state == "WAIT_ACK":
            if not valid:
                restore("inputs unavailable")
            elif not L["evConn"] or not in_solar:
                restore("EV disconnected or charger not in solar mode")
            elif not L["sun"]:
                restore("sunset")
            elif C["shadow"] or L["relActive"]:
                X["state"] = "WAIT_START"
                X["since"] = now
                X["day"]["releases"] += 1
                X["rel"] = new_session()
                reason = ("Release: HPVC " + ("would confirm" if C["shadow"] else "confirmed")
                          + " full PV, the charger can start in solar mode")
            elif now - X["since"] >= C["ackTimeout"]:
                restore("HPVC busy (" + (L["hpvcStatus"] or "unknown") + "), no release confirmation within "
                        + minutes(C["ackTimeout"]) + " min, request withdrawn")
            else:
                reason = ("Waiting for HPVC to confirm the release (" + minutes(now - X["since"]) + "/"
                          + minutes(C["ackTimeout"]) + " min, HPVC: " + (L["hpvcStatus"] or "unknown") + ")")
        elif state == "WAIT_START":
            integrate(X["rel"])
            if not valid:
                restore("inputs unavailable")
            elif not L["evConn"] or not in_solar:
                restore("EV disconnected or charger not in solar mode")
            elif not L["sun"]:
                restore("sunset")
            elif ev_charging:
                X["rel"]["startDelayMin"] = js_round((now - X["since"]) / 6000) / 10
                X["state"] = "CHARGING"
                X["since"] = now
                X["rel"]["evStarted"] = True
                reason = "EV started charging on solar"
            elif now - X["since"] >= C["tStart"]:
                if ev_full:
                    restore("EV full")
                else:
                    restore("EV did not start within " + minutes(C["tStart"]) + " min")
            else:
                reason = ("Waiting for the charger to start in solar mode (" + minutes(now - X["since"]) + "/"
                          + minutes(C["tStart"]) + " min)")
        elif state == "CHARGING":
            integrate(X["rel"])
            hold_ok = fc_hold_ok and irr_hold_ok
            X["dipSince"] = None if hold_ok else (X.get("dipSince") or now)
            X["stopSince"] = None if ev_charging else (X.get("stopSince") or now)
            if not valid:
                restore("inputs unavailable")
            elif not L["evConn"] or not in_solar:
                restore("EV disconnected or charger not in solar mode")
            elif not L["sun"]:
                restore("sunset")
            elif X["stopSince"] and now - X["stopSince"] >= C["tStop"]:
                restore("EV full" if ev_full else "EV stopped charging")
            elif X["dipSince"] and now - X["dipSince"] >= C["tDip"]:
                restore("solar below hold threshold")
            elif now - X["rel"]["start"] >= C["tMax"]:
                restore("maximum release duration")
            else:
                reason = "Release active — EV charging on solar"
    if not C["enabled"] and reason == "":
        reason = "HESC disabled"

    # ---- independent Eco charge sessions ----
    plan_grid = on("input_boolean.hesc_plan_owns_charging")
    eco_charging = ev_charging and in_solar and L["sun"] and not plan_grid
    if eco_charging and not X.get("eco"):
        X["eco"] = new_session()

        def num0(v: Any) -> bool:
            return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)

        X["eco"]["forced"] = bool(num0(L["fcNow"]) and num0(L["pv"]) and L["fcNow"] < C["pHold"] and L["pv"] < C["pHold"])
        if X["eco"]["forced"]:
            X["day"]["forcedSessions"] = (X["day"].get("forcedSessions") or 0) + 1
        else:
            X["day"]["ecoSessions"] += 1
    if X.get("eco"):
        integrate(X["eco"])
    if not eco_charging and X.get("eco"):
        close_session(X["eco"], "eco_charge",
                      "ev full" if ev_full else ("grid charging by plan" if plan_grid else "charging ended"))
        X["eco"] = None

    # ---- source reliability: 15-minute daylight intervals ----
    SLOT = 15 * 60000
    slot = math.floor(now / SLOT) * SLOT
    if X.get("acc") and X["acc"]["slot"] != slot:
        a = X["acc"]
        if a["n"] >= 10:
            hist({"type": "accuracy", "slot_start": iso(a["slot"]), "minutes": 15,
                  "fc_w": js_round(a["fc"] / a["nf"]), "fc10_w": js_round(a["fc10"] / a["n10"]) if a["n10"] else None,
                  "pv_w": js_round(a["pv"] / a["np"]),
                  "irr_wm2": js_round(a["irr"] / a["ni"]) if a["ni"] else None,
                  "hpvc_limited_share": js_round(100 * a["lim"] / a["n"]) / 100})
        X["acc"] = None
    if L["sun"] and L["fcMedian"] is not None and L["pv"] is not None:
        if not X.get("acc"):
            X["acc"] = {"slot": slot, "n": 0, "nf": 0, "fc": 0, "n10": 0, "fc10": 0, "np": 0, "pv": 0, "ni": 0, "irr": 0, "lim": 0}
        a = X["acc"]
        a["n"] += 1
        a["nf"] += 1
        a["fc"] += L["fcMedian"]
        a["np"] += 1
        a["pv"] += L["pv"]
        if C["fcAttr"] and L["fcNow"] is not None:
            a["n10"] += 1
            a["fc10"] += L["fcNow"]
        if L["irr"] is not None:
            a["ni"] += 1
            a["irr"] += L["irr"]
        if L["hpvcLimited"]:
            a["lim"] += 1

    # ---- status publication (only on change) ----
    state_txt = ("[shadow] " if C["shadow"] else "") + (LABELS[X["state"]] if C["enabled"] else "Disabled")
    d = X["day"]
    acc_txt = js_number_str(js_round(100 * d["pvWh"] / d["fcWh"])) + "%" if d["fcWh"] > 0 else "–"
    insight1 = ("Today: " + _s(d["releases"]) + " releases (" + _s(d["success"]) + " ok, " + _s(d["failed"])
                + " failed), " + _s(d["ecoSessions"]) + " solar sessions"
                + (", " + _s(d["forcedSessions"]) + " manual/scheduled" if d.get("forcedSessions") else ""))[:255]
    insight2 = ("Today: actual PV vs forecast during charging " + acc_txt + ", EV " + js_to_fixed(d["evWh"] / 1000, 1)
                + " kWh (" + js_to_fixed(d["greenKwh"], 1) + " kWh solar)")[:255]
    insight3 = ("Now: forecast " + ("–" if r0(fc_low) is None else _s(r0(fc_low)) + " W")
                + ((", irradiance " + ("–" if r0(L["irr"]) is None else _s(r0(L["irr"])) + " W/m²")) if (C["useIrr"] and C["irr"]) else "")
                + ", PV " + ("–" if r0(L["pv"]) is None else _s(r0(L["pv"])) + " W")
                + ", HPVC " + ("limiting" if hpvc_blocks else ("on" if L["hpvcOn"] else "off")))[:255]
    pub = {"input_text.hesc_state": state_txt, "input_text.hesc_reason": reason[:255],
           "input_text.hesc_insight_1": insight1, "input_text.hesc_insight_2": insight2}
    last = X["last"]
    if last.get("input_text.hesc_reason", UNDEFINED) != reason[:255]:
        pub["input_text.hesc_insight_3"] = insight3
    for eid, v in pub.items():
        if last.get(eid, UNDEFINED) != v and S.get(eid):
            last[eid] = v
            msgs1.append(act("input_text.set_value", eid, {"value": v}))
    if "action" not in last:
        o = S.get("input_text.hesc_last_action")
        cur = str(o.get("state")) if isinstance(o, Mapping) else str(o or "")
        last["action"] = _HHMM_PREFIX.sub("", cur, count=1)
    if reason and reason.startswith("Re") and last["action"] != reason:
        last["action"] = reason
        la = (local_hhmm(now, TZ) + " " + reason)[:255]
        if S.get("input_text.hesc_last_action"):
            msgs1.append(act("input_text.set_value", "input_text.hesc_last_action", {"value": la}))
        hist({"type": "event", "text": reason, "ctx": snapshot()})

    res.context = X
    res.runtime = {"state": X["state"], "since": X["since"], "cooldownUntil": X["cooldownUntil"], "day": X["day"]}
    res.node_status = state_txt + " · " + reason[:40]
    return res
