"""Navigate from the tavern to the boss menu."""

import time

from ... import screen


def go_to_boss_menu():
    screen.go_to_hub()

    print("Boss menu")
    screen.tap("boss_menu_button")
    time.sleep(1)

    screen.wait("boss_menu")
