"""Charge plan control: start and stop grid charging at the planned quarters.

Line-by-line port of v2.0.0's Node-RED function node "Charge plan" (runs with every input
update). Takes all states (Node-RED form), the node's flow context and the clock; returns the
three message lists (status, charger actions, history lines), the new flow context and the
node status text. Pure: it reads and writes nothing itself. In shadow mode it sends no
charger commands, exactly like v2. Proven identical to the original node on random runs
(`tests/integration/test_chargeplan_parity.py`).
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .inputs import js_parse_float
from .jscompat import UNDEFINED, iso, js_json, js_number_str, js_round, js_to_fixed
from .price_forecast import date_parse

BAD = ("unknown", "unavailable", "none", "")
MARGIN = 3
_BINARY = re.compile(r"^(binary_sensor|switch|input_boolean)\.")
_WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_OFF_DEFAULT = "off,disconnected,ready,available,no_ev_connected,unplugged,not_connected,no car,idle,ev disconnected"


def _s(v: Any) -> str:
    """JavaScript string concatenation of a value."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return js_number_str(v)
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    return str(v)


def _join(v: Any) -> str:
    """Array.prototype.join element: null/undefined become ''."""
    return "" if v is None or v is UNDEFINED else _s(v)


def _truthy(v: Any) -> bool:
    if v is None or v is UNDEFINED or v is False:
        return False
    if isinstance(v, (int, float)):
        return not (v == 0 or (isinstance(v, float) and math.isnan(v)))
    if isinstance(v, str):
        return v != ""
    return True


def _num(v: Any) -> float | None:
    return js_parse_float(v)


def _or0(v: Any) -> float:
    """v2's `(X.refused || 0)`: anything falsy counts as 0."""
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and _truthy(v) else 0


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
    status: list[dict[str, Any]] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    flow: dict[str, Any] = field(default_factory=dict)
    node_status: str = ""


