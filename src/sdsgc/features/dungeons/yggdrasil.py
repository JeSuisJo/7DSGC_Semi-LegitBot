"""Run the Yggdrasil dungeon at the configured level and memory."""

import time

from ... import console, screen
from ...battle import run_battle_preparation, run_battle_preparation_ticket
from ...config import get_config

TITLE = "Yggdrasil"

LEVELS = {
    "blue": "yggdrasil_blue",
    "yellow": "yggdrasil_yellow",
    "red": "yggdrasil_red",
}

MEMORIES = {str(n): f"yggdrasil_memory_{n}" for n in range(1, 6)}


def run_yggdrasil(title=TITLE):
    console.banner(title)
    config = get_config()

    screen.go_to_hub()

    print("Yggdrasil")
    screen.tap_found("yggdrasil_hub")
    time.sleep(1)

    screen.wait("yggdrasil_screen")

    level = LEVELS.get(str(config.get("yggdrasil_level")))
    if level:
        screen.tap(level)

    screen.wait("yggdrasil_difficulty_screen")

    memory = MEMORIES.get(str(config.get("yggdrasil_memory")))
    if memory:
        screen.tap(memory)

    if config.is_true("daily_use_ticket"):
        run_battle_preparation_ticket()
    else:
        run_battle_preparation()

    screen.wait_home()

    print("Return to the tavern")
    screen.tap("tavern_return")
