"""Claim finished expeditions and send the team back out."""

import time

from ... import console, screen
from ...config import get_config

TITLE = "Expeditions"

# Which bonus to pick is read from config.json ("expedition_items").
ITEMS = {
    "atk": "expedition_items_atk",
    "def": "expedition_items_def",
    "hp": "expedition_items_pv",
    "crit_chance": "expedition_items_cc",
    "crit_res": "expedition_items_cr",
    "recovery": "expedition_items_rec",
}

# The last two sit below the fold, so the list has to be scrolled down first.
ITEMS_BELOW_THE_FOLD = ("crit_res", "recovery")

DEFAULT_ITEM = "atk"


def run_expeditions(title=TITLE):
    console.banner(title)

    screen.go_to_hub()

    print("Expeditions")
    screen.tap("expedition_button")
    time.sleep(1)

    screen.tap_until_any("unblock", "expedition_screen", "take_reward", "expedition_not_finish")
    time.sleep(1.5)

    if screen.see("expedition_not_finish"):
        print("Expedition already")
        time.sleep(1.5)
        screen.tap("expedition_not_finish")
        time.sleep(2)
        screen.tap("back_home")
        return

    if not screen.see("expedition_screen"):
        print("Claim rewards")
        screen.tap("take_reward")
        time.sleep(3)
        screen.tap("unblock")
        time.sleep(1)
        screen.tap("unblock")

    screen.wait("expedition_screen")
    print("Auto Team")
    screen.tap("expedition_screen")
    time.sleep(1.5)
    print("Launch Expeditions")
    screen.tap("expedition_send_team")
    time.sleep(1.5)

    _choose_item()
    _handle_finish()


def _choose_item():
    choice = str(get_config().get("expedition_items", "")).strip().lower()

    if choice not in ITEMS:
        print(f"Unknown expedition_items '{choice}', taking {DEFAULT_ITEM}")
        choice = DEFAULT_ITEM

    print(f"Item : {choice}")

    screen.swipe_to("expedition_items_scroll_up")
    time.sleep(2)

    if choice in ITEMS_BELOW_THE_FOLD:
        screen.swipe_to("expedition_items_scroll_down")
        time.sleep(1.5)

    screen.tap(ITEMS[choice])
    time.sleep(1.5)
    screen.wait("expedition_items_confirm")
    time.sleep(1)
    screen.tap("expedition_items_confirm")


def _handle_finish():
    """Press through the send-off popups until the expedition list is back."""
    screen.tap_until("unblock", "expedition_not_finish")
    print("Back to the tavern")
    time.sleep(1.5)
    screen.tap("expedition_not_finish")
    time.sleep(2)
    screen.tap("back_home")
