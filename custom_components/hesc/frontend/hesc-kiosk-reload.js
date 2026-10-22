// HESC kiosk screen (a tablet on the wall).
// 1. Since 3.0.0: on HESC's Kiosk page the Home Assistant menu (sidebar) and the top bar are hidden, so
//    the kiosk-mode card is no longer needed. Only on the Kiosk page of a HESC dashboard (also a copy
//    made with "Add dashboard"); add ?disable_km to the address to keep the menu.
// 2. Reload the page once after Home Assistant has restarted: a page that was opened before the restart
//    keeps running without the HESC icon set (that file is only served once HESC has loaded). This waits
//    until the connection is back and the icon file is served again, then reloads - only on the kiosk page.
(() => {
  const ICONS = "/hesc_v3_frontend/hesc-icons.js";
  const MARK = "data-hesc-kiosk";
  let lost = false;
  let polling = false;

  const parts = () => {
    const main = document.querySelector("home-assistant")?.shadowRoot?.querySelector("home-assistant-main");
    const drawer = main?.shadowRoot?.querySelector("ha-drawer");
    const panel = main?.shadowRoot?.querySelector("partial-panel-resolver ha-panel-lovelace");
    const root = panel?.shadowRoot?.querySelector("hui-root");
    return { main, drawer, panel, root };
  };

  const onKiosk = () => {
    if (!/^\/[^/]+\/kiosk\/?$/.test(location.pathname)) return false;
    const { panel } = parts();
    try {
      return JSON.stringify(panel?.lovelace?.config || {}).includes("custom:hesc-");
    } catch (e) {
      return false;
    }
  };

  const style = (root, css, on) => {
    if (!root) return;
    const old = root.querySelector(`style[${MARK}]`);
    if (on && !old) {
      const s = document.createElement("style");
      s.setAttribute(MARK, "");
      s.textContent = css;
      root.appendChild(s);
    } else if (!on && old) {
      old.remove();
    }
  };

  const applyKiosk = () => {
    const on = onKiosk() && !/[?&]disable_km\b/.test(location.search);
    const { main, drawer, root } = parts();
    style(main?.shadowRoot, "ha-sidebar { display: none !important; }", on);
    style(drawer?.shadowRoot, ".sidebar-shell { display: none !important; } .app-content { padding-inline-start: 0 !important; }", on);
    style(root?.shadowRoot, ".header { display: none !important; } #view, hui-view-container { padding-top: 0 !important; margin-top: 0 !important; --header-height: 0px; }", on);
  };
  window.addEventListener("location-changed", () => setTimeout(applyKiosk, 50));
  window.addEventListener("popstate", () => setTimeout(applyKiosk, 50));
  setInterval(applyKiosk, 1000);  // the page can be redrawn (new view, theme, restart)

  const waitAndReload = async () => {
    if (polling) return;
    polling = true;
    for (let i = 0; i < 120; i++) {  // up to 10 minutes, every 5 s
      await new Promise((r) => setTimeout(r, 5000));
      try {
        const res = await fetch(ICONS, { method: "HEAD", cache: "no-store" });
        if (res.ok) { location.reload(); return; }
      } catch (e) { /* HA not reachable yet */ }
    }
    polling = false;
  };

  const attach = () => {
    const conn = document.querySelector("home-assistant")?.hass?.connection;
    if (!conn) { setTimeout(attach, 1000); return; }
    conn.addEventListener("disconnected", () => { lost = true; });
    conn.addEventListener("ready", () => { if (lost && onKiosk()) { lost = false; waitAndReload(); } });
  };
  attach();
})();
