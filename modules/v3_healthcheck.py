from __future__ import annotations

import json
from pathlib import Path

from .backup_core import inspect_backup_zip
from .db_core import count_playlists_and_tracks


def run_v3_healthcheck(project_dir: Path, runtime_info: dict) -> dict:
    live_db = Path(runtime_info.get('live_db', ''))
    live_sets = Path(runtime_info.get('live_sets', ''))
    backup_zip = Path(runtime_info.get('backup_zip', '')) if runtime_info.get('backup_zip') else None

    live_playlists, live_tracks = count_playlists_and_tracks(live_db)
    backup_info = inspect_backup_zip(backup_zip) if backup_zip else {"exists": False, "has_db": False, "has_sets": False}

    info = {
        "v": 3,
        "live_db": str(live_db),
        "live_sets": str(live_sets),
        "live_playlists": live_playlists,
        "live_tracks": live_tracks,
        "backup_zip": str(backup_zip) if backup_zip else "",
        "backup_has_db": bool(backup_info.get('has_db')),
        "backup_has_sets": bool(backup_info.get('has_sets')),
        "status": "ok" if (live_playlists > 0 or live_tracks > 0) else "empty_live_db",
    }
    try:
        (project_dir / 'v3_healthcheck.json').write_text(
            json.dumps(info, indent=2, ensure_ascii=False),
            encoding='utf-8',
        )
    except Exception:
        pass
    return info
