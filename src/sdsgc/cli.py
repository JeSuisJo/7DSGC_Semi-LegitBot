"""Interactive menu: choose and launch an automation mode."""

import traceback

from . import console
from .driver import StopScript, driver
from .features.registry import FEATURES

TITLE = "7DSGC SemiLegit-Bot"


def _print_menu():
    console.banner(TITLE)
    for key, feature in FEATURES.items():
        print(f"[{key}] {feature.label}")
    print("[0] Exit")
    print()


def main():
    while True:
        _print_menu()

        try:
            choice = input("Enter your choice: ").strip()
        except KeyboardInterrupt:
            print()
            console.info("Interrupted by user")
            return

        if choice == "0":
            return

        feature = FEATURES.get(choice)
        if feature is None:
            console.error(f"Invalid choice, enter a number between 0 and {len(FEATURES)}")
            input("\nPress Enter to return to the menu...")
            continue

        _run(feature)


def _run(feature):
    """Run one feature, keeping the menu alive whatever it raises."""
    try:
        # Resolve the emulator first: a mode that cannot reach a device should
        # fail here, not halfway through asking the user for its settings.
        driver.ensure_ready()
        args = feature.prepare() if feature.prepare else ()
        feature.run(*args)
    except StopScript as exc:
        print()
        console.warn(f"{exc}")
        console.info("Script stopped by user or automation condition")
    except KeyboardInterrupt:
        print()
        console.info("Interrupted by user")
    except Exception as exc:  # noqa: BLE001 - the menu must survive any mode
        console.error(f"Error during execution: {exc}")
        traceback.print_exc()

    input("\nPress Enter to return to the menu...")
