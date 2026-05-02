# WakeUp v2 — Overall Plan

## Build Order

| # | Feature | Module(s) | Status |
|---|---------|-----------|--------|
| 1 | Window positioning — monitors, presets, win32 | `window_manager.py` | `[ ]` |
| 2 | App launching — process spawning, browser block, env vars | `launcher.py` | `[ ]` |
| 3 | Profile execution — iterate apps, busy lock, daemon thread | `profile_runner.py` | `[ ]` |
| 4 | Entry point — tray icon, hotkey registration, wiring | `wakeup.py` | `[ ]` |
| 5 | Desktop capture — snapshot open windows → draft records | `capture_service.py` | `[ ]` |
| 6 | Capture review wizard — review drafts, save profile | `capture_ui.py` | `[ ]` |
| 7 | Voice keyword detection — Vosk listener, keyword matching | `audio_engine.py` | `[ ]` |
| 8 | Tests — preset math, schema validation | `tests/` | `[ ]` |

## Status Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Done |
