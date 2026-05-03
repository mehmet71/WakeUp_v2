import json
import sys

import profile_runner


# Reads and parses profiles.json from the working directory.
def load_profiles() -> dict:
    with open("profiles.json") as f:
        return json.load(f)


# Entry point: loads profiles, handles --run dev flag, or blocks waiting for triggers.
def main() -> None:
    data = load_profiles()
    profiles = data["profiles"]

    args = sys.argv[1:]

    if args and args[0] == "--run":
        if len(args) < 2:
            print("Usage: python wakeup.py --run <profile>")
            sys.exit(1)
        name = args[1]
        if name not in profiles:
            print(f"Profile '{name}' not found. Available: {', '.join(profiles)}")
            sys.exit(1)
        profile_runner.run(profiles[name])
        return

    print(f"WakeUp loaded. Profiles: {', '.join(profiles)}")
    print("Waiting for triggers... (press Ctrl+C to exit)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting.")


if __name__ == "__main__":
    main()
