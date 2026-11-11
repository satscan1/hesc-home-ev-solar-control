"""08-11 (opmaakchat, beta.1 nr 7): the charging-costs CSV as a download for the panel.

`GET /api/hesc_v4/costs/{car}/{kind}.csv` (`kind` = days or months) returns the file HESC's "Export charging
costs (CSV)" wrote for that car. Only for a signed-in user (requires_auth): the costs are private, so they
are not put in /config/www (served without a login). The panel fetches it with the user's token
(`hass.fetchWithAuth`) and offers it as a file.
"""
from __future__ import annotations

from pathlib import Path

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from . import cars, model
from .const import DOMAIN

URL = "/api/hesc_v4/costs/{car}/{kind}.csv"


class CostsCsvView(HomeAssistantView):
    url = URL
    name = "api:hesc_v4:costs_csv"
    requires_auth = True

    async def get(self, request: web.Request, car: str, kind: str) -> web.Response:
        hass: HomeAssistant = request.app["hass"]
        if car not in model.EVS or kind not in ("days", "months"):
            return web.Response(status=404)
        name = cars.file_name(f"charging_costs_{kind}.csv", car)
        entries = [e for e in hass.config_entries.async_entries(DOMAIN) if getattr(e, "runtime_data", None)]
        base = entries[0].runtime_data.data_dir if entries else Path(hass.config.path(DOMAIN))
        path = Path(base) / name
        if not await hass.async_add_executor_job(path.exists):
            return web.Response(status=404, text="Not exported yet: press 'Export charging costs (CSV)' first")
        body = await hass.async_add_executor_job(path.read_bytes)
        return web.Response(body=body, content_type="text/csv", charset="utf-8",
                            headers={"Content-Disposition": f'attachment; filename="{name}"'})


def async_register(hass: HomeAssistant) -> None:
    hass.http.register_view(CostsCsvView())
