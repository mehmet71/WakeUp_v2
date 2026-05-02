# WakeUp v2 — Design Decisions

Decisions made during planning and implementation, in chronological order.

---

## 2026-05-03

### No general profile editor UI
**Decision:** The only UI in the app is the capture review wizard. Profiles are edited directly in `profiles.json`.
**Why:** The full Tkinter editor from v1 was the biggest contributor to code bloat. Most edits are done in JSON anyway. The capture wizard covers the hard case (creating a new profile from scratch).

---

### Capture wizard is the primary profile creation path
**Decision:** `capture_ui.py` handles only the capture → review → save flow. Nothing else.
**Why:** Capturing the current desktop is faster and less error-prone than manual JSON authoring. Keeping the wizard focused prevents it from growing into another general editor.

---

### Three trigger paths, one dispatch point
**Decision:** Hotkey, voice keyword, and tray menu all dispatch to the same `profile_runner.run(profile)` call.
**Why:** Keeps trigger logic separate from execution logic. Adding or removing a trigger type never touches the runner.

---

### `profile_runner.py` extracted from `wakeup.py`
**Decision:** Profile execution lives in its own module, not in the entry point.
**Why:** In v1, `wakeup.py` owned too much — tray, hotkeys, and execution logic. Extracting the runner gives each file one job.

---

### No `args` on browser app entries
**Decision:** Browser apps (Chromium-based) use the `browser` block (`restore_session`, `urls`) only. The `args` field is for non-browser apps.
**Why:** Having both `args` and `browser.urls` for the same app was a source of confusion in v1. One path per app type.

---

### `hotkey` and `message` are optional fields
**Decision:** Omit these fields entirely when not needed. Empty strings (`""`) are not valid.
**Why:** The v1 `profiles.json` had profiles with `"hotkey": ""` and `"message": ""`. Optional fields should be absent, not empty.

---

### Phase 4 (voice agent) is out of scope
**Decision:** Whisper STT + LLM + TTS is not part of this rebuild.
**Why:** It's a fundamentally different feature that would pull the architecture in a direction the core doesn't need. If it comes back, it plugs in on top.

---

### Stay with Python
**Decision:** The rebuild uses Python, same as v1.
**Why:** The mess in v1 was caused by unclear module boundaries, not the language. All the Windows integrations (win32, pynput, pystray, vosk) have solid Python support. Rewriting in another language would mean rewriting all of that for no structural gain.

---

### Tests scoped to preset math and schema validation only
**Decision:** No tests for tray, hotkeys, win32 calls, or UI.
**Why:** Those are integration/platform territory that isn't worth mocking. The two things worth testing are pure logic: coordinate calculations and config parsing.
