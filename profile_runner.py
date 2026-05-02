import launcher


def run(profile: dict) -> None:
    message = profile.get("message")
    if message:
        print(message)

    for app in profile.get("apps", []):
        launcher.spawn(app)
