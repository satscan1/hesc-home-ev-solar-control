"""Report and back-up of HESC v4 in three forms (step 8, decisions 30-10-2026 21:13-21:35, 31-10 ± 19:45).

As in Marstek Capacity Monitor (`export.py` there): one format, three forms.

* full       - back-up: everything, also names, entity ids and phones; the planning and the learned
               charging power of each car can be put back from it (restore)
* anonymous  - to share (a bug or a question, on GitHub): no names, entity ids, phones or installation
               ids; each car gets a fixed random code; the settings, the planning and the latest decisions
               with their reasons stay
* bug        - short, in English, to paste into a GitHub issue: version, set-up, status per car, the
               latest decisions and what is missing

The file is an HTML page in the house style (as the HESC report and Cap Mon) with the data embedded
as JSON; a person reads the page, HESC (restore) reads the embedded data. What you see is what you share.

No Home Assistant dependency: the coordinator collects the data, this module turns it into one file.
"""
from __future__ import annotations

import json
import re
from html import escape
from typing import Any, Final

FORMAT: Final = "hesc-v4-export"
SCHEMA: Final = 1
VARIANTS: Final = ("full", "anonymous", "bug")
SCRIPT_ID: Final = "hesc-data"
FILE_NAMES: Final = {"full": "hesc_backup.html", "anonymous": "hesc_share.html", "bug": "hesc_bug.html"}

_ENTITY = re.compile(r"\b(?:sensor|binary_sensor|switch|select|number|input_[a-z]+|button|text|notify|device_tracker|"
                     r"person|zone|climate|light|cover|date|datetime)\.[a-z0-9_]+\b")
# keys of a car's or the shared settings that name a person, a phone or a place
_PRIVATE_KEYS: Final = frozenset({"notify_services", "ev_name", "name", "car_name"})


class ExportError(ValueError):
    """Not a HESC v4 export, or one made by a newer HESC."""


def build(variant: str, data: dict[str, Any]) -> dict[str, Any]:
    """One export. `data`: meta, setup (per car: entity ids and choices), settings (per car: helper ->
    value), planning and learn (per car), status (per car), decisions (per car: latest history
    lines), missing (per car), fleet (shared), share_ids (car -> fixed random code)."""
    if variant not in VARIANTS:
        raise ExportError(f"unknown variant {variant}")
    meta = data.get("meta") or {}
    out: dict[str, Any] = {"format": FORMAT, "schema": SCHEMA, "variant": variant,
                           "created": meta.get("created"), "hesc_version": meta.get("hesc_version"),
                           "ha_version": meta.get("ha_version"), "language": meta.get("language")}
    cars = list((data.get("status") or {}).keys())
    if variant == "full":
        out.update({k: data.get(k) for k in ("setup", "settings", "planning", "learn", "status", "decisions",
                                              "missing", "fleet", "names")})
        return out
    codes = data.get("share_ids") or {}
    out["cars"] = {codes.get(ev, ev.upper()): {
        "setup": _anon_setup((data.get("setup") or {}).get(ev) or {}),
        "settings": _anon_settings((data.get("settings") or {}).get(ev) or {}),
        "planning": (data.get("planning") or {}).get(ev),
        "learn": (data.get("learn") or {}).get(ev),
        "status": _anon_text((data.get("status") or {}).get(ev), data),
        "decisions": [_anon_text(d, data) for d in ((data.get("decisions") or {}).get(ev) or [])][
            -(200 if variant == "anonymous" else 15):],
        "missing": (data.get("missing") or {}).get(ev) or [],
    } for ev in cars}
    out["fleet"] = _anon_text(data.get("fleet"), data)
    if variant == "bug":
        out["text"] = bug_text(out)
    return out


def _anon_setup(setup: dict[str, Any]) -> dict[str, Any]:
    """Entity ids become "set" / "not set" (the kind of charger and other choices stay)."""
    out = {}
    for k, v in setup.items():
        if isinstance(v, str) and _ENTITY.fullmatch(v.strip()):
            out[k] = "set (" + v.split(".", 1)[0] + ")"
        elif k in _PRIVATE_KEYS:
            continue
        else:
            out[k] = v if not isinstance(v, str) else _ENTITY.sub(lambda m: m.group(0).split(".", 1)[0], v)
    return out


