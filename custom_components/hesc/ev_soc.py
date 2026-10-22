"""EV battery level with fallbacks, and the notice line on Main.

Line-by-line port of v2.0.0's Node-RED function node "EV battery level (fallbacks)" (every
input round) and of the template "HESC diag EV connected". Order of sources: the battery
sensor from the settings, an automatically found backup sensor of the same car, the last
known level of this plug-in session plus what was charged since, and the usual level at
plug-in over the last 14 days. Proven identical to the original node on random runs
(`tests/integration/test_evsoc_parity.py`).
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from typing import Any

from .inputs import js_parse_float
from .jscompat import UNDEFINED, iso, js_json, js_number_str, js_round, js_to_fixed
from .price_forecast import date_parse

BAD = ("unknown", "unavailable", "none", "")
DAY, H2 = 86400000, 2 * 3600000
EFF = 0.9
_BINARY = re.compile(r"^(binary_sensor|switch|input_boolean)\.")
_OFF_DIAG = "off,disconnected,ready,available,no_ev_connected,unplugged,not_connected,no car,idle,ev disconnected"
_OFF_NODE = "off,disconnected,ready,available,unplugged,not_connected"


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


def _join(v: Any) -> str:
    return "" if v is None or v is UNDEFINED else _s(v)


def _jsnum(v: Any) -> float:
    """JavaScript Number() for the subtraction now - v (null -> 0, missing -> NaN)."""
    if v is None:
        return 0
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        x = js_parse_float(v) if v.strip() else 0
        return math.nan if x is None or str(js_number_str(x)) != v.strip() and v.strip() != "" else x
    return math.nan


def _iso(v: Any) -> str:
    """new Date(v).toISOString() for a millisecond number or a date string."""
    return iso(date_parse(v)) if isinstance(v, str) else iso(v)


def _r1(v: float | None) -> float | None:
    return None if v is None else js_round(v * 10) / 10


def diag_ev_connected(S: dict[str, Any]) -> str:
    """State of v2's template binary_sensor.hesc_diag_ev_connected ('on'/'off')."""
    def states(e: str) -> str:
        return S[e]["state"] if e and e in S else "unknown"

    e = states("input_text.hesc_ev_connected_sensor")
    s = str(states(e))
    dv = states("input_text.hesc_ev_disconnected_values")
    off = (dv if dv not in ("", "unknown", "unavailable") else _OFF_DIAG).lower()
    if e.split(".")[0] in ("binary_sensor", "switch", "input_boolean"):
        res = s == "on"
    else:
        res = s not in ("unknown", "unavailable", "") and s.lower() not in [x.strip() for x in off.split(",")]
    return "on" if res else "off"


@dataclass
class Result:
    save: str | None = None  # ev_soc_plugins.json (None = not written)
    api: list[dict[str, Any]] = field(default_factory=list)  # HA API posts (states, notify)
    flow: dict[str, Any] = field(default_factory=dict)  # changed flow keys
    context: dict[str, Any] = field(default_factory=dict)  # node context
    ran: bool = True


