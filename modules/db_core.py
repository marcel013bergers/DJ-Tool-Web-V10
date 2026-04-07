"""Safely extracted database helpers for V3.

These helpers are copied from the stable app logic without changing behavior.
V3 uses them for startup validation only; the stable app remains untouched.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def count_playlists_and_tracks(db_path: str | Path) -> tuple[int, int]:
    p = Path(db_path)
    if (not p.exists()) or p.stat().st_size <= 0:
        return 0, 0
    conn = None
    try:
        conn = sqlite3.connect(str(p), timeout=5)
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


def database_exists_and_has_content(db_path: str | Path) -> bool:
    playlists, tracks = count_playlists_and_tracks(db_path)
    return bool(playlists > 0 or tracks > 0)
