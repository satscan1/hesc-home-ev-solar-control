"""Since 3.1.2: HESC's support report behind Home Assistant's login.

The report (charging history, entity states and settings) used to be written to /config/www, which
Home Assistant serves at /local/ without authentication. It now lives in HESC's own folder
(/config/hesc_v3/report/) and is only served by this view, which requires authentication. The
dashboard opens it through a short-lived signed path (auth/sign_path), so the browser can open it
in a new tab without a login header.
"""

from __future__ import annotations

from pathlib import Path

from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

REPORT_URL = "/api/" + DOMAIN + "/report"
REPORT_FOLDER = (DOMAIN + "_v3", "report")  # /config/hesc_v3/report/
REPORT_NAME = "report.html"
LEGACY_FOLDER = ("www", DOMAIN + "_v3")  # up to 3.1.1, served without login at /local/hesc_v3/


def report_path(hass: HomeAssistant) -> Path:
    return Path(hass.config.path(*REPORT_FOLDER, REPORT_NAME))


class HescReportView(HomeAssistantView):
    """GET /api/hesc/report: the latest report, for logged-in users (or a valid signed path)."""

    url = REPORT_URL
    name = "api:" + DOMAIN + ":report"
    requires_auth = True

    async def get(self, request: web.Request) -> web.StreamResponse:
        hass: HomeAssistant = request.app["hass"]
        path = report_path(hass)

        def read() -> str | None:
            try:
                return path.read_text(encoding="utf-8")
            except OSError:
                return None

        body = await hass.async_add_executor_job(read)
        if body is None:
            return web.Response(status=404, text="No HESC report yet: press 'Generate report' first.")
        return web.Response(text=body, content_type="text/html", charset="utf-8",
                            headers={"Cache-Control": "no-store"})


def remove_legacy_report(hass: HomeAssistant) -> None:
    """Remove the report files HESC wrote to /config/www/hesc_v3 up to 3.1.1 (run in the executor).
    Only HESC's own folder and only its own two files; the folder goes when it is then empty."""
    folder = Path(hass.config.path(*LEGACY_FOLDER))
    for name in ("report.html", "open.html"):
        try:
            (folder / name).unlink(missing_ok=True)
        except OSError:
            pass
    try:
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    except OSError:
        pass
