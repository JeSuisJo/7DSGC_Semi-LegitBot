"""Battle preparation reusing the settings of the previous run.

Once a run has configured auto-mode, later runs only need the auto button and
the start button, so this skips the whole config panel.
"""

import time

from .. import screen
from .preparation import start_battle


def battle_preparation_auto():
    screen.wait("battle_prep")

    print("Auto mode")
    screen.tap("battle_auto_button")
    time.sleep(2.5)

    start_battle()
