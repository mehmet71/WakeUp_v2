import os
import subprocess
import time


def spawn(app: dict) -> None:
    delay = app.get("delay", 0)
    if delay:
        time.sleep(delay)

    path = os.path.expandvars(app["path"])
    args = [os.path.expandvars(a) for a in app.get("args", [])]

    subprocess.Popen([path] + args)
