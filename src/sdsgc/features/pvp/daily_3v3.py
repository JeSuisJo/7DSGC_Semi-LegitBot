import time

from ... import console, screen
from ...config import get_config

TITLE = "PVP"


def daily_3v3(title=TITLE):
    console.banner(title)

    screen.go_to_hub()

    screen.tap_found("pvp_hub")
    print("Go to 3V3")

    screen.wait_or_tap_color(
        "pvp_3v3_screen",
        "pvp_3v3_confirm_low",
        "pvp_3v3_confirm_high",
        "pvp_screen_confirm",
        tolerance=15,
    )
    time.sleep(4)

    _claim_reward("pvp_3v3_daily_reward", "Daily reward", tolerance=50)

    if get_config().is_true("only_reward_3v3"):
        print("Only taking the reward for the 3v3")
        screen.tap("pvp_3v3_back")
        return

    _spend_tickets()


def _claim_reward(name, label, tolerance):
    if screen.is_color(name, tolerance):
        print(f"{label} available")
        screen.tap(name)
        time.sleep(1.5)
        screen.tap(name)
        time.sleep(1.5)
    else:
        print(f"No {label.lower()} for now")
        time.sleep(1.5)


def _spend_tickets():
    while True:
        screen.tap("pvp_3v3_fight")
        time.sleep(1.5)

        screen.wait("pvp_3v3_in_battle")
        time.sleep(1.5)
        screen.tap("pvp_3v3_start")
        time.sleep(3)

        if screen.see("in_menu"):
            print("All tickets used")
            screen.tap("pvp_3v3_exit")
            _claim_win_reward()
            screen.tap("pvp_3v3_exit")
            time.sleep(1)
            return

        screen.wait("pvp_finish")
        time.sleep(1.5)
        screen.tap("pvp_3v3_finish_ok")

        screen.wait("pvp_3v3_screen")
        time.sleep(3.5)


def _claim_win_reward():
    print("Check if the win reward is available")
    time.sleep(1.5)
    _claim_reward("pvp_3v3_win_reward", "Win reward", tolerance=5)
