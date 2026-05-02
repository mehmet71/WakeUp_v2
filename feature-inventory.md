# WakeUp v2 — Feature Inventory

---

## Core: Profile Launcher (`wakeup.py` + `profile_runner.py`)

- Load profiles from `profiles.json` on startup
- Per-profile hotkey registration via `pynput` (global, works even when WakeUp is not focused)
- Tray icon (pystray + Pillow) with right-click menu listing all profiles
- Launch a profile via: tray menu, hotkey, or voice keyword — all dispatch to `profile_runner.run(profile)`
- `_busy` lock prevents double-trigger while a launch is in progress
- Profile execution on a daemon thread (non-blocking)
- Optional `message` field: printed to console after launch

## App Launching (`launcher.py`)

- Spawn apps via `subprocess` with configurable `delay` between apps
- `args` passed to the process (non-browser apps only)
- Env-var expansion in paths (`%LOCALAPPDATA%`, `%APPDATA%`, `%PROGRAMFILES%`)
- **Browser block** (Chromium: Chrome, Edge, Brave):
  - `restore_session: true` — restores last session
  - `restore_session: false` — opens a fresh window (`--new-window`)
  - `urls` — extra URLs appended as positional args
  - Browser apps do not use `args`; use `browser.urls` instead

## Window Positioning (`window_manager.py`)

- Detect all connected monitors via `win32api.EnumDisplayMonitors`
- Address windows by monitor index (0 = primary, 1 = secondary, …)
- 14 named presets:
  `full`, `left-half`, `right-half`, `top-half`, `bottom-half`,
  `top-left`, `top-right`, `bottom-left`, `bottom-right`,
  `left-third`, `center-third`, `right-third`,
  `left-two-thirds`, `right-two-thirds`
- Explicit pixel coords: `x/y/w/h` relative to monitor top-left
- Optional `maximize` flag
- Window arrangement always async (own thread per app, retries while window appears)
- Visible window detection via canonical Alt-Tab algorithm:
  - Cloaked-window check (`DwmGetWindowAttribute(DWMWA_CLOAKED)`)
  - Root-owner chain via `GetAncestor` + `GetLastActivePopup` (ctypes)
  - `WS_EX_TOOLWINDOW` exclusion

## Capture Service (`capture_service.py`)

- Snapshot all open visible windows (`capture_current_desktop`)
- Detect app type: `vscode`, `chromium`, `generic`
- Exclude WakeUp's own PID and `applicationframehost.exe` (UWP container)
- Map window position → monitor index + preset (best-fit)
- Produce draft app records ready for the review wizard

## Capture Review Wizard (`capture_ui.py`)

- Minimal Tkinter window, two screens:
  1. **Review** — one row per detected app:
     - Remove app from list
     - Add an app manually
     - Set folder/args (for editor apps: VS Code, Cursor, etc.)
     - Set browser URLs + toggle restore session (for browser apps)
  2. **Save** — set profile name, optional hotkey, optional message → writes to `profiles.json`
- No general profile editor; this UI is capture-only

## Voice Detection (`audio_engine.py`, optional)

- Offline keyword spotting via Vosk (not installed by default)
- Opens Windows default microphone via `sounddevice` (WASAPI)
- Continuous listening on a background thread
- Matches spoken words against `trigger_keywords` for each profile
- Gracefully disabled if `sounddevice` or `vosk` not installed (`HAS_AUDIO` guard)

## Graceful Degradation

All optional integrations have `HAS_X` guards — missing packages disable the feature but don't crash:
- `pynput` — hotkeys disabled if missing
- `pystray` + `Pillow` — tray icon disabled if missing
- `sounddevice` — audio disabled if missing
- `vosk` — voice recognition disabled if missing
- `pywin32` — window positioning disabled if missing

## Tests

- Preset math: given a monitor rect, verify each named preset produces correct coordinates
- Schema validation: malformed profiles fail with a clear error, not a crash

## Out of Scope

- General profile editor UI (edit `profiles.json` directly)
- Phase 4: local voice agent (Whisper STT + LLM + TTS) — build on top later if needed
