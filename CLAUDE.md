# WakeUp v2 — CLAUDE.md

## Rules

- Whenever a design decision is made during conversation — about architecture, module boundaries, schema, features in or out, or any non-obvious implementation choice — add an entry to `docs/decisions.md` immediately. Format: date header, decision title, **Decision:** one sentence, **Why:** one sentence.
- Every function and method must have a one-line comment directly above the `def` line describing what it does. Add or update this comment whenever creating or editing a function.
- When implementing any feature, break the work into small, focused tasks. Each task should do one thing, be independently reviewable, and be completable without depending on unfinished sibling tasks. Never bundle unrelated changes into a single task. The goal is that each completed task produces a diff the user can read and understand in under a minute.

## Project Overview

WakeUp is a personal workspace launcher for Windows. It listens for voice keywords and hotkeys, then spawns and positions apps defined in profile configs. The primary way to create profiles is by capturing the current desktop.

## Architecture

```
wakeup.py          ← Entry point: tray icon, hotkey registration, dispatches to profile_runner
profile_runner.py  ← Executes a profile: iterates apps, calls launcher, triggers window_manager
launcher.py        ← Process spawning (subprocess + env-var expansion + browser arg handling)
window_manager.py  ← Monitor detection, preset layout math, win32 window positioning
capture_service.py ← Desktop snapshot → draft app records for the review wizard
capture_ui.py      ← Minimal Tkinter review wizard (capture only, not a general profile editor)
audio_engine.py    ← Optional Vosk voice keyword listener
profiles.json      ← User configuration (profiles + settings)
```

Each file has one job. Business logic does not live in `wakeup.py` or `capture_ui.py`.

## Key Design Decisions

- **Three trigger paths:** voice keywords, hotkeys (pynput), tray menu. All three dispatch to the same `profile_runner.run(profile)` call.
- **All optional dependencies degrade gracefully.** `pynput`, `pystray`, `sounddevice`, `vosk`, `pywin32` each have a `HAS_X` guard. Missing packages disable the feature but don't crash.
- **Voice uses Windows default mic.** No device selection needed.
- **Threading model.** Profile execution runs on a daemon thread. A `_busy` lock prevents double-triggers. Window arrangement is async (own thread per app, retries while window appears).
- **Hotkeys use pynput** (not `keyboard`, which is unmaintained).
- **No general profile editor UI.** Profiles are edited directly in `profiles.json`. The only UI is the capture review wizard (`capture_ui.py`).
- **Capture window filtering uses two layers:** `window_manager.list_visible_windows` (canonical Alt-Tab algorithm: cloaked-window check, root-owner chain, `WS_EX_TOOLWINDOW` exclusion) + `capture_service` exclusions (self-PID, `applicationframehost.exe`).

## profiles.json Schema

```json
{
  "settings": {
    "default_profile": "work",
    "voice": {
      "enabled": false,
      "model_path": "models/vosk-model-small-en-us",
      "sample_rate": 16000
    }
  },
  "profiles": {
    "<name>": {
      "trigger_keywords": ["..."],
      "hotkey": "ctrl+alt+w",
      "message": "...",
      "apps": [
        {
          "name": "VS Code",
          "path": "%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe",
          "args": ["C:/Projects/my-project"],
          "delay": 0,
          "window": {
            "monitor": 0,
            "preset": "left-two-thirds"
          }
        },
        {
          "name": "Chrome",
          "path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
          "delay": 0.5,
          "window": { "monitor": 0, "preset": "right-third" },
          "browser": {
            "restore_session": false,
            "urls": ["https://github.com"]
          }
        }
      ]
    }
  }
}
```

**Schema rules:**
- `hotkey` — optional. Omit if no hotkey desired (do not use `""`).
- `message` — optional. Omit if no message desired.
- `trigger_keywords` — optional. Omit or use `[]` if no voice trigger desired.
- `args` — for non-browser apps only. Omit for browser apps; use `browser.urls` instead.
- `delay` — seconds to wait before spawning this app (float, default 0).

**Window config options:**
- `preset` — one of the named presets listed below
- `x/y/w/h` (int) — explicit coords relative to monitor top-left
- `monitor` (int) — 0 = primary, 1 = secondary
- `maximize` (bool) — optional, forces maximize after positioning

**Browser block** (`browser` key on app entry, Chromium-based apps only):
- `restore_session` (bool, required) — `true` restores last session; `false` opens a fresh window.
- `urls` (string[], optional) — URLs to open. With `restore_session: true`, they open as extra tabs.

| `restore_session` | `urls`   | Result                                          |
|-------------------|----------|-------------------------------------------------|
| `true`            | present  | Last session restored + URLs open as extra tabs |
| `true`            | absent   | Last session restored, nothing extra            |
| `false`           | present  | Fresh window with only the specified URLs       |
| `false`           | absent   | Fresh empty window                              |

**Available presets:**
`full`, `left-half`, `right-half`, `top-half`, `bottom-half`,
`top-left`, `top-right`, `bottom-left`, `bottom-right`,
`left-third`, `center-third`, `right-third`,
`left-two-thirds`, `right-two-thirds`

## Capture Review Wizard (`capture_ui.py`)

Minimal Tkinter UI. Two screens only:

1. **Review screen** — one row per detected app. Per app: remove it, toggle browser restore session, set URLs (browser apps), set folder/args (editor apps like VS Code/Cursor). Monitor and preset are shown but not editable here (edit JSON for that).
2. **Save screen** — set profile name, optional hotkey, optional message. Writes to `profiles.json`.

Do not add general profile editing to this UI. Keep it capture-only.

## Dependencies

See `requirements.txt`. Key packages:
- `sounddevice` — audio streaming (WASAPI)
- `pynput` — global hotkeys
- `pystray` + `Pillow` — tray icon
- `pywin32` — window positioning
- `psutil` — process introspection
- `vosk` — optional, offline voice recognition

Do not add/remove/upgrade dependencies without approval.

## Running

```bash
python wakeup.py
```

Requires running terminal as Administrator at least once (pynput global hotkeys need elevated rights).

## Tests

Tests live in `tests/`. Run with:
```bash
python -m pytest tests/
```

Scope: preset math (window coordinate calculations) and schema validation only.

## Roadmap

- Phase 1 — Profile-based launcher (hotkey + voice keywords)
- Phase 2 — Window arrangement with multi-monitor support
- Phase 3 — Capture-based mode creation (snapshot desktop → review → save)
