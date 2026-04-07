from __future__ import annotations

import json
from pathlib import Path

from .backup_core import inspect_backup_zip
from .db_core import count_playlists_and_tracks


def run_v4_healthcheck(project_dir: Path, runtime_info: dict, startup_summary: dict) -> dict:
    live_db = Path(runtime_info.get("live_db", ""))
    backup_zip = Path(runtime_info.get("backup_zip", "")) if runtime_info.get("backup_zip") else None

    live_playlists, live_tracks = count_playlists_and_tracks(live_db)
    backup_info = inspect_backup_zip(backup_zip) if backup_zip else {"exists": False, "has_db": False, "has_sets": False}

    status = "ok" if (live_playlists > 0 or live_tracks > 0) else "empty_live_db"
    info = {
        "v": 4,
        "status": status,
        "live_db": str(live_db),
        "live_playlists": live_playlists,
        "live_tracks": live_tracks,
        "backup_zip": str(backup_zip) if backup_zip else "",
        "backup_has_db": bool(backup_info.get("has_db")),
        "backup_has_sets": bool(backup_info.get("has_sets")),
        "selected_source": runtime_info.get("selected_source", ""),
        "app_data_dir": runtime_info.get("app_data_dir", ""),
        "persistent_mode": bool(runtime_info.get("persistent_mode", False)),
        "startup_summary": startup_summary,
    }
    try:
        (project_dir / "v4_healthcheck.json").write_text(
            json.dumps(info, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass
    return info
