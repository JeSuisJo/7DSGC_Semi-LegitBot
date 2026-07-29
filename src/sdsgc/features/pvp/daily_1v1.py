"""Daily 1v1 PvP: run matches until the tickets are gone."""

import time

from ... import screen
from ...config import get_config


def daily_pvp():
    screen.wait_home()

    screen.tap("pvp_side_menu")
    time.sleep(1.5)

    if get_config().is_true("pvp_stuff"):
        print("Going to PvP (with equipment)")
        screen.tap("pvp_menu_with_gear")
    else:
        print("Going to PvP (no equipment)")
        screen.tap("pvp_menu_no_gear")
    time.sleep(1)

    screen.wait_or_tap_color("pvp_screen", "placement_game_finish", "pvp_screen_confirm", tolerance=15)
    print("Preparing to use all tickets")

    _fight_until_out_of_tickets()

    screen.wait_home()
    time.sleep(1.5)


def _fight_until_out_of_tickets():
    while True:
        # The buy-tickets prompt comes in two artworks depending on whether
        # any diamonds are left; either one means we are done.
        time.sleep(1.5)
        if screen.see_any_template("pvp_no_tickets", "pvp_no_tickets_alt"):
            print("No more PvP tickets")
            screen.tap("pvp_no_tickets_close")
            time.sleep(1.5)
            screen.tap("ok_end")
            return

        screen.tap("pvp_fight")

        if screen.see("pvp_screen"):
            time.sleep(1)
            screen.tap("pvp_start")
            time.sleep(1.5)

        if screen.see("auto_fight"):
            time.sleep(1)
            screen.tap("auto_fight_toggle")
            time.sleep(1)
            _run_match()

        if screen.see("pvp_rank_up"):
            screen.tap("pvp_rank_up_ok")
            time.sleep(1)

        if screen.see("pvp_finish"):
            time.sleep(1)
            screen.tap("pvp_finish_ok")
            time.sleep(1.5)

        screen.tap_if_color("placement_game", tolerance=15)

        screen.tap_if_color("placement_game_finish", tolerance=15)

        time.sleep(1)


def _run_match():
    """Tap through one auto-fought match until its result is dismissed."""
    while True:
        if screen.see("pvp_leave"):
            time.sleep(1)
            screen.tap("pvp_leave_ok")

        # Read the finish state before tapping: the tap may dismiss it.
        finished = screen.see("pvp_finish")
        screen.tap("pvp_battle_tap")

        if finished:
            time.sleep(1)
            screen.tap("pvp_finish_ok")
            time.sleep(1.5)
            return

        time.sleep(1)
