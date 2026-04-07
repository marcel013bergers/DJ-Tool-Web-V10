from __future__ import annotations

import json
from pathlib import Path

from .db_core import count_playlists_and_tracks


def build_startup_summary(project_dir: Path, runtime_info: dict) -> dict:
    live_db = Path(runtime_info.get("live_db", ""))
    live_sets = Path(runtime_info.get("live_sets", ""))
    playlists, tracks = count_playlists_and_tracks(live_db)

    summary = {
        "project_dir": str(project_dir),
        "live_db": str(live_db),
        "live_sets": str(live_sets),
        "selected_source": runtime_info.get("selected_source", ""),
        "playlists": playlists,
        "tracks": tracks,
        "app_data_dir": runtime_info.get("app_data_dir", ""),
        "app_data_dir_source": runtime_info.get("app_data_dir_source", ""),
        "persistent_mode": bool(runtime_info.get("persistent_mode", False)),
        "backup_zip": runtime_info.get("backup_zip", ""),
        "notes": [],
    }

    if playlists > 0 or tracks > 0:
        summary["notes"].append("Live DB is available.")
    else:
        summary["notes"].append("Live DB is empty.")
    if runtime_info.get("backup_zip"):
        summary["notes"].append("Backup ZIP found in project.")
    return summary


def write_startup_summary(project_dir: Path, payload: dict) -> None:
    try:
        (project_dir / "v4_startup_summary.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass
