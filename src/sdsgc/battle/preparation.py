import time

from .. import screen

REPEATS = 8


def run_battle_preparation(repeats=None):
    screen.wait("battle_prep")

    print("Battle preparation configuration")
    screen.tap("battle_config_button")

    screen.wait_color("battle_config_ok")

    _toggle_on(
        "auto_potion_off",
        "auto_potion_on",
        "Potions automatically activated",
        "Potions already activated",
    )
    if repeats is None:
        _toggle_on(
            "repeat_infinite_off",
            "repeat_infinite_on",
            "Level repetitions set to infinite",
            "Level repetitions already set to infinite",
        )
    else:
        _set_repeat_count(repeats)

    time.sleep(1)
    print("Saving configuration")
    screen.tap("battle_config_ok")

    time.sleep(1.5)
    start_battle()


def run_battle_preparation_equipment(repeats=REPEATS):
    run_battle_preparation(repeats)


def _set_repeat_count(repeats):
    while True:
        with screen.frame():
            off = screen.is_color("repeat_count_off")
            on = screen.is_color("repeat_count_on")
        if off:
            screen.tap("repeat_count_off")
            time.sleep(1)
            break
        if on:
            break
        time.sleep(1)

    screen.tap("repeat_count_field")
    time.sleep(1)

    screen.delete()
    time.sleep(0.5)
    screen.delete()
    time.sleep(0.5)

    screen.write(str(repeats))
    screen.enter()
    time.sleep(0.5)
    print(f"Level repetitions set to {repeats}")


def start_battle():
    print("Starting battle")
    screen.tap("battle_start")
    time.sleep(2)

    if screen.see("no_act"):
        print("No more ACT, refill potions")
        screen.tap("refill_act")
        time.sleep(2)
        print("Restarting battle")
        screen.tap("battle_start")

    if screen.see("no_potions"):
        screen.stop("No more ACT and no more potions")


def _toggle_on(off_name, on_name, turned_on_msg, already_on_msg):
    while True:
        with screen.frame():
            off = screen.is_color(off_name)
            on = screen.is_color(on_name)
        if off:
            screen.tap(off_name)
            print(turned_on_msg)
            return
        if on:
            print(already_on_msg)
            return
        time.sleep(1)
