"""Safely extracted build/config values for the V1 modular entrypoint.

This is intentionally non-invasive:
- app.py stays the stable implementation
- app_modular.py uses these values for the migration-safe runtime
"""

APP_VERSION = "DJ Tool V151 - Release Guard"
APP_SHORT_VERSION = "V151"
APP_BUILD_DATE = "2026-04-02"
APP_BUILD_TIME = "20:12"
APP_BASELINE_ID = "djtool_master_baseline_v1"
SOURCE_MASTER_BUILD = "V129"
MASTER_BUILD_RULE = "Neue Versionen nur auf der letzten funktionierenden Version aufbauen"
RELEASE_GUARD_MANIFEST_DIR = "release_guard"
RELEASE_GUARD_AUTO_WRITE = True
REQUIRE_SAFE_STORAGE_FOR_IMPORTS = True

SOURCE_PRESETS = ["Benjamin Schneider", "Michael Zimmermann", "Global", "Reverenz"]
EVENT_IMPORT_PRESETS = [
    "Hochzeit", "Geburtstag", "Party", "Firmenfeier", "Fasching", "80s", "90s",
    "90er-2000er", "2000s", "2010s", "Mixed", "Schlager", "Rock", "Latin"
]
BIRTHDAY_SUBEVENT_PRESETS = ["18", "21", "30", "40", "50", "60", "70", "80", "90"]
