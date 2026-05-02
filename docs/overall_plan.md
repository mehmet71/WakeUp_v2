# WakeUp v2 — Overall Plan

## Build Order

| # | Feature | Module(s) | Status |
|---|---------|-----------|--------|
| 1 | **Walking skeleton** — `profiles.json`, basic process spawn, profile runner, entry point (`python wakeup.py`, dev flag `--run <profile>`) | `profiles.json`, `launcher.py`, `profile_runner.py`, `wakeup.py` | `[x]` |
| 2 | Window positioning — monitor detection, preset layout math, win32 positioning | `window_manager.py`, `profile_runner.py` | `[ ]` |
| 3 | Hotkeys + persistent process — pynput hotkey registration, background event loop | `wakeup.py` | `[ ]` |
| 4 | Tray icon — pystray menu, launch profile, quit | `wakeup.py` | `[ ]` |
| 5 | Browser block — `urls`, `restore_session`, Chromium args | `launcher.py` | `[ ]` |
| 6 | Desktop capture — snapshot open windows → draft app records | `capture_service.py` | `[ ]` |
| 7 | Capture review wizard — review drafts, set name/hotkey, save to `profiles.json` | `capture_ui.py` | `[ ]` |
| 8 | Voice keywords — Vosk listener, keyword matching | `audio_engine.py` | `[ ]` |
| 9 | Tests — preset math, schema validation | `tests/` | `[ ]` |

**Task 1 is the skeleton.** After it, the app is runnable end-to-end (CLI only, no tray, no hotkeys, no window positioning — but apps spawn). Every task after that improves the already-running app.

## Status Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Done |
