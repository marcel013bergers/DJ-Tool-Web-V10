from __future__ import annotations

import json
from pathlib import Path


def run_v5_preflight(project_dir: Path, runtime_info: dict, health_info: dict) -> dict:
    live_db = Path(runtime_info.get("live_db", "")) if runtime_info.get("live_db") else None
    backup_zip = Path(runtime_info.get("backup_zip", "")) if runtime_info.get("backup_zip") else None
    stable_app = project_dir / "app_STABLE_backup.py"

    info = {
        "v": 5,
        "status": "ok",
        "live_db_exists": bool(live_db and live_db.exists()),
        "backup_zip_exists": bool(backup_zip and backup_zip.exists()),
        "stable_app_exists": stable_app.exists(),
        "live_playlists": int(health_info.get("live_playlists", 0) or 0),
        "live_tracks": int(health_info.get("live_tracks", 0) or 0),
        "selected_source": runtime_info.get("selected_source", ""),
        "notes": [],
    }

    if not info["stable_app_exists"]:
        info["status"] = "stable_app_missing"
        info["notes"].append("app_STABLE_backup.py fehlt")
    if not info["live_db_exists"]:
        info["notes"].append("Live DB fehlt oder wurde noch nicht angelegt")
    if info["live_playlists"] <= 0 and info["backup_zip_exists"]:
        info["notes"].append("Backup ZIP ist vorhanden, falls ein Restore noetig ist")
    if info["live_playlists"] > 0:
        info["notes"].append("Live Datenbestand ist vorhanden")

    try:
        (project_dir / "v5_preflight.json").write_text(
            json.dumps(info, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass
    return info
