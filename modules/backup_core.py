"""Safely extracted backup helpers for V3."""

from __future__ import annotations

import io
import zipfile as pyzipfile
from pathlib import Path


def inspect_backup_zip(backup_path: str | Path) -> dict:
    p = Path(backup_path)
    if not p.exists() or p.stat().st_size <= 0:
        return {"exists": False, "has_db": False, "has_sets": False, "names": []}
    try:
        with pyzipfile.ZipFile(p, 'r') as zf:
            names = zf.namelist()
            return {
                "exists": True,
                "has_db": 'djtool_live.db' in names,
                "has_sets": 'saved_sets.json' in names,
                "names": names,
            }
    except Exception:
        return {"exists": True, "has_db": False, "has_sets": False, "names": []}


def restore_backup_zip_to_runtime(backup_path: str | Path, live_db: str | Path, live_sets: str | Path) -> bool:
    backup = Path(backup_path)
    if not backup.exists():
        return False
    try:
        with pyzipfile.ZipFile(backup, 'r') as zf:
            names = set(zf.namelist())
            if 'djtool_live.db' not in names:
                return False
            live_db = Path(live_db)
            live_sets = Path(live_sets)
            live_db.parent.mkdir(parents=True, exist_ok=True)
            with open(live_db, 'wb') as f:
                f.write(zf.read('djtool_live.db'))
            if 'saved_sets.json' in names:
                with open(live_sets, 'wb') as f:
                    f.write(zf.read('saved_sets.json'))
        return True
    except Exception:
        return False


def backup_contains_runtime_data(backup_path: str | Path) -> bool:
    info = inspect_backup_zip(backup_path)
    return bool(info.get('has_db'))
