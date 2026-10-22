"""Support report (HTML), on demand.

Line-by-line port of v2.0.0's Node-RED function nodes "Mark generating" (clears "report ready"
and lets one request through per minute), "Build HESC report (HTML)" (history file + live states
+ engine runtime + advice -> report.html and the small launcher page open.html) and "Mark ready"
(sets "report ready" and the generation time once report.html is written). The report runs
outside the evaluation cycle and switches nothing. Proven byte-identical to the original nodes on
random cases (`tests/integration/test_report_parity.py`).

JavaScript semantics are kept on purpose: loose `+`, `<`, `>=` (string concatenation and string
comparison when the history holds texts), Number(), Math.round, toFixed, String(number), JS
truthiness, `undefined`, and the 'nl-NL' / 'sv-SE' date formats in the time zone of
sensor.hesc_prices. Date texts are read like JavaScript's ISO date format (what v2 writes);
other free-form date texts, which V8 would still try to read, count as invalid dates.
"""
from __future__ import annotations

import json
import math
import re
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from .jscompat import UNDEFINED, iso, js_to_fixed
from .report_texts import TEXTS

# Installation-specific texts of v2; v3 can pass its own to build() without touching the port.
VERSION = "v2.0.0"
HISTORY_PATH = "/homeassistant/hesc-data/history.jsonl"  # shown in the report (Runtime)
WEBHOOK_ID = "hesc_report_viewed"  # the report calls /api/webhook/<id> when opened
REPORT_FILE = "/homeassistant/www/hesc/report.html"  # msg.filename of the report
OPEN_FILE = "/homeassistant/www/hesc/open.html"  # msg.filename of the launcher page
REPORT_LINK = "report.html"  # what open.html loads (relative to itself)
DOWNLOAD_PREFIX = "hesc-report-"  # file name of the "Download report" button

READY_ENTITY = "input_boolean.hesc_report_ready"
GENERATED_ENTITY = "input_text.hesc_report_generated"
BUSY_KEY = "hescReportBusy"

# ---------------------------------------------------------------------------------------------
# JavaScript value semantics (private; see the module docstring)

_JS_WS = "\t\n\v\f\r                  　﻿"
_DEC_NUM = re.compile(r"[+-]?(?:Infinity|(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)")
_RADIX = re.compile(r"0([xXbBoO])([0-9a-fA-F]+)")
_ISO = re.compile(
    r"([+-][0-9]{6}|[0-9]{4})(?:-([0-9]{2})(?:-([0-9]{2}))?)?"
    r"(?:T([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\.([0-9]+))?)?(Z|[+-][0-9]{2}:[0-9]{2})?)?")
_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)
_MAX_TIME = 8.64e15


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _truthy(v: Any) -> bool:
    if v is None or v is False or v is UNDEFINED:
        return False
    if _is_num(v):
        return not (v == 0 or math.isnan(v))
    if isinstance(v, str):
        return v != ""
    return True


def _nullish(v: Any) -> bool:
    """v === null || v === undefined"""
    return v is None or v is UNDEFINED


def _seq(v: Any, s: str) -> bool:
    """v === 'text'"""
    return isinstance(v, str) and v == s


def _get(o: Any, k: str) -> Any:
    """o.k: TypeError on null/undefined, undefined for missing keys and non-objects."""
    if o is None or o is UNDEFINED:
        raise TypeError(f"Cannot read properties of {'null' if o is None else 'undefined'} (reading '{k}')")
    if isinstance(o, dict):
        return o.get(k, UNDEFINED)
    return UNDEFINED


def _and(o: Any, k: str) -> Any:
    """o && o.k"""
    return _get(o, k) if _truthy(o) else o


def _or(a: Any, b: Any) -> Any:
    """a || b"""
    return a if _truthy(a) else b


def _num_str(x: Any) -> str:
    """String(number) (Number::toString, radix 10)."""
    x = float(x)
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "Infinity" if x > 0 else "-Infinity"
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    t = Decimal(repr(abs(x))).as_tuple()
    ds = "".join(map(str, t.digits))
    n = len(ds) + int(t.exponent)
    s = ds.rstrip("0")
    k = len(s)
    if k <= n <= 21:
        return sign + s + "0" * (n - k)
    if 0 < n <= 21:
        return sign + s[:n] + "." + s[n:]
    if -6 < n <= 0:
        return sign + "0." + "0" * (-n) + s
    e = n - 1
    es = ("+" if e >= 0 else "-") + str(abs(e))
    return sign + (s if k == 1 else s[0] + "." + s[1:]) + "e" + es


def _str(v: Any) -> str:
    """String(v)"""
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    if _is_num(v):
        return _num_str(v)
    if isinstance(v, (list, tuple)):
        return ",".join("" if _nullish(x) else _str(x) for x in v)
    return "[object Object]"


def _prim(v: Any) -> Any:
    """ToPrimitive: objects and arrays become their text."""
    return _str(v) if isinstance(v, (dict, list, tuple)) else v


def _num(v: Any) -> float:
    """Number(v)"""
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if _is_num(v):
        return float(v)
    if v is None:
        return 0.0
    if v is UNDEFINED:
        return math.nan
    v = _prim(v)
    s = v.strip(_JS_WS)
    if s == "":
        return 0.0
    if _DEC_NUM.fullmatch(s):
        return float(s.replace("Infinity", "inf"))
    m = _RADIX.fullmatch(s)
    if m:
        base = {"x": 16, "b": 2, "o": 8}[m.group(1).lower()]
        try:
            return float(int(m.group(2), base))
        except ValueError:
            return math.nan
        except OverflowError:
            return math.inf
    return math.nan


def _isnan(v: Any) -> bool:
    """global isNaN(v)"""
    return math.isnan(_num(v))


def _add(a: Any, b: Any) -> Any:
    """a + b"""
    a, b = _prim(a), _prim(b)
    if isinstance(a, str) or isinstance(b, str):
        return _str(a) + _str(b)
    return _num(a) + _num(b)


def _cmp(a: Any, op: str, b: Any) -> bool:
    """a < b, a > b, a <= b, a >= b"""
    a, b = _prim(a), _prim(b)
    if isinstance(a, str) and isinstance(b, str):
        x: Any = a.encode("utf-16-be")
        y: Any = b.encode("utf-16-be")
    else:
        x, y = _num(a), _num(b)
        if math.isnan(x) or math.isnan(y):
            return False
    if op == "<":
        return x < y
    if op == ">":
        return x > y
    if op == "<=":
        return x <= y
    return x >= y


def _div(a: float, b: float) -> float:
    """a / b for numbers (no ZeroDivisionError)."""
    if b != 0 or math.isnan(a) or math.isnan(b):
        return a / b
    if a == 0:
        return math.nan
    neg = (a < 0) != (math.copysign(1.0, b) < 0)
    return -math.inf if neg else math.inf


