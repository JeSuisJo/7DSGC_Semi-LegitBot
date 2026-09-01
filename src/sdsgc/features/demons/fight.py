import time

from ... import screen
from ...config import get_config
from .boss_menu import go_to_boss_menu

DIFFICULTIES = {
    "easy": "demon_difficulty_easy",
    "hard": "demon_difficulty_hard",
    "extreme": "demon_difficulty_extreme",
    "hell": "demon_difficulty_hell",
}

DEFAULT_DIFFICULTY = "easy"


def fight_demon(demon_name):
    difficulty = _difficulty_for(demon_name)
    if difficulty is None:
        return

    screen.wait("demon_difficulty_menu")

    print(f"Selecting difficulty: {difficulty}")
    screen.tap(DIFFICULTIES[difficulty])
    time.sleep(1)

    _confirm_start()
    time.sleep(1.5)

    _wait_for_demon_menu(difficulty)
    _invite_ai_friend()

    screen.wait("demon_menu")

    print("Combat preparation")
    screen.tap("demon_battle_prep")
    time.sleep(1.5)
    screen.tap("demon_battle_prep")
    time.sleep(1)

    _enable_auto()

    if _wait_for_end() == "lost":
        _handle_defeat()
        return

    screen.wait_home()

    time.sleep(5)
    go_to_boss_menu()
    time.sleep(1)


def _difficulty_for(demon_name):
    configured = get_config().get("demon_difficulties", {}).get(demon_name)
    if not configured:
        print(
            f"Warning: No difficulty configured for demon '{demon_name}', "
            f"using '{DEFAULT_DIFFICULTY}' as default"
        )
        configured = DEFAULT_DIFFICULTY
    if configured not in DIFFICULTIES:
        print(f"Error: Unknown difficulty '{configured}' for demon '{demon_name}'")
        return None
    return configured


def _confirm_start():
    for name in ("demon_start_many", "demon_start_few"):
        if screen.is_color(name):
            print("Start the demon")
            screen.tap(name)
            time.sleep(1)


def _wait_for_demon_menu(difficulty):
    while True:
        with screen.frame():
            if screen.see("demon_menu"):
                return
            no_act = screen.see("no_act")
            no_potions = screen.see("no_potions")

        if no_act:
            print("No more ACT, refill potions")
            screen.tap("demon_refill_act")
            time.sleep(1.5)
            screen.tap(DIFFICULTIES[difficulty])
            time.sleep(1.5)
            _confirm_start()
            no_potions = screen.see("no_potions")

        if no_potions:
            screen.stop("No more ACT and no more potions")
        time.sleep(1)


def _invite_ai_friend():
    print("Add IA Friends")
    screen.tap("demon_invite_ai")
    time.sleep(2)

    while True:
        with screen.frame():
            row = next(
                (
                    name
                    for name in ("demon_ai_friend_low", "demon_ai_friend_high")
                    if screen.is_color(name)
                ),
                None,
            )
        if row:
            print("IA Friends added")
            screen.tap(row)
            time.sleep(1)
            return
        time.sleep(1)


def _enable_auto():
    while not screen.see("auto_fight"):
        screen.tap("demon_screen_tap")
        time.sleep(1)
    print("Mode auto")
    screen.tap("auto_fight_toggle")


def _wait_for_end():
    screen.tap_until_any("unblock_demon", "demon_fight_end", "failed_demon")

    if screen.see("failed_demon"):
        print("Combat lost")
        return "lost"

    print("Combat finished")
    screen.tap("demon_fight_end_ok")
    return "won"


def _handle_defeat():
    time.sleep(1.5)
    screen.tap("ok_failed_demon")

    screen.wait("back_to_map")
    time.sleep(1.5)
    screen.tap("back_to_map")

    go_to_boss_menu()
