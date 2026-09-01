import time

from ... import console, screen
from .clear import VILLAGES, villages_to_farm
from .stars import select_stars

TICKED = 20


def run_villages_ticket(stars, title, skip_done=False):
    console.banner(title)

    if screen.is_color("multi_achievement_disabled"):
        print("Activated achievement auto")
        screen.tap("multi_achievement_disabled")
        time.sleep(1)

    select_stars(stars)
    time.sleep(1.5)

    free = villages_to_farm(skip_done)
    if free is None:
        print("Every village is already finished, nothing to farm")
        return False
    if not free:
        print("Every village already holds a demon, nothing to farm")
        return True

    with screen.frame():
        to_toggle = [
            village
            for village in VILLAGES
            if screen.is_color(f"village_{village}_ticket", TICKED) != (village in free)
        ]

    for village in to_toggle:
        print(f"{'Selected' if village in free else 'Unselected'} village {village}")
        screen.tap(f"village_{village}_ticket")
        time.sleep(1)

    print("Clear all 6 villages")
    screen.tap("clear_all_villages")
    time.sleep(2)

    if screen.see("home"):
        screen.stop("No more ACT and no more potions")

    screen.wait_color("clear_finished_ok")
    print("Clear finished")
    screen.tap("clear_finished_ok")
    time.sleep(1)
    return True
