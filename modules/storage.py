"""Shared storage helpers for the V1 modular launcher."""

from __future__ import annotations

import os
from pathlib import Path


def is_writable_dir(path_obj: Path) -> bool:
    try:
        path_obj.mkdir(parents=True, exist_ok=True)
        test_file = path_obj / ".djtool_write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def resolve_app_data_dir() -> tuple[Path, str, bool]:
    env_candidates = [
        (os.environ.get("DJ_TOOL_DATA_DIR") or "").strip(),
        (os.environ.get("RENDER_DISK_MOUNT_PATH") or "").strip(),
        (os.environ.get("RENDER_DISK_PATH") or "").strip(),
    ]
    for raw in env_candidates:
        if not raw:
            continue
        candidate = Path(raw).expanduser() / "dj_tool_live_data"
        if is_writable_dir(candidate):
            return candidate, f"env:{raw}", True

    probe_candidates = [Path("/var/data/dj_tool_live_data"), Path("/data/dj_tool_live_data")]
    for candidate in probe_candidates:
        if is_writable_dir(candidate):
            return candidate, f"auto:{candidate}", True

    fallback = Path.home() / ".dj_tool_live_data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback, "fallback:home", False