def _anon_settings(settings: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, v in settings.items():
        if any(p in k for p in _PRIVATE_KEYS):
            continue
        if isinstance(v, str) and _ENTITY.search(v):
            out[k] = "set" if v.strip() else ""
        else:
            out[k] = v
    return out


def _anon_text(v: Any, data: dict[str, Any]) -> Any:
    """Names of the cars become their code; entity ids become their domain."""
    names = {n: data.get("share_ids", {}).get(ev, ev.upper()) for ev, n in (data.get("names") or {}).items() if n}
    if isinstance(v, str):
        s = _ENTITY.sub(lambda m: m.group(0).split(".", 1)[0], v)
        for n, code in names.items():
            s = s.replace(n, code)
        return s
    if isinstance(v, dict):
        return {k: _anon_text(x, data) for k, x in v.items() if k not in _PRIVATE_KEYS}
    if isinstance(v, list):
        return [_anon_text(x, data) for x in v]
    return v


def bug_text(export: dict[str, Any]) -> str:
    """The short English summary to paste into a GitHub issue (Markdown)."""
    lines = [f"**HESC** {export.get('hesc_version')} · **Home Assistant** {export.get('ha_version')} · "
             f"language {export.get('language')} · made {export.get('created')}", ""]
    fleet = export.get("fleet") or {}
    if fleet:
        lines.append("Set-up: " + ", ".join(f"{k} {v}" for k, v in fleet.items() if v not in (None, "", [], {})))
        lines.append("")
    for code, car in (export.get("cars") or {}).items():
        st = car.get("status") or {}
        lines.append(f"### {code}")
        setup = car.get("setup") or {}
        lines.append("- charger: " + str(setup.get("charger_type") or "?") + "; battery sensor: "
                     + ("set" if str(setup.get("ev_soc_sensor") or "").startswith("set") else "not set"))
        for k in ("state", "reason", "plan_status", "next_ready_by", "charging_power_kw"):
            if st.get(k) not in (None, ""):
                lines.append(f"- {k.replace('_', ' ')}: {st[k]}")
        if car.get("missing"):
            lines.append("- missing: " + ", ".join(str(m) for m in car["missing"]))
        if car.get("decisions"):
            lines.append("- latest decisions:")
            lines += [f"  - {d}" for d in car["decisions"][-15:]]
        lines.append("")
    return "\n".join(lines).strip() + "\n"


# ---- reading --------------------------------------------------------------------------------------
def parse(text: str) -> dict[str, Any]:
    """Read an export: the HTML page (data embedded) or plain JSON."""
    text = text.strip()
    if not text.startswith("{"):
        m = re.search(rf'<script type="application/json" id="{SCRIPT_ID}">(.*?)</script>', text, re.S)
        if not m:
            raise ExportError("no HESC data in this file")
        text = m.group(1).replace("<\\/", "</")
    try:
        export = json.loads(text)
    except json.JSONDecodeError as err:
        raise ExportError("damaged HESC data") from err
    if export.get("format") != FORMAT:
        raise ExportError("not a HESC v4 export")
    if int(export.get("schema") or 0) > SCHEMA:
        raise ExportError("made by a newer HESC")
    return export


# ---- the page -----------------------------------------------------------------------------------
_CSS = (
    ":root{--bg:#f6f7f9;--card:#fff;--tx:#1d2330;--mut:#667085;--ln:#e3e6ea;--ac:#1f7ae0;--ok:#2e9e5b}"
    "@media (prefers-color-scheme: dark){:root{--bg:#15181e;--card:#1e2128;--tx:#e8eaed;--mut:#9aa0a6;"
    "--ln:#333744;--ac:#42a5f5;--ok:#66bb6a}}"
    "*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);"
    "font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}"
    ".wrap{max-width:1100px;margin:0 auto;padding:16px}h1{font-size:22px;margin:0 0 4px}"
    "h2{font-size:16px;margin:24px 0 8px}.sub{color:var(--mut);font-size:13px}"
    ".box{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:14px;margin-top:10px;"
    "overflow-x:auto}pre{white-space:pre-wrap;margin:0;font:12px/1.4 ui-monospace,Menlo,Consolas,monospace}"
    "table{border-collapse:collapse;width:100%}td{padding:6px 10px;border-top:1px solid var(--ln);vertical-align:top}"
    "td:first-child{color:var(--mut);width:35%}button{background:var(--ac);color:#fff;border:0;border-radius:8px;"
    "padding:9px 14px;font-weight:600;cursor:pointer}.in{border-left:4px solid var(--ok);padding:4px 0 4px 12px}"
    ".out{border-left:4px solid var(--mut);padding:4px 0 4px 12px;margin-top:14px;color:var(--mut)}"
    "@media print{button{display:none}}"
)

_L: Final[dict[str, dict[str, Any]]] = {
    "nl": {"title": {"full": "HESC — volledige back-up", "anonymous": "HESC — anoniem om te delen",
                     "bug": "HESC — kort voor een bugmelding"},
           "made": "gemaakt", "download": "Rapport downloaden", "copy": "Tekst kopiëren",
           "in": "Dit staat in het bestand", "out": "Dit zit er níet in",
           "share_in": {"full": ["alle instellingen, met namen, entiteiten en telefoons", "de planning en het geleerde laadvermogen per auto",
                                 "de stand en de laatste beslissingen per auto"],
                        "anonymous": ["de instellingen, zonder namen en entiteiten", "de planning en het geleerde laadvermogen per auto",
                                      "de laatste beslissingen met hun reden"],
                        "bug": ["versie, opstelling en stand per auto", "de laatste 15 beslissingen", "wat er ontbreekt"]},
           "share_out": {"full": ["niets weggelaten: bewaar dit bestand zelf, deel het niet"],
                         "anonymous": ["namen van auto's (een vaste code in de plaats)", "entiteit-id's en telefoons",
                                       "je locatie en je Home Assistant-adres"],
                         "bug": ["namen, entiteiten, telefoons en locatie"]},
           "data": "Gegevens"},
    "en": {"title": {"full": "HESC — full back-up", "anonymous": "HESC — anonymous to share", "bug": "HESC — short for a bug report"},
           "made": "made", "download": "Download report", "copy": "Copy text",
           "in": "This is in the file", "out": "This is not in it",
           "share_in": {"full": ["all settings, with names, entities and phones", "the planning and the learned charging power per car",
                                 "the status and latest decisions per car"],
                        "anonymous": ["the settings, without names and entities", "the planning and the learned charging power per car",
                                      "the latest decisions with their reason"],
                        "bug": ["version, set-up and status per car", "the latest 15 decisions", "what is missing"]},
           "share_out": {"full": ["nothing left out: keep this file yourself, do not share it"],
                         "anonymous": ["names of the cars (a fixed code instead)", "entity ids and phones",
                                       "your location and your Home Assistant address"],
                         "bug": ["names, entities, phones and location"]},
           "data": "Data"},
    "de": {"title": {"full": "HESC — vollständige Sicherung", "anonymous": "HESC — anonym zum Teilen",
                     "bug": "HESC — kurz für eine Fehlermeldung"},
           "made": "erstellt", "download": "Bericht herunterladen", "copy": "Text kopieren",
           "in": "Das steht in der Datei", "out": "Das steht nicht darin",
           "share_in": {"full": ["alle Einstellungen, mit Namen, Entitäten und Telefonen", "die Planung und die gelernte Ladeleistung je Auto",
                                 "Stand und letzte Entscheidungen je Auto"],
                        "anonymous": ["die Einstellungen, ohne Namen und Entitäten", "die Planung und die gelernte Ladeleistung je Auto",
                                      "die letzten Entscheidungen mit Grund"],
                        "bug": ["Version, Aufbau und Stand je Auto", "die letzten 15 Entscheidungen", "was fehlt"]},
           "share_out": {"full": ["nichts weggelassen: Datei selbst aufbewahren, nicht teilen"],
                         "anonymous": ["Namen der Autos (ein fester Code statt dessen)", "Entitäts-IDs und Telefone",
                                       "dein Standort und deine Home-Assistant-Adresse"],
                         "bug": ["Namen, Entitäten, Telefone und Standort"]},
           "data": "Daten"},
}


def page(export: dict[str, Any], lang: str | None = "en") -> str:
    """The HTML page with the export embedded (as Cap Mon: what you see is what you share)."""
    L = _L.get((lang or "en")[:2], _L["en"])
    v = export["variant"]
    blob = json.dumps(export, ensure_ascii=False, indent=1).replace("</", "<\\/")
    shown = export.get("text") if v == "bug" else json.dumps(
        {k: x for k, x in export.items() if k not in ("format", "schema")}, ensure_ascii=False, indent=1)
    name = f"hesc-{v}-{str(export.get('created') or '')[:10]}.html"
    ins = "".join(f"<li>{escape(x)}</li>" for x in L["share_in"][v])
    outs = "".join(f"<li>{escape(x)}</li>" for x in L["share_out"][v])
    copy = (f'<button onclick="navigator.clipboard.writeText(document.getElementById(\'t\').innerText)">'
            f'{escape(L["copy"])}</button> ') if v == "bug" else ""
    return (
        f'<!doctype html><html lang="{escape((lang or "en")[:2])}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(L["title"][v])}</title>'
        f"<style>{_CSS}</style></head><body><div class=\"wrap\">"
        f'<h1>{escape(L["title"][v])}</h1><div class="sub">HESC {escape(str(export.get("hesc_version")))} · '
        f'{escape(L["made"])} {escape(str(export.get("created")))}</div>'
        f'<div class="box"><div class="in"><b>{escape(L["in"])}</b><ul>{ins}</ul></div>'
        f'<div class="out"><b>{escape(L["out"])}</b><ul>{outs}</ul></div></div>'
        f'<p>{copy}<button onclick="dl()">{escape(L["download"])}</button></p>'
        f'<h2>{escape(L["data"])}</h2><div class="box"><pre id="t">{escape(str(shown))}</pre></div>'
        f'<script type="application/json" id="{SCRIPT_ID}">{blob}</script>'
        "<script>function dl(){const b=new Blob([document.documentElement.outerHTML],{type:'text/html'});"
        f"const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download={json.dumps(name)};a.click();}}</script>"
        "</div></body></html>"
    )
