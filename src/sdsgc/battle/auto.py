import time

from .. import screen
from .preparation import start_battle


def battle_preparation_auto():
    screen.wait("battle_prep")

    print("Auto mode")
    screen.tap("battle_auto_button")
    time.sleep(2.5)

    start_battle()