def run(S: dict[str, Any], flow: dict[str, Any], now: int) -> Result:  # noqa: C901 - mirrors the v2 node
    """One run of v2's "Charge plan" node. flow: the node's flow context (hescPlan, hescLastPlan, hescNoticeP1)."""
    flow = json.loads(js_json(flow)) if flow else {}
    pa = ((S.get("sensor.hesc_prices") or {}).get("attributes") or {})
    tzname = pa.get("tz") or "Europe/Amsterdam"
    tz = ZoneInfo(tzname)
    minor = pa.get("minor") or "ct"

    def st(i: Any) -> Any:
        return S[i].get("state") if i and i in S else UNDEFINED

    def attr(i: Any, a: str) -> Any:
        if i and i in S and S[i].get("attributes") is not None:
            return S[i]["attributes"].get(a, UNDEFINED)
        return UNDEFINED

    def txt(i: str) -> str:
        v = st(i)
        return "" if (v is UNDEFINED or v is None or v in BAD) else _s(v).strip()

    def on(i: str) -> bool:
        return st(i) == "on"

    def low(v: Any) -> str:
        return ("" if v is None or v is UNDEFINED else _s(v)).strip().lower()

    def lst(v: str) -> list[str]:
        return [x for x in (low(p) for p in (v or "").split(",")) if x]

    def hhmm(t: float) -> str:
        return datetime.fromtimestamp(t / 1000, tz).strftime("%H:%M")

    C: dict[str, Any] = {
        "shadow": st("input_boolean.hesc_shadow_mode") != "off",
        "startStop": txt("input_text.hesc_charger_start_stop_entity"),
        "solarBack": txt("input_text.hesc_charger_resume_entity"),
        "gridMode": txt("input_text.hesc_charger_grid_mode_value"),
        "modeEnt": txt("input_text.hesc_charger_mode_entity"),
        "ecoVals": lst(txt("input_text.hesc_charger_eco_value") or "eco_mode"),
        "evConn": txt("input_text.hesc_ev_connected_sensor"),
        "offVals": lst(txt("input_text.hesc_ev_disconnected_values") or _OFF_DEFAULT),
        "oppOn": on("input_boolean.hesc_plan_opportunity"),
        "oppPrice": _num(st("input_number.hesc_plan_opportunity_price")),
        "priceSensor": "sensor.hesc_prices",
        "marginMin": 15,
        "tStart": (_num(st("input_number.hesc_t_start")) or 10) * 60000,
        "tStop": (_num(st("input_number.hesc_t_stop")) or 5) * 60000,
        "fcNow": txt("input_text.hesc_forecast_now_sensor"),
        "fcAttr": txt("input_text.hesc_forecast_attribute"),
        "pStart": _num(st("input_number.hesc_p_start")) or 1500,
        "fullSoc": _num(st("input_number.hesc_ev_full_soc")) or 80,
    }
    ev_soc_ent = S.get("sensor.hesc_ev_soc") or {}
    C["evSoc"] = ("sensor.hesc_ev_soc" if (txt("input_text.hesc_ev_soc_sensor") and _num(ev_soc_ent.get("state")) is not None)
                  else txt("input_text.hesc_ev_soc_sensor"))
    C["method"] = "Start/stop switch" if C["startStop"] else ("Mode value" if (C["gridMode"] and C["modeEnt"]) else "Off")
    sw_dom = C["startStop"].split(".")[0] if C["startStop"] else ""
    can_park = C["method"] == "Start/stop switch" and bool(C["startStop"]) and not C["startStop"].startswith("button.")
    if _BINARY.match(C["evConn"]):
        ev_conn = on(C["evConn"])
    else:
        v = st(C["evConn"])
        ev_conn = bool(C["evConn"]) and not (v is UNDEFINED or v is None or v in BAD) and low(v) not in C["offVals"]
    soc = _num(st(C["evSoc"])) if C["evSoc"] else None
    pw_id = txt("input_text.hesc_ev_power_sensor")
    pw_raw = _num(st(pw_id))
    pw_unit = low(attr(pw_id, "unit_of_measurement"))
    ev_pow = None if pw_raw is None else (pw_raw * 1000 if pw_unit == "kw" else pw_raw)
    ev_charging = ev_pow is not None and ev_pow > (_num(st("input_number.hesc_ev_active_w")) or 400)
    fc_caut = _num(attr(C["fcNow"], C["fcAttr"]) if C["fcAttr"] else st(C["fcNow"])) if C["fcNow"] else None
    sun_go = st("sun.sun") == "above_horizon" and fc_caut is not None and fc_caut >= C["pStart"]

    P: Any = {}
    raw = attr("sensor.hesc_charge_plan", "plan")
    try:
        if isinstance(raw, str):
            P = json.loads(raw)
        else:
            P = raw if _truthy(raw) else {}
    except ValueError:
        P = {}
    if not isinstance(P, dict):
        P = {}
    plan_ok = isinstance(P, dict) and isinstance(P.get("deadline"), str) and isinstance(P.get("planned"), list)
    last_plan = flow.get("hescLastPlan")
    if plan_ok:
        flow["hescLastPlan"] = {"p": P, "at": now}
    elif isinstance(last_plan, dict) and _truthy(last_plan.get("p")) and now - last_plan.get("at", math.nan) <= 10 * 60000:
        P = last_plan["p"]
    goal = _num(P.get("goal", UNDEFINED))
    plan_active = P.get("active") is True
    deadline = _dparse(P.get("deadline")) if _truthy(P.get("deadline")) else None
    need_kwh = _num(P.get("need_kwh", UNDEFINED)) or 0
    kw = _num(P.get("kw", UNDEFINED)) or 0
    planned = [x for x in (_dparse(t) for t in P["planned"]) if not math.isnan(x)] if isinstance(P.get("planned"), list) else []

    X = flow.get("hescPlan")
    owns_ha = on("input_boolean.hesc_plan_owns_charging")
    if not _truthy(X):
        X = {"charging": owns_ha, "since": now, "last": {}}
    eff_goal = goal if (plan_active and goal is not None) else C["fullSoc"]
    if soc is None:
        below_goal = plan_active and need_kwh > 0
    else:
        below_goal = soc < eff_goal - (0.5 if _truthy(X.get("charging")) else MARGIN)

    price = None
    rows = _as_list(attr(C["priceSensor"], "raw_today")) + _as_list(attr(C["priceSensor"], "raw_tomorrow"))
    for r in rows:
        a, b = _dparse(_get(r, "start")), _dparse(_get(r, "end"))
        if now >= a and now < b:
            price = _num(_get(r, "value"))
            break

    in_planned = any(now >= t and now < t + 15 * 60000 for t in planned)
    need_min = (need_kwh / kw) * 60 if kw > 0 else 0
    left_min = (deadline - now) / 60000 if _truthy(deadline) else None
    safety_net = (plan_active and deadline is not None and _gt(left_min, 0) and need_kwh > 0
                  and _le(left_min, need_min + C["marginMin"]))
    chance = C["oppOn"] and price is not None and C["oppPrice"] is not None and price <= C["oppPrice"]
    sun_covers, sun_kwh, need_chance = False, 0.0, 0.0
    if chance and soc is not None:
        def day_key(t: float) -> str:
            return datetime.fromtimestamp(t / 1000, tz).strftime("%Y-%m-%d")
        tgt = eff_goal
        cap_c = _num(st("input_number.hesc_ev_battery_kwh")) or 60
        kw_c = _num(st("input_number.hesc_plan_charge_kw")) or 11
        p_hold = _num(st("input_number.hesc_p_hold")) or 1200
        fc_key = {"estimate": "pv_estimate", "estimate10": "pv_estimate10", "estimate90": "pv_estimate90"}.get(C["fcAttr"], "pv_estimate10")
        need_chance = max(0, tgt - soc) / 100 * cap_c
        today = day_key(now)
        for r in _as_list(attr(txt("input_text.hesc_solar_today_sensor"), "detailedForecast")):
            t = _dparse(_get(r, "period_start"))
            e = t + 30 * 60000
            v = (_num(_get(r, fc_key)) or 0) * 1000
            if math.isnan(t) or e <= now or day_key(t) != today or v < p_hold:
                continue
            frac = (e - max(t, now)) / (30 * 60000)
            sun_kwh += min(max(v / 1000 - 0.4, 0), kw_c) * 0.5 * frac
        sun_covers = need_chance > 0 and sun_kwh >= 1.2 * need_chance
    final_min = _num(st("input_number.hesc_plan_final_check_min"))
    final_win = (plan_active and deadline is not None and _gt(left_min, 0) and final_min is not None and final_min > 0
                 and _le(left_min, final_min))
    want, why = False, ""
    if C["method"] == "Off":
        why = "Grid charging not set up (Settings → Charge plan)"
    elif not ev_conn:
        why = "No EV connected"
    elif not below_goal:
        if soc is None:
            why = "Nothing to charge"
        elif not plan_active:
            why = "No active plan"
        elif soc < eff_goal - 0.5:
            why = "Within " + _s(MARGIN) + "% of goal (" + _s(js_round(soc)) + "%, charges below " + _s(eff_goal - MARGIN) + "%)"
        else:
            why = "Goal reached (" + _s(js_round(soc)) + "%)"
    elif plan_active and in_planned:
        want, why = True, "Planned quarter"
    elif safety_net:
        want, why = True, "Safety net: only just enough time left"
    elif final_win:
        want, why = True, "Final check: below goal, charging to goal"
    elif chance and sun_covers:
        why = "Cheap chance skipped: enough sun today (~" + js_to_fixed(sun_kwh, 1) + " kWh for " + js_to_fixed(need_chance, 1) + " kWh)"
    elif chance:
        want, why = True, "Cheap chance (" + js_to_fixed(price * 100, 1) + " " + minor + " ≤ " + js_to_fixed(C["oppPrice"] * 100, 1) + " " + minor + ")"
    else:
        why = "Waiting for the next planned quarter" if plan_active else "No active plan"

    M = {"on": on("input_boolean.hesc_min_charge_enabled"), "soc": _num(st("input_number.hesc_min_charge_soc")),
         "hours": _num(st("input_number.hesc_min_charge_hours")), "cap": _num(st("input_number.hesc_ev_battery_kwh")),
         "kw": _num(st("input_number.hesc_plan_charge_kw"))}
    if not M["on"] or not ev_conn or soc is None or M["soc"] is None or soc >= M["soc"]:
        X["min"] = None
    elif C["method"] != "Off":
        if not _truthy(X.get("min")):
            X["min"] = {"since": now, "deadline": now + max(0.5, M["hours"] or 3) * 3600000}
        need_min_kwh = (M["soc"] - soc) / 100 * (M["cap"] or 60)
        q = max(1, math.ceil(need_min_kwh / (M["kw"] or 11) * 4))
        slots = []
        for r in rows:
            a, b, v = _dparse(_get(r, "start")), _dparse(_get(r, "end")), _num(_get(r, "value"))
            if math.isnan(a) or math.isnan(b) or v is None:
                continue
            t = a
            while t < b:
                if t + 15 * 60000 > now and t < X["min"]["deadline"]:
                    slots.append({"t": t, "v": v})
                t += 15 * 60000
        slots.sort(key=lambda x: (x["v"], x["t"]))
        chosen = slots[:q]
        left = (X["min"]["deadline"] - now) / 60000
        min_net = left <= (need_min_kwh / (M["kw"] or 11)) * 60 + C["marginMin"]
        in_chosen = any(now >= s["t"] and now < s["t"] + 15 * 60000 for s in chosen)
        nxt = sorted([s for s in chosen if s["t"] > now], key=lambda s: s["t"])
        nxt = nxt[0] if nxt else None
        if not want:
            if len(slots) == 0 or in_chosen or min_net or left <= 0:
                want, why = True, "Minimum charge: below " + _s(M["soc"]) + "%, charging (ready by " + hhmm(X["min"]["deadline"]) + ")"
            else:
                why = ("Minimum charge: below " + _s(M["soc"]) + "%, waiting for the cheapest quarter"
                       + (" (" + hhmm(nxt["t"]) + ")" if nxt else "") + ", ready by " + hhmm(X["min"]["deadline"]))

    # v2.0.1 (12-10-2026): a charger that keeps refusing a planned start. Three "stopped by itself" rounds in a row in
    # which the EV never drew power: no more starts for this plan, one notification. Counting starts again when the EV
    # charges (by itself or later), the EV is unplugged, or the plan changes. The final check may still try (see below).
    if not ev_conn or (ev_charging and not _truthy(X.get("charging"))):
        X["refused"], X["refusedNotified"] = 0, False
    if _truthy(X.get("charging")) and ev_charging:
        X["drew"] = True
    if not ev_conn or (_truthy(X.get("doneUntil")) and now >= X["doneUntil"]):
        X["doneUntil"] = None
    # v2.0.1-dev5 (12-10-2026): after 3 refused starts the final check may still try ONCE in the final window, also when
    # the reason in that hour is "Planned quarter" or "Safety net" (before: only the literal reason "Final check" was
    # exempt, which almost never won, so no last try happened). X.finalTried resets as soon as the count is back at 0.
    if not (_or0(X.get("refused")) > 0):
        X["finalTried"] = False
    final_try = want and final_win and _or0(X.get("refused")) >= 3 and (not _truthy(X.get("finalTried")) or _truthy(X.get("charging")))
    if want and _truthy(X.get("doneUntil")) and not final_try and why.find("Final check") != 0:
        want, why = False, "Finished, charger stopped by itself"
    if _truthy(X.get("charging")) and ev_conn and now - X["since"] >= C["tStart"]:
        if ev_charging:
            X["idleSince"] = None
        else:
            X["idleSince"] = X.get("idleSince") if _truthy(X.get("idleSince")) else now
        if _truthy(X.get("idleSince")) and now - X["idleSince"] >= C["tStop"]:
            want, why = False, "Finished, charger stopped by itself"
            X["doneUntil"] = now + 30 * 60000
            X["refused"] = (_or0(X.get("refused")) + 1) if X.get("drew") is False else 0
    elif not _truthy(X.get("charging")):
        X["idleSince"] = None
    if want and _or0(X.get("refused")) >= 3 and not final_try:
        want, why = False, "Charger refused to start 3 times, no more starts for this plan"
    if want and _or0(X.get("refused")) >= 3 and final_try and not _truthy(X.get("finalTried")):
        X["finalTried"] = True
        why = "Final check: one more try after refused starts"

    msgs1: list[dict[str, Any]] = []
    msgs2: list[dict[str, Any]] = []
    msgs3: list[dict[str, Any]] = []

    def hist(o: dict[str, Any]) -> None:
        rec = {"ts": iso(now), "type": "charge_plan", "shadow": C["shadow"]}
        rec.update(o)
        rec["chg"] = {"mode": st(C["modeEnt"]) if C["modeEnt"] else None, "sw": st(C["startStop"]) if C["startStop"] else None,
                      "ev_w": ev_pow, "conn": ev_conn}
        msgs3.append({"payload": js_json(rec)})

    def start_grid() -> None:
        if C["shadow"]:
            return
        X["prevMode"] = st(C["modeEnt"]) if C["modeEnt"] else None
        park = X.get("park")
        X["prevSwitch"] = park.get("prev", UNDEFINED) if _truthy(park) else (st(C["startStop"]) if C["startStop"] else None)
        X["park"] = None
        X["resume"] = None
        if C["method"] == "Start/stop switch" and C["startStop"]:
            msgs2.append(_act("button.press" if C["startStop"].startswith("button.") else sw_dom + ".turn_on", C["startStop"]))
        elif C["method"] == "Mode value" and C["modeEnt"] and C["gridMode"]:
            msgs2.append(_act(C["modeEnt"].split(".")[0] + ".select_option", C["modeEnt"], {"option": C["gridMode"]}))
        msgs1.append(_act("input_boolean.turn_on", "input_boolean.hesc_plan_owns_charging"))

    def stop_grid() -> None:
        if C["shadow"]:
            return
        if can_park and C["solarBack"]:
            msgs2.append(_act(sw_dom + ".turn_off", C["startStop"]))
            X["park"] = {"since": now, "prev": "solar", "solar": True, "tries": 1, "nextCheck": now + 1e12, "confirmed": False,
                         "backAt": now + 60000, "backDone": False}
        elif can_park:
            msgs2.append(_act(sw_dom + ".turn_off", C["startStop"]))
            if X.get("prevSwitch") == "on":
                X["park"] = {"since": now, "prev": "on", "tries": 1, "nextCheck": now + 30 * 60000, "confirmed": False}
        elif C["method"] == "Mode value" and C["modeEnt"] and C["ecoVals"]:
            opts = attr(C["modeEnt"], "options")
            opts = opts if _truthy(opts) else []
            pm = X.get("prevMode", UNDEFINED)
            if _truthy(pm) and pm in opts:
                back = pm
            else:
                back = next((o for o in opts if low(o) in C["ecoVals"]), UNDEFINED)
                if not _truthy(back):
                    back = C["ecoVals"][0]
            msgs2.append(_act(C["modeEnt"].split(".")[0] + ".select_option", C["modeEnt"], {"option": back}))
        msgs1.append(_act("input_boolean.turn_off", "input_boolean.hesc_plan_owns_charging"))

    def resume_charger(reason: str) -> None:
        if C["shadow"] or not _truthy(X.get("park")):
            return
        msgs2.append(_act(sw_dom + ".turn_on", C["startStop"]))
        hist({"event": "charger_resume", "reason": reason, "soc": soc, "goal": goal})
        X["park"] = None
        X["resume"] = {"tries": 1, "nextCheck": now + 5 * 60000, "reason": reason}

    plan_key = "|".join(_join(P.get(k, UNDEFINED)) for k in ("source", "deadline", "goal", "active"))
    last = X.setdefault("last", {})
    if last.get("planKey", UNDEFINED) != plan_key:
        if "planKey" in last:
            hist({"event": "plan_changed", "source": P.get("source") or None, "deadline": P.get("deadline") or None,
                  "goal": goal, "active": plan_active, "soc": soc})
        last["planKey"] = plan_key
        X["refused"], X["refusedNotified"] = 0, False  # v2.0.1: a new plan gets new start attempts

    def notify(title: str, message: str, prio: int, meta: dict[str, Any] | None = None) -> None:
        p = prio or 1
        services = [x.strip() for x in txt("input_text.hesc_notify_services").split(",")]
        services = [x for x in services if x]
        t = "HESC P" + _s(p) + " · " + title
        flow["hescNoticeP1"] = {"text": title + ": " + message, "at": now, "prio": p,
                                "goal": meta["goal"] if (meta and meta.get("goal") is not None) else None}
        msgs1.append({"payload": {"action": "persistent_notification.create",
                                  "data": {"title": t, "message": message, "notification_id": "hesc_charge_plan"}}})
        if p >= 3:
            return
        for sv in services:
            msgs1.append({"payload": {"action": sv if sv.find(".") > 0 else "notify." + sv,
                                      "data": {"title": t, "message": message,
                                               "data": {"push": {"interruption-level": "time-sensitive"}, "ttl": 0, "priority": "high"} if p == 1 else {}}}})

    if _truthy(X.get("checkDl")) and now >= X["checkDl"] and not _truthy(X.get("checkDone")):
        X["checkDone"] = True
        g = X.get("checkGoal")
        dl_local = datetime.fromtimestamp(X["checkDl"] / 1000, tz)
        when = _WD[dl_local.weekday()] + " " + dl_local.strftime("%H:%M")
        if not ev_conn or soc is None or g is None:
            hist({"event": "goal_unknown", "reason": "EV not connected" if not ev_conn else "no battery level", "soc": soc, "goal": g,
                  "deadline": iso(X["checkDl"])})
            if ev_conn and soc is None and g is not None:
                notify("EV goal not confirmed", when + ": battery level unknown, " + _s(g) + "% not confirmed. Check the car.", 1, {"goal": g})
        elif soc < g - MARGIN:
            notify("EV goal missed", when + ": " + _s(js_round(soc)) + "% instead of " + _s(g) + "%. Check the car.", 1, {"goal": g})
            hist({"event": "goal_missed", "soc": soc, "goal": g, "deadline": iso(X["checkDl"])})
        else:
            hist({"event": "goal_check", "soc": soc, "goal": g, "ok": True, "deadline": iso(X["checkDl"])})
    if plan_active and deadline is not None and _gt(deadline, now) and deadline != X.get("checkDl", UNDEFINED):
        X["checkDl"], X["checkGoal"], X["checkDone"] = deadline, goal, False
    if want and not _truthy(X.get("charging")) and ev_charging:
        want, why = False, "EV already charging, left alone"
    if _or0(X.get("refused")) >= 3 and not _truthy(X.get("refusedNotified")):
        X["refusedNotified"] = True
        notify("Charger refuses to start",
               "The charger did not start 3 times. HESC stops trying for this plan. Check the car and the charger.",
               1, {"goal": goal})
        hist({"event": "start_refused", "rounds": X["refused"], "soc": soc, "goal": goal})
    if want and not _truthy(X.get("charging")):
        start_grid()
        X["charging"], X["since"], X["startAt"], X["startTries"] = True, now, now, 0
        X["drew"] = False
        hist({"event": "grid_start", "reason": why, "soc": soc, "goal": goal, "price": price, "deadline": P.get("deadline") or None})
    elif not want and _truthy(X.get("charging")):
        if ev_conn:
            stop_grid()
        elif not C["shadow"]:
            msgs1.append(_act("input_boolean.turn_off", "input_boolean.hesc_plan_owns_charging"))
        hist({"event": "grid_stop", "reason": why, "soc": soc, "goal": goal, "minutes": js_round((now - X["since"]) / 60000),
              "paused": _truthy(X.get("park"))})
        X["charging"], X["since"] = False, now

    if (_truthy(X.get("charging")) and not C["shadow"] and C["method"] == "Start/stop switch" and C["startStop"]
            and not C["startStop"].startswith("button.") and ev_conn):
        if ev_charging:
            X["startTries"] = 0
        elif (st(C["startStop"]) != "on" and now - (X.get("startAt") or X["since"]) >= 5 * 60000
              and (X.get("startTries") or 0) < 3 and soc is not None and soc < eff_goal - 1):
            X["startTries"] = (X.get("startTries") or 0) + 1
            X["startAt"] = now
            msgs2.append(_act(sw_dom + ".turn_on", C["startStop"]))
            hist({"event": "grid_start_retry", "try": X["startTries"], "soc": soc, "goal": goal})

    if _truthy(X.get("park")) and not _truthy(X.get("charging")) and can_park and not C["shadow"]:
        pk = X["park"]
        if _truthy(pk.get("solar")) and not _truthy(pk.get("backDone")) and now >= pk["backAt"]:
            still_on = ev_charging or st(C["startStop"]) == "on"
            if still_on and (pk.get("offTries") or 0) < 3:
                pk["offTries"] = (pk.get("offTries") or 0) + 1
                pk["backAt"] = now + 60000
                msgs2.append(_act(sw_dom + ".turn_off", C["startStop"]))
                hist({"event": "pause_retry", "attempt": pk["offTries"],
                      "reason": "EV still charging after the pause, pause again before back to solar", "soc": soc, "goal": goal})
            else:
                if still_on:
                    hist({"event": "pause_failed", "attempts": pk.get("offTries") or 0, "reason": "still charging after 3 pauses, back to solar anyway"})
                msgs2.append(_act("button.press" if C["solarBack"].startswith("button.") else C["solarBack"].split(".")[0] + ".turn_on", C["solarBack"]))
                pk["backDone"] = True
                pk["confirmed"] = True
                hist({"event": "charger_to_solar", "reason": "grid charging done, charger back to its own (solar) mode", "soc": soc, "goal": goal})
        sw_state = st(C["startStop"])
        park_goal = goal if (plan_active and goal is not None) else C["fullSoc"]
        if _truthy(pk.get("confirmed")) and sw_state == "on":
            hist({"event": "park_ended", "reason": "switched on by someone else"})
            X["park"] = None
        elif not ev_conn:
            if _truthy(pk.get("solar")):
                hist({"event": "park_ended", "reason": "EV unplugged"})
                X["park"] = None
            else:
                resume_charger("EV unplugged")
        elif sun_go and not _truthy(pk.get("solar")):
            resume_charger("Enough sun to start solar charging")
        elif soc is not None and soc < park_goal - MARGIN and not (plan_active and any(t + 15 * 60000 > now for t in planned)):
            resume_charger("EV more than " + _s(MARGIN) + "% below " + _s(park_goal) + "%")
        elif now >= pk["nextCheck"]:
            if sw_state == "off":
                pk["confirmed"] = True
                pk["nextCheck"] = now + 1e12
            elif pk["tries"] < 3:
                msgs2.append(_act(sw_dom + ".turn_off", C["startStop"]))
                pk["tries"] += 1
                pk["nextCheck"] = now + 30 * 60000
                hist({"event": "pause_retry", "attempt": pk["tries"]})
            else:
                hist({"event": "pause_failed", "attempts": pk["tries"]})
                pk["failed"] = True
                pk["nextCheck"] = now + 1e12
        pk = X.get("park")
        if _truthy(pk) and not _truthy(X.get("charging")) and _truthy(pk.get("solar")):
            why += " · charger back in its own solar mode (grid top-up below " + _s(park_goal - MARGIN) + "%)"
        elif _truthy(pk) and not _truthy(X.get("charging")):
            why += (" · pause refused 3x (charger stays as it is)" if _truthy(pk.get("failed"))
                    else " · charger paused by HESC (on again with sun, below " + _s(park_goal - MARGIN) + "% or a plan)")
    rs = X.get("resume")
    if _truthy(rs) and not C["shadow"] and now >= rs["nextCheck"]:
        if st(C["startStop"]) == "on":
            X["resume"] = None
        elif rs["tries"] < 3:
            msgs2.append(_act(sw_dom + ".turn_on", C["startStop"]))
            rs["tries"] += 1
            rs["nextCheck"] = now + 5 * 60000
            hist({"event": "resume_retry", "attempt": rs["tries"]})
        else:
            hist({"event": "resume_failed", "attempts": rs["tries"], "reason": rs.get("reason", UNDEFINED)})
            notify("Charger fault", "HESC could not switch the charger back on after 3 attempts (" + _s(rs.get("reason", UNDEFINED))
                   + "). The EV may not charge as planned. Please check the charger.", 1)
            X["resume"] = None

    state_txt = ("[shadow] " if C["shadow"] else "") + ("Grid charging · " + why if _truthy(X.get("charging")) else why)
    if last.get("status", UNDEFINED) != state_txt and "input_text.hesc_plan_status" in S:
        last["status"] = state_txt
        msgs1.append(_act("input_text.set_value", "input_text.hesc_plan_status", {"value": state_txt[:255]}))
    flow["hescPlan"] = X
    flow = json.loads(js_json(flow))
    return Result(msgs1, msgs2, msgs3, flow, state_txt[:60])


def _as_list(v: Any) -> list[Any]:
    """[].concat(v || []) for the values v2 meets (lists, or a single item)."""
    if not _truthy(v):
        return []
    return list(v) if isinstance(v, list) else [v]


def _get(r: Any, k: str) -> Any:
    return r.get(k, UNDEFINED) if isinstance(r, dict) else UNDEFINED


def _gt(a: Any, b: float) -> bool:
    return a is not None and a is not UNDEFINED and not (isinstance(a, float) and math.isnan(a)) and a > b


def _le(a: Any, b: float) -> bool:
    return a is not None and a is not UNDEFINED and not (isinstance(a, float) and math.isnan(a)) and a <= b