def _round(x: float) -> float:
    """Math.round"""
    x = float(x)
    if not math.isfinite(x) or x == 0 or x == int(x):
        return x
    if 0 < x < 0.5:
        return 0.0
    if -0.5 <= x < 0:
        return -0.0
    f = float(math.floor(x))
    return f + 1 if x - f >= 0.5 else f


def _fixed(x: float, d: int) -> str:
    """x.toFixed(d)"""
    x = float(x)
    if math.isnan(x):
        return "NaN"
    if math.isinf(x) or abs(x) >= 1e21:
        return _num_str(x)
    return js_to_fixed(x, d)


def _utf16_len(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2


def _json_parse(line: str) -> Any:
    """JSON.parse: numbers are doubles; NaN/Infinity are not JSON."""
    def bad(c: str) -> Any:
        raise ValueError(f"Unexpected token {c}")
    return json.loads(line, parse_int=float, parse_constant=bad)


# ---- Date ----

def _parse_date(s: str) -> float:
    """Date.parse for JavaScript's ISO date format (date only: UTC; date-time without offset: local)."""
    m = _ISO.fullmatch(s)
    if not m:
        return math.nan
    ys, mo, d, hh, mi, ss, frac, off = m.groups()
    y = int(ys)
    if ys == "-000000":
        return math.nan
    mo_i, d_i = int(mo or 1), int(d or 1)
    h_i, mi_i, s_i = int(hh or 0), int(mi or 0), int(ss or 0)
    ms_i = int((frac or "0")[:3].ljust(3, "0"))
    if not (1 <= mo_i <= 12 and 1 <= d_i <= 31 and mi_i <= 59 and s_i <= 59):
        return math.nan
    if h_i > 24 or (h_i == 24 and (mi_i or s_i or ms_i)):
        return math.nan
    if not 1 <= y <= 9999:
        raise OverflowError("date outside 1..9999 is not supported")
    local = datetime(y, mo_i, 1) + timedelta(  # noqa: DTZ001 - naive on purpose (UTC or host local time)
        days=d_i - 1, hours=h_i, minutes=mi_i, seconds=s_i, milliseconds=ms_i)
    if hh is not None and off is None:
        t = local.timestamp() * 1000  # host local time, like V8
        return float(round(t))
    t = (local.replace(tzinfo=UTC) - _EPOCH) / timedelta(milliseconds=1)
    if off and off != "Z":
        oh, om = int(off[1:3]), int(off[4:6])
        if oh > 23 or om > 59:
            return math.nan
        t -= (1 if off[0] == "+" else -1) * (oh * 60 + om) * 60000
    return float(t) if abs(t) <= _MAX_TIME else math.nan


def _date_value(v: Any) -> float:
    """The time value of new Date(v) (NaN = Invalid Date)."""
    if v is UNDEFINED:
        return math.nan
    p = _prim(v)
    if isinstance(p, str):
        return _parse_date(p)
    t = _num(p)
    if not math.isfinite(t) or abs(t) > _MAX_TIME:
        return math.nan
    return float(math.trunc(t)) + 0.0


def _local(t: float, tz: str) -> datetime:
    return (_EPOCH + timedelta(milliseconds=int(t))).astimezone(ZoneInfo(tz))


def _nl_short(t: float, tz: str) -> str:
    """toLocaleString('nl-NL', {timeZone, day/month/hour/minute: '2-digit'})"""
    if math.isnan(t):
        return "Invalid Date"
    d = _local(t, tz)
    return f"{d.day:02d}-{d.month:02d}, {d.hour:02d}:{d.minute:02d}"


def _nl_full(t: float, tz: str) -> str:
    """toLocaleString('nl-NL', {timeZone})"""
    if math.isnan(t):
        return "Invalid Date"
    d = _local(t, tz)
    return f"{d.day}-{d.month}-{d.year}, {d.hour:02d}:{d.minute:02d}:{d.second:02d}"


def _nl_time(t: float, tz: str) -> str:
    """toLocaleTimeString('nl-NL', {timeZone})"""
    if math.isnan(t):
        return "Invalid Date"
    d = _local(t, tz)
    return f"{d.hour:02d}:{d.minute:02d}:{d.second:02d}"


def _sv_date(t: float, tz: str) -> str:
    """toLocaleDateString('sv-SE', {timeZone})"""
    if math.isnan(t):
        return "Invalid Date"
    d = _local(t, tz)
    return f"{d.year}-{d.month:02d}-{d.day:02d}"


def _tz_of(S: dict[str, Any]) -> tuple[str, Any]:
    pr = S.get("sensor.hesc_prices")
    pa = _get(pr, "attributes") if _truthy(pr) else UNDEFINED
    pa = pa if _truthy(pa) else {}
    return _or(_get(pa, "tz"), "Europe/Amsterdam"), pa


# ---------------------------------------------------------------------------------------------
# Static page parts (copied from the v2 node)

_CSS = (':root{--bg:#f6f7f9;--card:#fff;--tx:#1d2330;--mut:#667085;--ln:#e3e6ea;--ac:#1f7ae0;--ok:#2e9e5b;--wr:#d9822b;--bad:#d64545}'
        '@media (prefers-color-scheme: dark){:root{--bg:#15181e;--card:#1e2128;--tx:#e8eaed;--mut:#9aa0a6;--ln:#333744;--ac:#42a5f5;--ok:#66bb6a;--wr:#ffa726;--bad:#ef5350}}'
        '*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}'
        '.wrap{max-width:1100px;margin:0 auto;padding:16px}h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:24px 0 8px}'
        '.sub{color:var(--mut);font-size:13px}.box{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:14px;margin-top:10px;overflow-x:auto}'
        '.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:12px}.kpi{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:12px}'
        '.kl{font-size:11px;letter-spacing:.6px;color:var(--mut)}.kb{font-size:24px;font-weight:650;margin-top:2px}.ks{font-size:12px;color:var(--mut)}'
        'table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:var(--mut);font-weight:600;padding:6px 8px;border-bottom:1px solid var(--ln);white-space:nowrap}td{padding:6px 8px;border-bottom:1px solid var(--ln);vertical-align:top}'
        '.chip{display:inline-block;font-size:11px;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle}.chip.adv{background:#1f7ae022;color:var(--ac)}.chip.ok{background:#2e9e5b22;color:var(--ok)}.chip.wait{background:#66708522;color:var(--mut)}.adv-item{padding:8px 0;border-bottom:1px solid var(--ln)}.adv-item:last-child{border-bottom:0}.adv-item div{margin-top:2px}'
        '.mut{color:var(--mut)}.up{color:var(--ok)}.dn{color:var(--wr)}.warn{color:var(--bad);font-weight:600}code{font-size:12px}'
        '.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;border:1px solid var(--ln);margin-right:6px}'
        '.bar{display:flex;align-items:center;gap:8px;margin:4px 0}.bl{width:80px;text-align:right;color:var(--mut);font-size:12px}.bt{flex:1;height:12px;background:var(--ln);border-radius:4px;overflow:hidden}.bf{display:block;height:12px;background:var(--ac)}.bv{width:30px;font-size:12px}')

# Report layout in the same structure as the HPVC report
_CSS2 = (':root{color-scheme:dark;--bg:#0a121a;--card:#15222e;--tx:#f2f5f8;--mut:#93a3af;--ln:#2a3a48;--ac:#18b9df;--ok:#54d36b;--wr:#f3c44f;--bad:#ef5350}'
         'body{background:radial-gradient(circle at 50% 0,#13212f,#0a121a 60%) fixed;color:var(--tx)}'
         '.wrap{max-width:1220px;padding:28px}'
         '.top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.top h1{margin:0;font-size:27px}.meta{color:var(--mut);margin-top:4px}'
         '.dl{border:0;border-radius:10px;background:var(--ac);color:#fff;font-weight:800;padding:12px 17px;cursor:pointer;font-size:14px}'
         'nav{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 26px}nav a{color:var(--tx);text-decoration:none;background:#152633;border:1px solid var(--ln);border-radius:999px;padding:7px 12px}nav a:hover{border-color:var(--ac)}'
         'section{margin:0 0 26px;scroll-margin-top:12px}h2{font-size:17px;margin:0 0 10px}'
         '.box,.kpi,.panel{background:linear-gradient(180deg,#172836,#111e29);border:1px solid var(--ln);border-radius:12px}'
         '.panel{overflow:hidden}.kvr{display:flex;justify-content:space-between;gap:16px;padding:12px 16px;border-top:1px solid var(--ln)}.kvr:first-child{border-top:0}.kvr span{color:var(--mut)}.kvr b{text-align:right}'
         '.kb{font-size:22px}.lead{color:var(--mut);font-style:italic;font-size:13px;margin-top:4px}'
         'details.compact{background:linear-gradient(180deg,#172836,#111e29);border:1px solid var(--ln);border-radius:12px;padding:0}details.compact>summary{cursor:pointer;padding:12px 16px;font-weight:700;list-style:none}details.compact>summary::before{content:"\\25B8  ";color:var(--ac)}details.compact[open]>summary::before{content:"\\25BE  "}details.compact>.box{border:0;border-top:1px solid var(--ln);border-radius:0;margin:0;background:none}'
         '#live .kpis{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}'
         '#settings td{padding:10px 14px}#settings td:first-child{color:var(--mut)}#settings td:last-child{text-align:right;font-weight:700}#settings code{font:inherit}'
         '@media (max-width:640px){.wrap{padding:16px}.top{flex-direction:column}}')

_SET_IDS = ['input_boolean.hesc_enabled', 'input_boolean.hesc_shadow_mode', 'input_boolean.hesc_use_irradiance', 'input_boolean.hesc_owns_hpvc_off',
            'input_text.hesc_forecast_now_sensor', 'input_text.hesc_forecast_30m_sensor', 'input_text.hesc_forecast_attribute', 'input_text.hesc_irradiance_sensor', 'input_text.hesc_pv_power_sensor', 'input_text.hesc_grid_power_sensor',
            'input_text.hesc_ev_connected_sensor', 'input_text.hesc_ev_power_sensor', 'input_text.hesc_ev_green_energy_sensor', 'input_text.hesc_charger_mode_entity', 'input_text.hesc_charger_eco_value', 'input_text.hesc_charger_solar_switch_entity', 'input_text.hesc_ev_disconnected_values', 'input_text.hesc_hpvc_enabled_entity', 'input_text.hesc_hpvc_limited_entity',
            'input_number.hesc_p_start', 'input_number.hesc_p_hold', 'input_number.hesc_irr_start', 'input_number.hesc_irr_hold', 'input_number.hesc_ev_active_w',
            'input_number.hesc_t_stable', 'input_number.hesc_t_start', 'input_number.hesc_t_dip', 'input_number.hesc_t_stop', 'input_number.hesc_t_max', 'input_number.hesc_cooldown', 'input_number.hesc_max_attempts']

_BINS = [(0, 50, '< 50%'), (50, 80, '50–80%'), (80, 100, '80–100%'), (100, 120, '100–120%'), (120, 150, '120–150%'), (150, 1e9, '> 150%')]
_CHIP = {'advice': '<span class="chip adv">advice</span>', 'ok': '<span class="chip ok">fits</span>',
         'waiting': '<span class="chip wait">collecting data</span>', 'info': '<span class="chip wait">good to know</span>'}
_NAV = [('summary', 'Status'), ('live', 'Live'), ('advice', 'Advice'), ('accuracy', 'Accuracy'), ('sources', 'Sources'), ('days', 'Days'),
        ('sessions', 'Sessions'), ('events', 'Events'), ('settings', 'Settings'), ('runtime', 'Runtime')]
_HESC_NAME = re.compile(r"<td>HESC (\w)", re.ASCII)


def _lang_code(lang: str | None) -> str:
    """Base language code with report texts (nl, de), else 'en'."""
    code = str(lang or "en").split("-")[0].split("_")[0].lower()
    return code if code in TEXTS else "en"


def _tr(lang: str | None) -> Any:
    """Text lookup for the report language (nl, de); English and unknown languages keep v2's texts."""
    tab = TEXTS.get(_lang_code(lang), {})
    return lambda text: tab.get(text, text)


def open_page(report_link: str = REPORT_LINK, lang: str = "en") -> str:
    """The launcher page (open.html): /local files are cached by the browser for a month, so the
    dashboard opens open.html, which loads the report with a unique query string."""
    T = _tr(lang)
    return ('<!doctype html><html><head><meta charset="utf-8"><title>' + T('HESC report') + '</title><meta name="viewport" content="width=device-width,initial-scale=1"></head>'
            '<body style="background:#0a121a;color:#ccc;font-family:sans-serif">' + T('Opening HESC report…') + '<script>location.replace("'
            + report_link + '?t="+Date.now());</script></body></html>')


# ---------------------------------------------------------------------------------------------

def mark_generating(flow: dict[str, Any], now_ms: int) -> tuple[dict[str, Any] | None, bool, dict[str, Any], str | None]:
    """v2 "Mark generating": (output 1: turn "report ready" off, or None; proceed = output 2 (read the
    history and build); flow; node status or None). One request per minute while busy."""
    flow = dict(flow)
    busy = flow.get(BUSY_KEY, UNDEFINED)
    if _truthy(busy) and now_ms - _num(busy) < 60000:
        return None, False, flow, 'already generating'
    flow[BUSY_KEY] = now_ms
    return {'payload': {'action': 'input_boolean.turn_off', 'target': {'entity_id': [READY_ENTITY]}, 'data': {}}}, True, flow, None


def mark_ready(flow: dict[str, Any], S: dict[str, Any], now_ms: int, is_open: bool) -> tuple[list[dict[str, Any]] | None, dict[str, Any], str | None]:
    """v2 "Mark ready", after a file was written: (actions or None, flow, node status or None).
    is_open: the file written was the launcher page (msg.hescOpen), which marks nothing."""
    flow = dict(flow)
    if is_open:
        return None, flow, None
    tz, _pa = _tz_of(S or {})
    flow[BUSY_KEY] = 0
    t = _nl_full(float(now_ms), _str(tz))
    return [
        {'payload': {'action': 'input_boolean.turn_on', 'target': {'entity_id': [READY_ENTITY]}, 'data': {}}},
        {'payload': {'action': 'input_text.set_value', 'target': {'entity_id': [GENERATED_ENTITY]}, 'data': {'value': t}}},
    ], flow, 'ready ' + t


def build(S: dict[str, Any] | None, runtime: dict[str, Any] | None, advice: dict[str, Any] | None, history_text: str, now_ms: int,
          *, global_advice: dict[str, Any] | None = None, version: str = VERSION, history_path: str = HISTORY_PATH,
          webhook_id: str = WEBHOOK_ID, report_link: str = REPORT_LINK, download_prefix: str = DOWNLOAD_PREFIX,
          lang: str = "en") -> tuple[str, str, str]:
    """v2 "Build HESC report (HTML)": (report html, launcher page html, node status).

    S: HA states as the node sees them; runtime: global hescRuntime; advice: msg.advice (from the
    Advisor); global_advice: global hescAdvice, used when msg.advice is missing (`msg.advice ||
    global.get('hescAdvice')`); history_text: contents of the history file ('' if missing)."""
    T = _tr(lang)  # report language; English is v2's text unchanged
    S = S if _truthy(S) else {}
    tz_v, pa = _tz_of(S)
    tz = _str(tz_v)
    dec = '.' if _seq(_get(pa, 'decimal'), '.') else ','
    RT = runtime if _truthy(runtime) else None
    now = float(now_ms)

    def esc(v: Any) -> str:
        return _str('–' if _nullish(v) else v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def ent(i: Any) -> Any:
        return S.get(_str(i), UNDEFINED)

    def st(i: Any) -> Any:
        return _get(ent(i), 'state') if _truthy(i) and _truthy(ent(i)) else UNDEFINED

    def round_v(v: Any) -> Any:
        if _seq(v, '') or _nullish(v):
            return v
        x = _num(v)
        return _num_str(_round(x)) if math.isfinite(x) else v

    def fmt_t(v: Any) -> str:
        try:
            return _nl_short(_date_value(v), tz)
        except (KeyError, ValueError):  # unknown time zone (RangeError in JS)
            return _str(v)

    def day_of(v: Any) -> str:
        return _sv_date(_date_value(v), tz)

    def kwh(wh: Any) -> str:
        if _nullish(wh) or _isnan(wh):
            return '–'
        return _fixed(_num(wh) / 1000, 2).replace('.', dec, 1)

    def pct(v: Any) -> str:
        if _nullish(v) or _isnan(v):
            return '–'
        return _num_str(_round(_num(v))) + '%'

    def qn(a: list[Any], p: float) -> Any:
        s = sorted((x for x in a if not _nullish(x) and not _isnan(x)), key=_num)
        if not s:
            return None
        return s[min(len(s) - 1, max(0, int(_round(p * (len(s) - 1)))))]

    # ---- parse history ----
    raw = history_text if isinstance(history_text, str) else ''
    rows: list[Any] = []
    bad = 0
    for line in raw.split('\n'):
        if not line.strip(_JS_WS):
            continue
        try:
            rows.append(_json_parse(line))
        except ValueError:
            bad += 1
    sessions = [r for r in rows if _seq(_get(r, 'type'), 'release') or _seq(_get(r, 'type'), 'eco_charge')]
    releases = [r for r in rows if _seq(_get(r, 'type'), 'release')]
    # A solar-mode session that starts while there is hardly any sun (forecast AND PV below the hold
    # threshold) was started by hand or by a schedule: logged, but left out of advice and accuracy.
    hold_x = _num(st('input_number.hesc_p_hold'))
    HOLD = hold_x if _truthy(hold_x) else 2000

    def is_forced(r: Any) -> bool:
        fs = _get(r, 'forced_start')
        if fs is True:
            return True
        if fs is not UNDEFINED:
            return False
        sc = _get(r, 'start_ctx')
        if not _truthy(sc):
            return False
        fc, pv = _get(sc, 'fc_now'), _get(sc, 'pv')
        return _is_num(fc) and _is_num(pv) and fc < HOLD and pv < HOLD

    forced_count = len([r for r in rows if _seq(_get(r, 'type'), 'eco_charge') and is_forced(r)])
    eco = [r for r in rows if _seq(_get(r, 'type'), 'eco_charge') and not is_forced(r)]
    events = [r for r in rows if _seq(_get(r, 'type'), 'event')]
    first = _get(rows[0], 'ts') if rows else None

    # ---- summary (patterns first) ----
    def total(a: list[Any], f: str) -> float:
        s = 0.0
        for r in a:
            x = _num(_get(r, f))
            s = s + (x if _truthy(x) else 0)
        return s

    eco_fc, eco_pv, eco_ev = total(eco, 'forecast_wh'), total(eco, 'pv_wh'), total(eco, 'ev_wh')
    eco_green = 0.0
    for r in eco:
        g = _get(r, 'ev_green_kwh')
        eco_green = eco_green + (0 if _nullish(g) else _num(g))
    acc_list = [_get(r, 'actual_vs_forecast_pct') for r in eco if _cmp(_get(r, 'minutes'), '>=', 10)]
    rel_ok = len([r for r in releases if _truthy(_get(r, 'ev_started'))])
    rel_shadow = len([r for r in releases if _truthy(_get(r, 'shadow'))])

    # ---- per day, newest first, trend first ----
    D: dict[str, dict[str, Any]] = {}

    def day_rec(k: str) -> dict[str, Any]:
        if k not in D:
            D[k] = {'n': 0, 'fc': 0, 'pv': 0, 'ev': 0, 'green': 0, 'rel': 0, 'relOk': 0}
        return D[k]

    for r in eco:
        d = day_rec(day_of(_or(_get(r, 'start'), _get(r, 'ts'))))
        d['n'] += 1
        d['fc'] = _add(d['fc'], _or(_get(r, 'forecast_wh'), 0))
        d['pv'] = _add(d['pv'], _or(_get(r, 'pv_wh'), 0))
        d['ev'] = _add(d['ev'], _or(_get(r, 'ev_wh'), 0))
        d['green'] = _add(d['green'], _or(_num(_get(r, 'ev_green_kwh')), 0))
    for r in releases:
        d = day_rec(day_of(_or(_get(r, 'start'), _get(r, 'ts'))))
        d['rel'] += 1
        if _truthy(_get(r, 'ev_started')):
            d['relOk'] += 1
    days = sorted(D, key=lambda k: k.encode('utf-16-be'), reverse=True)

    def day_acc(k: str) -> float | None:
        return _div(100 * _num(D[k]['pv']), _num(D[k]['fc'])) if _cmp(D[k]['fc'], '>', 0) else None

    day_rows = ''
    for i, k in enumerate(days[:31]):
        cur = day_acc(k)
        old = day_acc(days[i + 1]) if i + 1 < len(days) else None
        tr = '<span class="mut">–</span>'
        if cur is not None and old is not None:
            dd = cur - old
            tr = '<span class="mut">→</span>' if abs(dd) < 5 else ('<span class="up">↑</span>' if dd > 0 else '<span class="dn">↓</span>')
        Dk = D[k]
        day_rows += ('<tr><td>' + esc(k) + '</td><td>' + tr + '</td><td>' + _str(Dk['n']) + '</td><td>' + kwh(Dk['fc']) + '</td><td>' + kwh(Dk['pv'])
                     + '</td><td><b>' + pct(cur) + '</b></td><td>' + kwh(Dk['ev']) + '</td><td>' + _fixed(Dk['green'], 2).replace('.', dec, 1)
                     + '</td><td>' + (_str(Dk['relOk']) + '/' + _str(Dk['rel']) if Dk['rel'] else '–') + '</td></tr>')

    # ---- accuracy distribution ----
    bn = [len([x for x in acc_list if x is not None and _cmp(x, '>=', b[0]) and _cmp(x, '<', b[1])]) for b in _BINS]
    bmax = max(1, *bn)
    dist_rows = ''
    for i, b in enumerate(_BINS):
        dist_rows += ('<div class="bar"><span class="bl">' + b[2] + '</span><span class="bt"><span class="bf" style="width:'
                      + _num_str(_round(100 * bn[i] / bmax)) + '%"></span></span><span class="bv">' + _str(bn[i]) + '</span></div>')

    # v0.5.2: optional EV battery level at start → end
    def soc_txt(r: Any) -> str:
        sc, ec = _get(r, 'start_ctx'), _get(r, 'end_ctx')
        a = _get(sc, 'ev_soc') if _truthy(sc) and _is_num(_get(sc, 'ev_soc')) else None
        b = _get(ec, 'ev_soc') if _truthy(ec) and _is_num(_get(ec, 'ev_soc')) else None
        if a is None and b is None:
            return ''
        return (' <span class="mut">(' + T('EV') + ' ' + ('?' if a is None else _num_str(_round(a))) + '→'
                + ('?' if b is None else _num_str(_round(b))) + '%)</span>')

    # ---- sessions, newest first ----
    sess_rows = ''
    for r in list(reversed(sessions))[:40]:
        if _seq(_get(r, 'type'), 'release'):
            kind = T('Release') + (T(' (shadow)') if _truthy(_get(r, 'shadow')) else '')
        else:
            kind = T('Manual/scheduled (not counted)') if is_forced(r) else T('Solar charge')
        g = _get(r, 'ev_green_kwh')
        sess_rows += ('<tr><td>' + fmt_t(_or(_get(r, 'start'), _get(r, 'ts'))) + '</td><td>' + kind + '</td><td>' + esc(_get(r, 'minutes'))
                      + '</td><td>' + kwh(_get(r, 'forecast_wh')) + '</td><td>' + kwh(_get(r, 'pv_wh')) + '</td><td><b>' + pct(_get(r, 'actual_vs_forecast_pct'))
                      + '</b></td><td>' + kwh(_get(r, 'ev_wh')) + '</td><td>' + ('–' if _nullish(g) else _str(g).replace('.', dec, 1))
                      + '</td><td>' + ((T('yes') if _truthy(_get(r, 'ev_started')) else T('no')) if _seq(_get(r, 'type'), 'release') else '–')
                      + '</td><td>' + esc(_get(r, 'reason')) + soc_txt(r) + '</td></tr>')
    ev_rows = ''
    for r in list(reversed(events))[:30]:
        ctx = _get(r, 'ctx')
        ev_rows += ('<tr><td>' + fmt_t(_get(r, 'ts')) + '</td><td>' + esc(_get(r, 'text')) + (' <span class="mut">' + T('(shadow)') + '</span>' if _truthy(_get(r, 'shadow')) else '')
                    + '</td><td>' + esc(_and(ctx, 'fc_now')) + ' W</td><td>' + esc(_and(ctx, 'irr')) + '</td><td>' + esc(_and(ctx, 'pv')) + ' W</td></tr>')

    # ---- settings & live ----
    set_rows = ''
    for i in _SET_IDS:
        e = ent(i)
        unit = _and(_and(e, 'attributes'), 'unit_of_measurement')
        u = ' ' + _str(unit) if _truthy(unit) else ''
        set_rows += '<tr><td>' + esc(_or(_and(_and(e, 'attributes'), 'friendly_name'), i)) + '</td><td><code>' + esc(round_v(st(i))) + u + '</code></td></tr>'

    def src(i: str) -> Any:
        return st('input_text.' + i)

    fc_attr = st('input_text.hesc_forecast_attribute')

    def live_val(eid: Any, a: Any = UNDEFINED) -> Any:
        if not _truthy(eid) or not _truthy(ent(eid)):
            return 'missing'
        if _truthy(a):
            attrs = _get(ent(eid), 'attributes')
            return _get(attrs, _str(a)) if _truthy(attrs) else 'missing'
        return _get(ent(eid), 'state')

    fa = ' (' + _str(fc_attr) + ')' if _truthy(fc_attr) else ''
    live = [
        (T('Forecast now') + fa, live_val(src('hesc_forecast_now_sensor'), fc_attr), 'W'),
        (T('Forecast +30 min') + fa, live_val(src('hesc_forecast_30m_sensor'), fc_attr), 'W'),
        (T('Irradiance'), live_val(src('hesc_irradiance_sensor')), 'W/m²'),
        (T('PV power'), live_val(src('hesc_pv_power_sensor')), 'W'),
        (T('Grid power'), live_val(src('hesc_grid_power_sensor')), 'W'),
        (T('EV connected'), live_val(src('hesc_ev_connected_sensor')), ''),
        (T('EV charging power'), live_val(src('hesc_ev_power_sensor')), 'W'),
        (T('Charger mode'), live_val(src('hesc_charger_mode_entity')), ''),
        (T('HPVC enabled'), live_val(src('hesc_hpvc_enabled_entity')), ''),
        (T('HPVC limiting'), live_val(src('hesc_hpvc_limited_entity')), ''),
    ]
    live_rows = ''
    issues: list[str] = []
    for n, v, u in live:
        ok = not (_nullish(v) or (isinstance(v, str) and v in ('missing', 'unknown', 'unavailable', '')))
        if not ok and not (n == T('Irradiance') and not _truthy(src('hesc_irradiance_sensor'))):
            issues.append(n)
        live_rows += ('<tr><td>' + esc(n) + '</td><td class="' + ('' if ok else 'warn') + '">' + esc(T(v) if _seq(v, 'missing') else (round_v(v) if u else v))
                      + (' ' + u if ok and u else '') + '</td></tr>')
    if bad:
        issues.append(_str(bad) + T(' unreadable history line(s)'))

    # Plain-language summary of the engine's day counters (instead of raw JSON).
    def today_text(d: Any) -> str:
        if not _truthy(d):
            return '–'

        def n(v: Any) -> float:
            x = _num(v)
            return x if math.isfinite(x) else 0

        rel = n(_get(d, 'releases'))
        eco_n = n(_get(d, 'ecoSessions'))
        forced_n = n(_get(d, 'forcedSessions'))
        return (_num_str(eco_n) + ' ' + T('solar session' if eco_n == 1 else 'solar sessions')
                + (' · ' + _num_str(forced_n) + T(' manual/scheduled (not counted)') if _truthy(forced_n) else '')
                + ' · ' + _num_str(rel) + ' ' + T('release' if rel == 1 else 'releases')
                + (' (' + _num_str(n(_get(d, 'success'))) + T(' ok, ') + _num_str(n(_get(d, 'failed'))) + T(' failed)') if _truthy(rel) else '')
                + T('<br>During solar charging only: forecast ') + kwh(_get(d, 'fcWh')) + T(' kWh · actual PV ') + kwh(_get(d, 'pvWh'))
                + T(' kWh · EV charged ') + kwh(_get(d, 'evWh')) + T(' kWh, of which ') + _fixed(n(_get(d, 'greenKwh')), 2).replace('.', dec, 1) + T(' kWh from solar'))

    shadow = not _seq(st('input_boolean.hesc_shadow_mode'), 'off')

    def card(label: str, big: str, sub: str, cls: str = '') -> str:
        return '<div class="kpi"><div class="kl">' + label + '</div><div class="kb ' + cls + '">' + big + '</div><div class="ks">' + sub + '</div></div>'

    kpis = (card(T('SOLAR SESSIONS'), _str(len(eco)), T('since ') + (fmt_t(first) if _truthy(first) else '–')
                 + (' · ' + _str(forced_count) + T(' manual/scheduled not counted') if forced_count else ''))
            + card(T('ACTUAL PV VS FORECAST'), pct(_div(100 * eco_pv, eco_fc) if eco_fc > 0 else None), T('while charging in solar mode · median per session ') + pct(qn(acc_list, 0.5)))
            + card(T('EV ENERGY'), kwh(eco_ev) + ' kWh', _fixed(eco_green, 1).replace('.', dec, 1) + T(' kWh from solar (charger)'))
            + card(T('RELEASES'), _str(rel_ok) + ' / ' + _str(len(releases)), T('EV started / attempts') + (' · ' + _str(rel_shadow) + T(' in shadow') if rel_shadow else '')))

    # ---- advice (from the Advisor node; plain language, advice only) ----
    ADV = advice if _truthy(advice) else (global_advice if _truthy(global_advice) else None)
    adv_html = ''
    if ADV is not None:
        items = _get(ADV, 'items')
        if not isinstance(items, list):
            raise TypeError('ADV.items.map is not a function')
        changed = _get(ADV, 'changed')
        parts = []
        for it in items:
            chip = _CHIP.get(_str(_get(it, 'status')), '')
            for word in ('advice', 'fits', 'collecting data', 'good to know'):
                chip = chip.replace('>' + word + '<', '>' + T(word) + '<')
            parts.append('<div class="adv-item"><div class="adv-t"><b>' + esc(_get(it, 'title')) + '</b> ' + chip + '</div><div class="mut">' + T('Measured: ')
                         + esc(_get(it, 'measured')) + '</div><div>' + esc(_get(it, 'advice')) + '</div></div>')
        adv_html = ('<h2>' + T('Advice') + '</h2><div class="sub">' + T('Based on the last ') + _str(_get(ADV, 'window_days'))
                    + T(' days. Recalculated daily, so it can change with the seasons. HESC never changes a setting itself; you decide.') + '</div>'
                    + ('<div class="box warn">' + esc(changed) + '</div>' if _truthy(changed) else '') + '<div class="box">' + ''.join(parts) + '</div>')

    # ---- source reliability (15-min daylight intervals, not curtailed by HPVC) ----
    acc_rows = [x for x in rows if _seq(_get(x, 'type'), 'accuracy') and _cmp(_or(_get(x, 'hpvc_limited_share'), 0), '<', 0.1) and _cmp(_get(x, 'fc_w'), '>', 50)]

    def rel_of(a: list[Any]) -> dict[str, Any]:
        ratio = [_div(100 * _num(_get(x, 'pv_w')), _num(_get(x, 'fc_w'))) for x in a]
        within = _round(100 * len([x for x in a if abs(_num(_get(x, 'pv_w')) - _num(_get(x, 'fc_w'))) <= 0.2 * _num(_get(x, 'fc_w'))]) / len(a)) if a else None
        e10 = [x for x in a if not _nullish(_get(x, 'fc10_w'))]
        e10ok = _round(100 * len([x for x in e10 if _cmp(_get(x, 'pv_w'), '>=', _get(x, 'fc10_w'))]) / len(e10)) if e10 else None
        irr = [x for x in a if not _nullish(_get(x, 'irr_wm2')) and _cmp(_get(x, 'irr_wm2'), '>', 50)]
        kpv = [_div(_num(_get(x, 'pv_w')), _num(_get(x, 'irr_wm2')) / 1000) for x in irr]
        corr = None
        if len(irr) >= 5:
            xs = [_get(x, 'irr_wm2') for x in irr]
            ys = [_get(x, 'pv_w') for x in irr]
            sx: Any = 0
            for v in xs:
                sx = _add(sx, v)
            sy: Any = 0
            for v in ys:
                sy = _add(sy, v)
            mx, my = _num(sx) / len(xs), _num(sy) / len(ys)
            sxy = sxx = syy = 0.0
            for i in range(len(xs)):
                dx, dy = _num(xs[i]) - mx, _num(ys[i]) - my
                sxy += dx * dy
                sxx += dx * dx
                syy += dy * dy
            corr = _div(sxy, math.sqrt(sxx * syy)) if (sxx > 0 and syy > 0) else None
        return {'n': len(a), 'med': qn(ratio, 0.5), 'within': within, 'e10ok': e10ok, 'nIrr': len(irr),
                'kpvMed': qn(kpv, 0.5), 'kpvP25': qn(kpv, 0.25), 'kpvP75': qn(kpv, 0.75), 'corr': corr}

    RA = rel_of(acc_rows)
    RD: dict[str, list[Any]] = {}
    for x in acc_rows:
        RD.setdefault(day_of(_get(x, 'slot_start')), []).append(x)
    rdays = sorted(RD, key=lambda k: k.encode('utf-16-be'), reverse=True)
    rel_rows = ''
    for i, k in enumerate(rdays[:31]):
        cur_r = rel_of(RD[k])
        old_r = rel_of(RD[rdays[i + 1]]) if i + 1 < len(rdays) else None
        tr = '<span class="mut">–</span>'
        if old_r is not None and cur_r['med'] is not None and old_r['med'] is not None:
            dd = abs(cur_r['med'] - 100) - abs(old_r['med'] - 100)
            tr = '<span class="mut">→</span>' if abs(dd) < 5 else ('<span class="up">' + T('↑ better') + '</span>' if dd < 0 else '<span class="dn">' + T('↓ worse') + '</span>')
        rel_rows += ('<tr><td>' + esc(k) + '</td><td>' + tr + '</td><td>' + _str(cur_r['n']) + '</td><td><b>' + pct(cur_r['med']) + '</b></td><td>'
                     + pct(cur_r['within']) + '</td><td>' + pct(cur_r['e10ok']) + '</td><td>' + ('–' if cur_r['kpvMed'] is None else _num_str(_round(cur_r['kpvMed'])))
                     + '</td><td>' + ('–' if cur_r['corr'] is None else _fixed(cur_r['corr'], 2).replace('.', dec, 1)) + '</td></tr>')
    if not _truthy(st('input_text.hesc_irradiance_sensor')) or not _seq(st('input_boolean.hesc_use_irradiance'), 'on'):
        irr_card = card(T('IRRADIANCE → PV'), T('off'), T('local weather station off (optional)'))
    elif RA['nIrr'] == 0:
        irr_card = card(T('IRRADIANCE → PV'), '–', T('not enough intervals above 50 W/m² yet'))
    else:
        irr_card = card(T('IRRADIANCE → PV'), '–' if RA['kpvMed'] is None else _num_str(_round(RA['kpvMed'])) + ' W',
                        T('PV per 1 kW/m² · middle half ') + ('–' if RA['kpvP25'] is None else _num_str(_round(RA['kpvP25'])) + '–' + _num_str(_round(RA['kpvP75'])))
                        + T(' · correlation ') + ('–' if RA['corr'] is None else _fixed(RA['corr'], 2).replace('.', dec, 1)))
    rel_kpis = (card(T('FORECAST (MEDIAN) VS ACTUAL'), pct(RA['med']), T('actual as % of forecast · ') + _str(RA['n']) + T(' intervals of 15 min'))
                + card(T('WITHIN ±20%'), pct(RA['within']), T('share of intervals where actual was close to the forecast'))
                + card(T('CAUTIOUS FORECAST HELD'), pct(RA['e10ok']), T('actual ≥ cautious estimate (ideal ≈ 90%)'))
                + irr_card)

    def kv(pairs: list[tuple[str, str]]) -> str:
        return '<div class="panel">' + ''.join('<div class="kvr"><span>' + p[0] + '</span><b>' + p[1] + '</b></div>' for p in pairs) + '</div>'

    def n_or(v: Any) -> float | None:
        x = _num(v)
        return _round(x) if math.isfinite(x) else None

    def time_iso(v: Any) -> float:
        """new Date(v).toISOString() (RangeError on an invalid date), as a time value."""
        t = _date_value(v)
        if math.isnan(t):
            raise ValueError('Invalid time value')
        return t

    def fmt_ms(t: float) -> str:
        try:
            return _nl_short(t, tz)
        except (KeyError, ValueError):
            return iso(t)

    # Executive summary
    hpvc_on = live_val(src('hesc_hpvc_enabled_entity'))
    hpvc_lim = live_val(src('hesc_hpvc_limited_entity'))
    rt_since = _and(RT, 'since') if RT is not None else None
    since_txt = esc(fmt_ms(time_iso(rt_since)) if _truthy(rt_since) else '–')
    last_action = st('input_text.hesc_last_action')
    summary = kv([
        (T('HESC status'), T('Disabled') if _seq(st('input_boolean.hesc_enabled'), 'off') else T('Enabled')),
        (T('Configuration'), '<span style="color:var(--wr)">' + T('Attention: ') + esc(', '.join(issues)) + '</span>' if issues else T('Valid')),
        (T('Mode'), T('Shadow — evaluates only') if shadow else T('Live — asks HPVC for releases')),
        (T('Current state'), esc(_or(st('input_text.hesc_state'), '–'))),
        (T('Reason'), esc(_or(st('input_text.hesc_reason'), '–'))),
        (T('Status since'), since_txt),
        (T('Last action'), T('None yet') if (not _truthy(last_action) or _seq(last_action, 'unknown') or _seq(last_action, 'unavailable')) else esc(last_action)),
        ('HPVC', (T('On') if _seq(hpvc_on, 'on') else T('Off') if _seq(hpvc_on, 'off') else esc(T(hpvc_on) if _seq(hpvc_on, 'missing') else hpvc_on)) + ' · ' + (T('limiting PV') if _seq(hpvc_lim, 'on') else T('not limiting'))),
        (T('Today so far'), today_text(_and(RT, 'day') if RT is not None else None)),
        (T('Runtime evaluation'), esc(_nl_full(now, tz))),
    ])

    # Live status cards
    def w(v: Any) -> str:
        x = n_or(v)
        return '–' if x is None else _num_str(x) + ' W'

    grid_v0 = n_or(live_val(src('hesc_grid_power_sensor')))
    gep = S.get('input_boolean.hesc_grid_export_positive', UNDEFINED)
    grid_v = -grid_v0 if (grid_v0 is not None and _truthy(gep) and _seq(_get(gep, 'state'), 'on')) else grid_v0  # v1.5: sign setting
    irr_id = src('hesc_irradiance_sensor')
    irr_n = n_or(live_val(irr_id)) if _truthy(irr_id) else None
    live_cards = (card(T('FORECAST NOW'), w(live_val(src('hesc_forecast_now_sensor'), fc_attr)), T('Cautious estimate') + (' (' + esc(fc_attr) + ')' if _truthy(fc_attr) else ''))
                  + card(T('FORECAST +30 MIN'), w(live_val(src('hesc_forecast_30m_sensor'), fc_attr)), T('Start threshold ') + w(st('input_number.hesc_p_start')))
                  + card('PV', w(live_val(src('hesc_pv_power_sensor'))), T('Current solar power'))
                  + card(T('GRID'), '–' if grid_v is None else _num_str(abs(grid_v)) + ' W ' + (T('export') if grid_v < 0 else T('import')), T('Grid meter'))
                  + card(T('EV CHARGING'), w(live_val(src('hesc_ev_power_sensor'))), T('EV ') + (T('connected') if _seq(live_val(src('hesc_ev_connected_sensor')), 'on') else T('not connected'))
                         + T(' · charger ') + esc(live_val(src('hesc_charger_mode_entity'))))
                  + (card(T('IRRADIANCE'), '–' if irr_n is None else _num_str(irr_n) + ' W/m²', T('Weather station')) if _truthy(irr_id) else ''))

    n_sess, n_ev = sess_rows.count('<tr'), ev_rows.count('<tr')
    stamp = _nl_full(now, tz)

    rt_state = _and(RT, 'state') if RT is not None else None
    cd = _and(RT, 'cooldownUntil') if RT is not None else None
    cooldown = esc(fmt_ms(time_iso(cd)) if (_truthy(cd) and _cmp(cd, '>', now)) else T('none'))
    download = download_prefix + re.sub(r'[:T]', '-', iso(now)[:16]) + '.html'

    out = ('<!doctype html><html lang="' + _lang_code(lang) + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + T('HESC report') + '</title><style>' + _CSS + _CSS2 + '</style></head><body><div class="wrap">'
           + '<header class="top"><div><h1>' + T('HESC report') + '</h1><div class="meta">' + esc(stamp) + ' · ' + version + T(' · history since ') + esc(fmt_t(first) if _truthy(first) else '–') + ' · ' + _str(len(rows)) + T(' records') + '</div></div><button class="dl" id="download">' + T('Download report') + '</button></header>'
           + '<nav>' + ''.join('<a href="#' + n[0] + '">' + T(n[1]) + '</a>' for n in _NAV) + '</nav>'
           + '<section id="summary"><h2>' + T('Executive Summary') + '</h2>' + summary + '</section>'
           + '<section id="live"><h2>' + T('Live Status') + '</h2><div class="kpis">' + live_cards + '</div></section>'
           + '<section id="advice">' + (adv_html or '<h2>' + T('Advice') + '</h2><div class="sub">' + T('No advice available yet.') + '</div>') + '</section>'
           + '<section id="accuracy"><h2>' + T('How well did the forecast match reality during solar charging?') + '</h2><div class="kpis">' + kpis + '</div>'
           + '<div class="box"><div class="sub" style="margin-bottom:6px">' + T('Actual PV as % of the Solcast forecast (median estimate), per solar session of 10 min or longer') + '</div>' + (dist_rows if acc_list else '<span class="mut">' + T('No solar sessions recorded yet.') + '</span>') + '</div></section>'
           + '<section id="sources"><h2>' + T('How reliable are the sources?') + '</h2><div class="sub">' + T('All daylight 15-minute intervals, also without charging. Intervals in which HPVC limited PV are left out, because curtailed PV says nothing about the forecast.') + '</div><div class="kpis">' + rel_kpis + '</div>'
           + '<div class="box"><table><tr><th>' + T('Day') + '</th><th>' + T('Trend') + '</th><th>' + T('Intervals') + '</th><th>' + T('Actual / forecast') + '</th><th>' + T('Within ±20%') + '</th><th>' + T('Actual ≥ cautious') + '</th><th>' + T('PV per kW/m²') + '</th><th>' + T('Irradiance ↔ PV') + '</th></tr>' + (rel_rows or '<tr><td colspan="8" class="mut">' + T('No intervals recorded yet.') + '</td></tr>') + '</table><div class="sub" style="margin-top:6px">' + T('Trend: ↑ better means the forecast was closer to 100% than the previous day. PV per kW/m² and the correlation show how well the weather station explains the PV output (1,0 = perfect).') + '</div></div></section>'
           + '<section id="days"><h2>' + T('Per day (newest first)') + '</h2><div class="box"><table><tr><th>' + T('Day') + '</th><th>' + T('Trend') + '</th><th>' + T('Solar sessions') + '</th><th>' + T('Forecast kWh') + '</th><th>' + T('Actual PV kWh') + '</th><th>' + T('Actual / forecast') + '</th><th>' + T('EV kWh') + '</th><th>' + T('EV solar kWh') + '</th><th>' + T('Releases ok') + '</th></tr>' + (day_rows or '<tr><td colspan="9" class="mut">' + T('No data yet.') + '</td></tr>') + '</table><div class="sub" style="margin-top:6px">' + T('Trend compares actual/forecast with the previous day: ↑ higher, ↓ lower, → within 5 points.') + '</div></div></section>'
           + '<section id="sessions"><details class="compact"><summary>' + T('Sessions') + ' · ' + _str(n_sess) + T(' entries (newest first)') + '</summary><div class="box"><table><tr><th>' + T('Start') + '</th><th>' + T('Type') + '</th><th>' + T('Min') + '</th><th>' + T('Forecast kWh') + '</th><th>' + T('Actual PV kWh') + '</th><th>' + T('Actual / forecast') + '</th><th>' + T('EV kWh') + '</th><th>' + T('EV solar kWh') + '</th><th>' + T('EV started') + '</th><th>' + T('Reason') + '</th></tr>' + (sess_rows or '<tr><td colspan="10" class="mut">' + T('No sessions yet.') + '</td></tr>') + '</table></div></details></section>'
           + '<section id="events"><details class="compact"><summary>' + T('Decisions and events') + ' · ' + _str(n_ev) + T(' entries (newest first)') + '</summary><div class="box"><table><tr><th>' + T('Time') + '</th><th>' + T('Event') + '</th><th>' + T('Forecast') + '</th><th>' + T('Irradiance') + '</th><th>PV</th></tr>' + (ev_rows or '<tr><td colspan="5" class="mut">' + T('No events yet.') + '</td></tr>') + '</table></div></details></section>'
           + '<section id="settings"><h2>' + T('Settings') + '</h2><div class="box"><table>' + _HESC_NAME.sub(lambda m: '<td>' + m.group(1).upper(), set_rows) + '</table></div><h2 style="margin-top:18px">' + T('Input check') + '</h2><div class="box"><table>' + live_rows + '</table></div></section>'
           + '<section id="runtime"><h2>' + T('Runtime') + '</h2>' + kv([
               (T('Engine state'), esc(_or(rt_state, '–')) + T(' since ') + since_txt),
               (T('Cooldown until'), cooldown),
               (T('History file'), '<code>' + history_path + '</code> · ' + _str(len(rows)) + T(' records · ') + _num_str(_round(_utf16_len(raw) / 1024)) + ' KiB'),
           ]) + '</section>'
           + '<div class="sub" style="margin:20px 0">' + T('Home EV Solar Control works alongside Home PV Control (HPVC). The only thing it ever switches is the HPVC on/off switch, and only when shadow mode is off. In shadow mode it evaluates and logs, but switches nothing.') + '</div></div>'
           + '<script>document.getElementById("download").addEventListener("click",function(){var b=new Blob(["<!doctype html>"+document.documentElement.outerHTML],{type:"text/html;charset=utf-8"});var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="' + download + '";a.click();setTimeout(function(){URL.revokeObjectURL(a.href)},1000)});'
           + 'fetch("/api/webhook/' + webhook_id + '",{method:"POST",keepalive:true}).catch(function(){});</script></body></html>')

    status = 'report ' + _str(len(rows)) + ' records · ' + _nl_time(now, tz)
    return out, open_page(report_link, lang), status
