import os

import launcher
import window_manager


# Prints the profile message (if any), spawns all apps, then positions their windows simultaneously.
def run(profile: dict) -> None:
    message = profile.get("message")
    if message:
        print(message)

    pending = []
    for app in profile.get("apps", []):
        pid = launcher.spawn(app)
        if pid and "window" in app:
            exe_name = os.path.basename(os.path.expandvars(app["path"]))
            pending.append((pid, app["window"], exe_name))

    if pending:
        window_manager.position_all(pending)
