from __future__ import annotations

def render_version_banner(st, g: dict) -> None:
    try:
        version = g.get("APP_VERSION", "Unbekannt")
        build_date = g.get("APP_BUILD_DATE", "-")
        build_time = g.get("APP_BUILD_TIME", "-")
        st.caption(f"Aktuelle Version: {version} | Build: {build_date} {build_time} | Modular Safe V5.2")
    except Exception:
        pass
