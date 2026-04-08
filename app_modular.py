"""DJ Tool V16 modular launcher.

V5 is intentionally conservative:
- keeps the full V4 project contents intact
- keeps the stable app as the real runtime
- keeps the stable runtime unchanged
- adds sidebar quick access and recent menu shortcuts
- keeps the Windows starter reliable
"""

from __future__ import annotations

from pathlib import Path
import streamlit as st
import os
import runpy

from modules.runtime_bootstrap import bootstrap_runtime
from modules.startup_bridge import build_startup_summary, write_startup_summary
from modules.v4_healthcheck import run_v4_healthcheck
from modules.v5_preflight import run_v5_preflight
from modules.version_banner import render_version_banner

st.set_page_config(page_title="DJ Tool", layout="wide")

PROJECT_DIR = Path(__file__).parent
runtime = bootstrap_runtime(PROJECT_DIR)
summary = build_startup_summary(PROJECT_DIR, runtime)
health = run_v4_healthcheck(PROJECT_DIR, runtime, summary)
preflight = run_v5_preflight(PROJECT_DIR, runtime, health)
health["v5_preflight"] = preflight
write_startup_summary(PROJECT_DIR, health)

print(
    f"[DJ Tool V10] source={runtime.get('selected_source')} "
    f"playlists={health.get('live_playlists', 0)} tracks={health.get('live_tracks', 0)} "
    f"status={health.get('status', '-')} preflight={preflight.get('status', '-')}",
    flush=True,
)

os.environ["DJ_TOOL_LAUNCHER_VERSION"] = "V16 Heute auflegen + DJ Memory PRO"
os.environ["DJ_TOOL_LAUNCHER_LABEL"] = "Modular Launcher"
os.environ["DJ_TOOL_CORE_APP"] = "V16"
os.environ["DJ_TOOL_PACKAGE_BASE"] = "V16 Heute auflegen + DJ Memory PRO"

stable_app = PROJECT_DIR / 'app_STABLE_backup.py'
runpy.run_path(str(stable_app), run_name='__main__')