def run(S: dict[str, Any], flow: dict[str, Any], context: dict[str, Any], now: int) -> Result:  # noqa: C901
    """One run of the node. flow: hescSocLog, hescSocState, hescNoticeP1, hescNoticeP3; context: node context."""
    flow = json.loads(js_json(flow)) if flow else {}
    ctx = json.loads(js_json(context)) if context else {}
    res = Result()

    def st(i: Any) -> Any:
        return S[i].get("state") if i and i in S else UNDEFINED

    def attr(i: Any, a: str) -> Any:
        if i and i in S and S[i].get("attributes") is not None:
            return S[i]["attributes"].get(a, UNDEFINED)
        return UNDEFINED

    def num(v: Any) -> float | None:
        return js_parse_float(v)

    def txt(i: str) -> str:
        v = st(i)
        return "" if (v is UNDEFINED or v is None or v in BAD) else _s(v).strip()

    def low(v: Any) -> str:
        return ("" if (v is None or v is UNDEFINED or v == "" or v is False or v == 0) else _s(v)).lower()

    def lst(v: str) -> list[str]:
        return [x.strip() for x in (v or "").split(",") if x.strip()]

    def on(i: str) -> bool:
        return st(i) == "on"

    def pw(i: str) -> float | None:
        v = num(st(i))
        if v is None:
            return None
        u = low(attr(i, "unit_of_measurement"))
        return v * 1000 if u == "kw" else (v * 1e6 if u == "mw" else v)

    def ok(v: Any) -> bool:
        return v is not None and 0 <= v <= 100

    def tms(v: Any) -> float:
        return date_parse(v) if isinstance(v, str) else math.nan

    LOG = flow.get("hescSocLog")
    if not isinstance(LOG, list):
        first = ctx.get("firstTs") or now
        ctx["firstTs"] = first
        if now - first < 60000:
            res.context, res.flow, res.ran = ctx, flow, False
            return res
        LOG = []
        flow["hescSocLog"] = LOG

    main_id = txt("input_text.hesc_ev_soc_sensor")
    b_txt = txt("sensor.hesc_ev_battery_backup_sensor")
    backup_id = b_txt if re.match(r"^sensor\.", b_txt) else ""
    main_name = attr(main_id, "friendly_name")
    main_name = main_name if (main_name not in (None, UNDEFINED, "", 0, False)) else main_id
    backup_name = attr("sensor.hesc_ev_battery_backup_sensor", "device")
    if backup_name in (None, UNDEFINED, "", 0, False):
        backup_name = attr(backup_id, "friendly_name")
        if backup_name in (None, UNDEFINED, "", 0, False):
            backup_name = backup_id
    cap = num(st("input_number.hesc_ev_battery_kwh")) or 60
    active_w = num(st("input_number.hesc_ev_active_w")) or 400
    ev_w = pw(txt("input_text.hesc_ev_power_sensor"))
    charging = ev_w is not None and ev_w > active_w

    diag = st("binary_sensor.hesc_diag_ev_connected")
    if "binary_sensor.hesc_diag_ev_connected" in S and not (diag is UNDEFINED or diag is None or diag in BAD):
        connected = on("binary_sensor.hesc_diag_ev_connected")
    else:
        c_id = txt("input_text.hesc_ev_connected_sensor")
        off = [low(x) for x in lst(txt("input_text.hesc_ev_disconnected_values") or _OFF_NODE)]
        if _BINARY.match(c_id):
            connected = on(c_id)
        else:
            sv = st(c_id)
            connected = bool(c_id) and not (sv is UNDEFINED or sv is None or sv in BAD) and low(sv) not in off

    X = ctx.get("X")
    if not X:
        saved = flow.get("hescSocState")
        if saved and saved.get("X") and now - (saved.get("savedAt") or 0) < 6 * 3600000:
            X = saved["X"]
        else:
            X = {"conn": None, "sess": None}
        if saved and saved.get("P1") and not flow.get("hescNoticeP1") and now - (saved["P1"].get("at") or 0) < 12 * 3600000:
            flow["hescNoticeP1"] = saved["P1"]
    if connected and X.get("conn") is not True:
        X["sess"] = {"start": now, "last": None, "lastAt": None, "kwh": 0, "logged": X.get("conn") is not False, "told": {}}
    if not connected:
        X["sess"] = None
    X["conn"] = connected
    sess = X["sess"]

    last_ts = ctx.get("lastTs") or now
    ctx["lastTs"] = now
    dt_h = min(now - last_ts, 120000) / 3600000
    if sess and ev_w is not None and ev_w > 0:
        sess["kwh"] += ev_w / 1000 * dt_h

    main_v = num(st(main_id)) if main_id else None
    backup_v = num(st(backup_id)) if backup_id else None
    if backup_id and backup_id in S:
        b = S[backup_id]
        lc = b.get("last_changed") or b.get("last_updated") or 0
        b_changed = lc if isinstance(lc, (int, float)) else tms(lc)
    else:
        b_changed = 0
    if backup_v is not None and charging and now - b_changed > H2:
        backup_v = None

    soc, source, src_name, estimated = None, "none", "", False
    if ok(main_v):
        soc, source, src_name = main_v, "main", main_name
    elif ok(backup_v):
        soc, source, src_name = backup_v, "backup", backup_name
    if soc is not None and sess:
        sess["last"], sess["lastAt"], sess["kwh"] = soc, now, 0

    if soc is None and sess and sess.get("last") is not None:
        soc = min(100, sess["last"] + sess["kwh"] * EFF / cap * 100)
        source = "last_known"
        src_name = "last known " + _s(js_round(sess["last"])) + "% + " + js_to_fixed(sess["kwh"], 1) + " kWh charged"
        estimated = True

    recent = [e.get("soc") for e in LOG if isinstance(e, dict) and now - tms(e.get("t")) <= 14 * DAY]
    recent = sorted(v for v in recent if isinstance(v, (int, float)) and not isinstance(v, bool) and ok(v))
    typical = recent[math.floor((len(recent) - 1) * 0.25)] if len(recent) >= 5 else None
    if soc is None and connected and main_id and typical is not None:
        soc, source, src_name, estimated = typical, "typical", "usual level at plug-in (last 14 days)", True

    out1 = None
    if sess and not sess.get("logged"):
        if source in ("main", "backup") and now - sess["start"] <= 15 * 60000:
            LOG.append({"t": iso(now), "soc": js_round(soc * 10) / 10, "src": source})
            cut = now - 60 * DAY
            while LOG and tms(LOG[0].get("t") if isinstance(LOG[0], dict) else None) < cut:
                LOG.pop(0)
            flow["hescSocLog"] = LOG
            out1 = js_json({"version": 1, "plugins": LOG})
            sess["logged"] = True
        elif now - sess["start"] > 15 * 60000:
            sess["logged"] = True

    notice, kind = "", ""
    if main_id and connected:
        if source == "backup":
            notice, kind = "Battery level from " + _s(backup_name) + " (" + _s(main_name) + " missing)", "backup"
        elif source == "last_known":
            notice, kind = "Battery level estimated (no sensor value)", "estimated"
        elif source == "typical":
            notice, kind = "Battery level estimated from usual level (no sensor value)", "estimated"
        elif source == "none":
            notice, kind = "Battery level unknown: plan waits", "unknown"
    msgs: list[dict[str, Any]] = []
    services = [s for s in lst(txt("input_text.hesc_notify_services")) if re.match(r"^notify\.", s)]
    if sess and kind in ("estimated", "unknown") and not sess["told"].get(kind) and now - sess["start"] > 120000:
        sess["told"][kind] = True
        for sv in services:
            msgs.append({"payload": {"protocol": "http", "method": "post", "path": "/api/services/notify/" + sv[7:],
                                     "data": {"title": "HESC P2 · EV battery level", "message": notice}}})
    ctx["X"] = X

    p1now = flow.get("hescNoticeP1")
    if p1now and (not connected or (p1now.get("goal") is not None and source in ("main", "backup") and soc >= p1now["goal"] - 3)):
        flow["hescNoticeP1"] = None

    p1save = flow.get("hescNoticeP1") or None
    s_key = "|".join([_join(connected), _join(sess["start"] if sess else 0),
                      js_json(sess["told"] if sess else {}), js_json(p1save)])
    last_save = ctx.get("lastSave") or 0
    s_now = js_json([sess["last"], js_round(sess["kwh"] * 10)]) if sess else ""
    periodic = bool(sess) and now - last_save >= 300000 and s_now != ctx.get("lastSavedLast", UNDEFINED)
    if out1 or s_key != ctx.get("sKey", UNDEFINED) or periodic:
        ctx["sKey"], ctx["lastSave"], ctx["lastSavedLast"] = s_key, now, s_now
        state_out = {"X": X, "P1": p1save, "savedAt": now}
        flow["hescSocState"] = json.loads(js_json(state_out))
        out1 = js_json({"version": 2, "plugins": LOG, "state": state_out})

    prio = 2 if notice else 0
    notice_at = None
    p1 = flow.get("hescNoticeP1")
    if p1 and now - _jsnum(p1.get("at")) < 12 * 3600000:
        notice, kind, prio, notice_at = p1["text"], "charge_goal", (p1.get("prio") or 1), (p1.get("at") or None)
    p3 = flow.get("hescNoticeP3")
    if not notice and p3 and now - _jsnum(p3.get("at")) < 2 * 3600000:
        notice, kind, prio, notice_at = p3["text"], "advice", 3, (p3.get("at") or None)
    key = "|".join([_join(_r1(soc)), source, notice, _join(notice_at), "v3"])
    last_pub = ctx.get("lastPub") or 0
    if key != ctx.get("lastKey", UNDEFINED) or now - last_pub >= 300000:
        ctx["lastKey"], ctx["lastPub"] = key, now
        msgs.append({"payload": {"protocol": "http", "method": "post", "path": "/api/states/sensor.hesc_ev_soc", "data": {
            "state": "unknown" if soc is None else _s(js_round(soc)),
            "attributes": {
                "friendly_name": "HESC EV battery level", "unit_of_measurement": "%", "device_class": "battery", "icon": "mdi:car-battery",
                "source": source, "source_name": src_name, "estimated": estimated, "exact": _r1(soc),
                "main_sensor": main_id or None, "backup_sensor": backup_id or None,
                "last_known": _r1(sess["last"]) if sess else None,
                "charged_since_kwh": js_round(sess["kwh"] * 100) / 100 if sess else None,
                "typical_at_plugin": typical, "plugins_14d": len(recent), "connected": connected, "updated": iso(now),
            }}}})
        prev_notice = ctx.get("notice") or ""
        if notice_at:
            since = notice_at
        elif notice and notice == prev_notice:
            since = ctx.get("noticeSince") or now
        else:
            since = now
        ctx["notice"], ctx["noticeSince"] = notice, since
        msgs.append({"payload": {"protocol": "http", "method": "post", "path": "/api/states/sensor.hesc_notice", "data": {
            "state": notice[:250] if notice else "none",
            "attributes": {"friendly_name": "HESC notice", "icon": "mdi:alert-circle-outline" if notice else "mdi:check-circle-outline",
                           "kind": kind or None, "prio": prio or None,
                           "link": ("/hesc-v3/charge-plan" if prio == 1 else "/hesc-v3/settings") if notice else None,
                           "since": _iso(since) if notice else None}}}})
    res.save, res.api, res.flow, res.context = out1, msgs, flow, ctx
    return res
