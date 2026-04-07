from __future__ import annotations

import json
import os
import shutil
import sqlite3
import zipfile
from pathlib import Path

from .storage import resolve_app_data_dir


STATUS_FILE_NAME = "v2_runtime_status.json"


def _count_db_rows(db_path: Path) -> tuple[int, int]:
    if not db_path.exists() or db_path.stat().st_size <= 0:
        return 0, 0
    conn = None
    try:
        conn = sqlite3.connect(str(db_path), timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='playlists'")
        has_playlists = cur.fetchone() is not None
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='playlist_tracks'")
        has_tracks = cur.fetchone() is not None
        playlist_count = 0
        track_count = 0
        if has_playlists:
            cur.execute("SELECT COUNT(*) FROM playlists")
            playlist_count = int(cur.fetchone()[0] or 0)
        if has_tracks:
            cur.execute("SELECT COUNT(*) FROM playlist_tracks")
            track_count = int(cur.fetchone()[0] or 0)
        return playlist_count, track_count
    except Exception:
        return 0, 0
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass


def _extract_backup_to_runtime(backup_zip: Path, target_live_db: Path, target_live_sets: Path) -> tuple[bool, int, int]:
    try:
        with zipfile.ZipFile(backup_zip, "r") as zf:
            names = set(zf.namelist())
            if "djtool_live.db" not in names:
                return False, 0, 0
            target_live_db.parent.mkdir(parents=True, exist_ok=True)
            with open(target_live_db, "wb") as f:
                f.write(zf.read("djtool_live.db"))
            if "saved_sets.json" in names:
                with open(target_live_sets, "wb") as f:
                    f.write(zf.read("saved_sets.json"))
        playlists, tracks = _count_db_rows(target_live_db)
        return True, playlists, tracks
    except Exception:
        return False, 0, 0


def _inspect_backup_counts(backup_zip: Path) -> tuple[int, int]:
    try:
        with zipfile.ZipFile(backup_zip, "r") as zf:
            if "djtool_live.db" not in set(zf.namelist()):
                return 0, 0
            temp_db = backup_zip.parent / ".tmp_bootstrap_count.db"
            try:
                with open(temp_db, "wb") as f:
                    f.write(zf.read("djtool_live.db"))
                return _count_db_rows(temp_db)
            finally:
                temp_db.unlink(missing_ok=True)
    except Exception:
        return 0, 0


def _copy_project_db_if_better(project_dir: Path, live_db: Path, live_sets: Path) -> tuple[str, int, int, bool, bool]:
    project_db_candidates = [project_dir / "djtool_live.db", project_dir / "djtool.db"]
    source_db = next((p for p in project_db_candidates if p.exists() and p.stat().st_size > 0), None)
    source_sets = project_dir / "saved_sets.json"
    source_playlists, source_tracks = _count_db_rows(source_db) if source_db else (0, 0)
    copied_db = False
    copied_sets = False

    live_playlists, live_tracks = _count_db_rows(live_db)
    if source_db and (source_playlists + source_tracks) > (live_playlists + live_tracks):
        live_db.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_db, live_db)
        copied_db = True
        live_playlists, live_tracks = _count_db_rows(live_db)
    if source_sets.exists() and ((not live_sets.exists()) or live_sets.stat().st_size <= 2):
        try:
            shutil.copy2(source_sets, live_sets)
            copied_sets = True
        except Exception:
            copied_sets = False
    return str(source_db) if source_db else "", live_playlists, live_tracks, copied_db, copied_sets


def bootstrap_runtime(project_dir: Path) -> dict:
    os.environ.setdefault("DJ_TOOL_MODULAR_VERSION", "V2")
    live_dir, source_label, is_persistent = resolve_app_data_dir()
    live_db = live_dir / "djtool_live.db"
    live_sets = live_dir / "saved_sets.json"

    project_db_candidates = [project_dir / "djtool_live.db", project_dir / "djtool.db"]
    source_db = next((p for p in project_db_candidates if p.exists() and p.stat().st_size > 0), None)
    source_playlists, source_tracks = _count_db_rows(source_db) if source_db else (0, 0)

    backup_candidates = sorted(project_dir.glob("dj_tool_backup_*.zip"))
    backup_zip = backup_candidates[-1] if backup_candidates else None
    backup_playlists, backup_tracks = _inspect_backup_counts(backup_zip) if backup_zip else (0, 0)

    live_playlists, live_tracks = _count_db_rows(live_db)
    selected_source = "live_existing"
    copied_db = False
    copied_sets = False
    restored_from_backup = False

    should_fill_live = (not live_db.exists()) or (live_playlists <= 0 and live_tracks <= 0)
    if should_fill_live:
        best_kind = "none"
        best_score = -1
        if source_db and (source_playlists + source_tracks) > best_score:
            best_kind = "project_db"
            best_score = source_playlists + source_tracks
        if backup_zip and (backup_playlists + backup_tracks) > best_score:
            best_kind = "backup_zip"
            best_score = backup_playlists + backup_tracks

        if best_kind == "project_db" and source_db:
            live_db.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_db, live_db)
            copied_db = True
            selected_source = "project_db"
            live_playlists, live_tracks = _count_db_rows(live_db)
        elif best_kind == "backup_zip" and backup_zip:
            ok, p_count, t_count = _extract_backup_to_runtime(backup_zip, live_db, live_sets)
            if ok:
                copied_db = True
                restored_from_backup = True
                selected_source = "backup_zip"
                live_playlists, live_tracks = p_count, t_count

    source_db_str, live_playlists, live_tracks, project_copy_db, project_copy_sets = _copy_project_db_if_better(
        project_dir, live_db, live_sets
    )
    if project_copy_db:
        selected_source = "project_db_upgrade"
    copied_db = copied_db or project_copy_db
    copied_sets = copied_sets or project_copy_sets

    runtime_info = {
        "live_dir": str(live_dir),
        "live_db": str(live_db),
        "live_sets": str(live_sets),
        "live_playlists": live_playlists,
        "live_tracks": live_tracks,
        "source_label": source_label,
        "persistent_mode": bool(is_persistent),
        "source_db": source_db_str,
        "source_playlists": source_playlists,
        "source_tracks": source_tracks,
        "backup_zip": str(backup_zip) if backup_zip else "",
        "backup_playlists": backup_playlists,
        "backup_tracks": backup_tracks,
        "copied_db": copied_db,
        "copied_sets": copied_sets,
        "restored_from_backup": restored_from_backup,
        "selected_source": selected_source,
    }
    try:
        (project_dir / STATUS_FILE_NAME).write_text(
            json.dumps(runtime_info, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass
    return runtime_info
