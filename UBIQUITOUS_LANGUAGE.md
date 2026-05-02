# Ubiquitous Language — WakeUp

## Profiles

| Term | Definition | Aliases to avoid |
|------|------------|-----------------|
| **Profile** | A named configuration that defines which apps to launch and how to arrange them | Mode, setup, workspace, config |
| **App entry** | A single app defined inside a profile, including its path, args, delay, and window config | App, application, item |
| **Window config** | The monitor and position settings for an app entry (`monitor`, `preset`, or `x/y/w/h`) | Layout, position, placement |
| **Preset** | A named window region (e.g. `left-half`, `full`) that maps to pixel coordinates on a monitor | Layout preset, snap, region |
| **Browser block** | The optional `browser` key on an app entry that controls session restore and URLs for Chromium apps | Browser config, browser args |
| **Args** | Command-line arguments passed to non-browser app entries at launch | Params, flags, arguments |

## Triggers

| Term | Definition | Aliases to avoid |
|------|------------|-----------------|
| **Trigger** | Any mechanism that activates a profile (hotkey, voice keyword, or tray menu selection) | Activation, invoke, fire |
| **Hotkey** | A global keyboard shortcut bound to a specific profile | Shortcut, keybind, keyboard trigger |
| **Voice keyword** | A spoken phrase that activates a profile when recognized by the voice engine | Voice command, trigger word, speech trigger |
| **Tray menu** | The right-click menu on the system tray icon listing all profiles for manual launch | System tray, tray icon menu |

## Capture Flow

| Term | Definition | Aliases to avoid |
|------|------------|-----------------|
| **Capture** | A snapshot of all currently open, visible windows — their executables, positions, and monitors | Desktop snapshot, scan, detect |
| **Draft** | An intermediate app record produced by a capture, before the user reviews and confirms it | Candidate, suggestion, detected app |
| **Review wizard** | The minimal UI where the user inspects drafts, removes unwanted apps, and fills in details before saving | Review step, capture UI, wizard |
| **Save** | The action of writing a reviewed profile to `profiles.json` | Commit, confirm, apply |

## Execution

| Term | Definition | Aliases to avoid |
|------|------------|-----------------|
| **Launch** | The act of executing a profile — spawning its app entries and arranging their windows | Run, activate, start, execute |
| **Window arrangement** | The async process of moving and resizing a spawned app's window to its configured position | Positioning, snapping, layout |
| **Restore session** | Browser behavior where the previous session tabs are reopened instead of a fresh window | Resume session, last session |

## Flagged Ambiguities

- **"Mode" vs "Profile"** — used interchangeably throughout the docs and UI (e.g. "work mode", "New mode button", but `profiles.json` and `profile_runner`). **Canonical term: Profile.** "Mode" is natural in user-facing copy ("work mode" as a label) but should not appear in code, JSON keys, or technical docs. The JSON key stays `profiles`.

- **"Trigger" as noun and verb** — "trigger a profile" (verb) and "voice trigger" (noun) both appear. Acceptable: use **trigger** as a noun for the mechanism, and **launch** as the verb for executing a profile. Avoid "trigger a profile" — say "launch a profile via a trigger".

- **"App" alone** — used loosely to mean the WakeUp app itself, a running process, and an app entry in a profile. Prefer **app entry** when referring to the JSON configuration object, **process** when referring to a running executable, and **WakeUp** when referring to the tool itself.

- **"Capture" as noun and verb** — "run a capture" (noun) and "capture the desktop" (verb) are both fine. Avoid "snapshot" as a synonym — it's not used in code.

## Example dialogue

> **Dev:** "When a user presses `Ctrl+Alt+W`, what exactly fires?"
>
> **Domain expert:** "The **hotkey** is a **trigger**. It calls `profile_runner.run()` with the matching **profile**. The runner iterates the **app entries**, spawns each process, then hands off to the window manager for **window arrangement**."
>
> **Dev:** "What if the user wants Chrome to open with their previous tabs?"
>
> **Domain expert:** "They set `restore_session: true` in the **browser block** on that **app entry**. No `--new-window` flag is added, so Chrome restores its last session naturally."
>
> **Dev:** "And for a new profile — do they have to write JSON by hand?"
>
> **Domain expert:** "No — they arrange their apps, run a **capture**, and the **review wizard** shows them each **draft**. They remove what they don't want, fill in the VS Code folder or browser URLs, then **save**. The wizard writes the **profile** to `profiles.json`."
>
> **Dev:** "So a **draft** is just an unconfirmed **app entry**?"
>
> **Domain expert:** "Exactly. A **draft** becomes an **app entry** once the user confirms it in the **review wizard**."
