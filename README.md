# WakeUp — Personal Workspace Launcher

Your personal workspace launcher for Windows.

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> Run your terminal as Administrator once during first setup — `pynput`
> needs elevated rights to register global hotkeys.

### 2. Configure your profiles

The fastest way is to capture your current setup (see [Capture Mode](#capture-mode) below).

For manual editing, open `profiles.json` directly. Each profile follows this shape:

```json
"work": {
  "trigger_keywords": ["wake up", "work mode"],
  "hotkey": "ctrl+alt+w",
  "message": "Good morning.",
  "apps": [
    {
      "name": "VS Code",
      "path": "%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe",
      "args": ["C:/Projects"],
      "delay": 0,
      "window": { "monitor": 0, "preset": "left-two-thirds" }
    },
    {
      "name": "Chrome",
      "path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
      "delay": 0.5,
      "window": { "monitor": 0, "preset": "right-third" },
      "browser": { "restore_session": false, "urls": ["https://github.com"] }
    }
  ]
}
```

**Path tips**
- Use `%LOCALAPPDATA%`, `%APPDATA%`, `%PROGRAMFILES%` env vars freely
- Find exact paths: right-click any shortcut → Properties → Target

**`hotkey` and `message` are optional** — omit them if you don't need them.

**Window presets**
```
full             left-half / right-half    top-half / bottom-half
top-left / top-right / bottom-left / bottom-right
left-third / center-third / right-third
left-two-thirds / right-two-thirds
```

Or use exact pixel coords:
```json
"window": { "monitor": 0, "x": 0, "y": 0, "w": 1920, "h": 1080 }
```

**Monitor index**: 0 = primary, 1 = secondary, etc.

**Browser apps** use a `browser` block instead of `args`:
```json
"browser": { "restore_session": true, "urls": ["https://music.youtube.com"] }
```

### 3. Run

```bash
python wakeup.py
```

A tray icon appears in the taskbar. Right-click to launch any profile.

---

## Capture Mode

The fastest way to create a profile is to capture your current desktop:

1. Open the apps you want, arrange them on your monitors (don't minimize any)
2. Run: `python capture_ui.py`
3. Click **Capture** — WakeUp snapshots all open windows
4. Review the detected apps: remove any you don't want, set VS Code folder, add browser URLs
5. Name the profile, set an optional hotkey, click **Save**

The profile is written directly to `profiles.json`.

---

## Triggers

| Trigger | How |
|---------|-----|
| Hotkey | Press the hotkey defined in the profile |
| Tray menu | Right-click the tray icon → launch any profile |
| Voice keyword | Say any phrase in `trigger_keywords` (requires Vosk, see below) |

---

## Voice Commands (optional)

1. Uncomment `vosk` in `requirements.txt` and run `pip install vosk`
2. Download a model: https://alphacephei.com/vosk/models
   - Recommended: `vosk-model-small-en-us-0.15` (~50 MB)
3. Extract to `models/vosk-model-small-en-us`
4. In `profiles.json` → `settings.voice`:
   ```json
   "enabled": true,
   "model_path": "models/vosk-model-small-en-us"
   ```
5. Restart the app

---

## Auto-start with Windows

1. Press `Win + R` → type `shell:startup` → Enter
2. Drop a shortcut to `wakeup.py` (or a `.bat`) in that folder

`.bat` example:
```bat
@echo off
cd /d C:\path\to\WakeUp
python wakeup.py
```

---

## Project Structure

```
WakeUp/
├── wakeup.py          ← Entry point: tray icon, hotkeys, dispatches profiles
├── profile_runner.py  ← Executes a profile (spawns apps, triggers positioning)
├── launcher.py        ← Process spawning + browser arg handling
├── window_manager.py  ← Monitor detection, presets, win32 positioning
├── capture_service.py ← Desktop snapshot → draft app records
├── capture_ui.py      ← Minimal review wizard for captured apps
├── audio_engine.py    ← Optional Vosk voice keyword listener
├── profiles.json      ← Your configuration
├── requirements.txt
└── models/            ← Place Vosk models here (optional)
```

---

## Roadmap

- [x] Phase 1 — Profile-based app launcher (hotkey + voice keywords)
- [x] Phase 2 — Window arrangement with multi-monitor support
- [x] Phase 3 — Capture-based mode creation (snapshot current desktop → new profile)
