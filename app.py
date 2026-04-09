"""Compatibility launcher for Streamlit hosting.

This file intentionally forwards to the current modular entrypoint so
older startup scripts, Docker deploys and managed hosts keep working.
"""

from __future__ import annotations

from pathlib import Path
import runpy

PROJECT_DIR = Path(__file__).resolve().parent
TARGET = PROJECT_DIR / "app_modular.py"

if not TARGET.exists():
    raise FileNotFoundError(f"Expected launcher target not found: {TARGET}")

runpy.run_path(str(TARGET), run_name="__main__")
