import time

from ... import console, prompts
from ...config import get_config
from .boss_menu import go_to_boss_menu
from .clear import clear_demons
from .stars import star_mode
from .villages import run_villages
from .villages_ticket import run_villages_ticket

TITLE = "Auto Demon Farm"
DAILY_TITLE = "Village Clear"
ONE_STAR = "1"
PAUSE = 0.5


def prepare():
    console.banner(TITLE)
    use_ticket = prompts.ask_yes_no("Do you want to farm with ticket?")
    num_times = prompts.ask_int("How many times do you want to farm? ")
    return use_ticket, num_times


def run(use_ticket, num_times):
    go_to_boss_menu()

    for _ in range(num_times):
        console.banner(TITLE)
        if use_ticket:
            run_villages_ticket(ONE_STAR, TITLE)
        else:
            run_villages(ONE_STAR, TITLE)
        clear_demons()


def run_daily(title=DAILY_TITLE):
    config = get_config()
    stars = config.get("daily_demon_stars")

    skip_done = star_mode(stars) == "multi_star"

    go_to_boss_menu()
    time.sleep(PAUSE)

    walk = run_villages_ticket if config.is_true("daily_demon_ticket") else run_villages
    if not walk(stars, title, skip_done=skip_done):
        return

    time.sleep(PAUSE)
    clear_demons()
