"""Clear one village without tickets: pick difficulty, fight, dismiss the demon."""

import time

from ... import screen
from ...battle import battle_preparation_auto, fight_pve, run_battle_preparation

DIFFICULTY_BUTTON = {
    "one_star": "village_last_difficulty_one_star",
    "multi_star": "village_last_difficulty_multi_star",
}


def cycle_village(star_mode, configure=True):
    """Run one village.

    ``configure`` fills in the battle config panel; later villages reuse the
    settings of the first one and only need auto mode.
    """
    screen.wait("village_difficulty")

    print("Last difficulty")
    screen.tap(DIFFICULTY_BUTTON[star_mode])
    time.sleep(1)

    if configure:
        run_battle_preparation()
    else:
        battle_preparation_auto()

    fight_pve()

    # The demon that spawned is announced by a dialog; dismissing it is what
    # returns us to the village list.
    screen.tap_until_color("unblock", "demon_appeared_cancel")
    time.sleep(1.5)
    print("Demon appeared")
    screen.tap("demon_appeared_cancel")
    time.sleep(1.5)


def skip_village():
    """Leave a village that already holds a demon, without fighting it.

    Opening it cannot be avoided: the "next" arrow only exists inside the
    village screen.
    """
    screen.wait("village_difficulty")

    print("Demon already here, village skipped")
    screen.tap("demon_appeared_cancel")
    time.sleep(1.5)
