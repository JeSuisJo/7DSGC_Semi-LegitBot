import time

from ... import console, screen
from ...battle import run_battle_preparation, run_battle_preparation_ticket
from ...config import get_config

TITLE = "Special Dungeon"


def run_special_dungeon(title=TITLE):
    console.banner(title)

    screen.go_to_hub()

    print("Fort Solgales")
    screen.tap("fort_solgales")
    time.sleep(1)

    screen.wait("special_dungeon_menu")

    print("Special dungeon")
    screen.tap("special_dungeon_button")
    time.sleep(1)

    screen.tap_found("sara_arrow")
    screen.tap_found("last_level", dx=150)

    if get_config().is_true("daily_use_ticket"):
        run_battle_preparation_ticket()
    else:
        run_battle_preparation()

    screen.wait_home()

    print("Return to the tavern")
    screen.tap("special_dungeon_return")
    time.sleep(1)
