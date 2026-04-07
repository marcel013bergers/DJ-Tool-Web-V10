from pathlib import Path

APP = Path('/mnt/data/app_v150_master_stable.py')
text = APP.read_text(encoding='utf-8')

checks = {
    'version_v150': 'APP_SHORT_VERSION = "V150"' in text,
    'build_source': 'APP_BUILD_SOURCE =' in text,
    'upload_note_column': 'upload_note TEXT' in text or 'ADD COLUMN upload_note' in text,
    'save_playlist_upload_note': 'def save_playlist(name, event, source, is_top, import_type, tracks, sub_event="", upload_note="")' in text,
    'single_edit_restore': 'def update_playlist_meta(' in text and '💾 Änderungen speichern' in text,
    'rebuild_restore': 'def rebuild_full_analysis_state()' in text and '🧠 Gesamten Bestand neu analysieren' in text,
    'zip_duplicate_index': 'preload_duplicate_index(' in text and 'find_duplicate_playlists_in_index(' in text,
    'executemany_insert': 'cur.executemany(' in text,
}

failed = [name for name, ok in checks.items() if not ok]
print('Smoke test results:')
for name, ok in checks.items():
    print(f'- {name}: {"OK" if ok else "FAIL"}')

if failed:
    raise SystemExit(f"\nFAILED: {', '.join(failed)}")
print('\nAll smoke checks passed.')
