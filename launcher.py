import os
import subprocess
import time


# Converts a browser block into Chromium CLI args.
def _browser_args(browser: dict) -> list[str]:
    restore = browser.get("restore_session", True)
    urls = browser.get("urls", [])
    args = []
    if not restore:
        args.append("--new-window")
    args.extend(urls)
    return args


# Waits for the app's delay, expands env vars, then spawns the process.
def spawn(app: dict) -> None:
    delay = app.get("delay", 0)
    if delay:
        time.sleep(delay)

    path = os.path.expandvars(app["path"])

    browser = app.get("browser")
    if browser is not None:
        args = _browser_args(browser)
    else:
        args = [os.path.expandvars(a) for a in app.get("args", [])]

    subprocess.Popen([path] + args)
