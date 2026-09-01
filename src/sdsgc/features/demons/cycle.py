import time

from ... import screen
from ...battle import battle_preparation_auto, fight_pve, run_battle_preparation

DIFFICULTY_BUTTON = {
    "one_star": "village_last_difficulty_one_star",
    "multi_star": "village_last_difficulty_multi_star",
}


def cycle_village(star_mode, configure=True):
    screen.wait("village_difficulty")

    print("Last difficulty")
    screen.tap(DIFFICULTY_BUTTON[star_mode])
    time.sleep(1)

    if configure:
        run_battle_preparation()
    else:
        battle_preparation_auto()

    fight_pve()

    screen.tap_until_color("unblock", "demon_appeared_cancel")
    time.sleep(1.5)
    print("Demon appeared")
    screen.tap("demon_appeared_cancel")
    time.sleep(1.5)


def skip_village():
    screen.wait("village_difficulty")

    print("Demon already here, village skipped")
    screen.tap("demon_appeared_cancel")
    time.sleep(1.5)
