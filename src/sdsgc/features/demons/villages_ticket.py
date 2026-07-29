"""Clear the six villages in one go by spending auto-clear tickets."""

import time

from ... import console, screen
from .clear import VILLAGES, villages_to_farm
from .stars import select_stars


def run_villages_ticket(stars, title, skip_done=False):
    """Tick every free village, then fire the single multi-village clear.

    The multi-clear already leaves the finished villages out, so ``skip_done``
    only serves to spot the run where all six are finished; it returns False
    then, and the caller drops the demon clearing that would follow.
    """
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

    # Each village has its own tick box; an unlit box means it is not selected.
    # Only the free ones are worth a ticket, so the occupied ones are unticked
    # when the game left them selected. One capture reads all six boxes.
    with screen.frame():
        to_toggle = [
            village
            for village in VILLAGES
            if screen.is_color(f"village_{village}_ticket") != (village in free)
        ]

    for village in to_toggle:
        print(f"{'Selected' if village in free else 'Unselected'} village {village}")
        screen.tap(f"village_{village}_ticket")
        time.sleep(1)

    print("Clear all 6 villages")
    screen.tap("clear_all_villages")
    time.sleep(2)

    # Being sent home instead of into the clear means there was nothing to
    # spend: no ACT and no potions left.
    if screen.see("home"):
        screen.stop("No more ACT and no more potions")

    screen.wait_color("clear_finished_ok")
    print("Clear finished")
    screen.tap("clear_finished_ok")
    time.sleep(1)
    return True
