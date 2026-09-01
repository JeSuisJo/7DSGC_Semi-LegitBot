from ... import console, prompts
from .fight import enter_battle, fight, launch

TITLE = "Legendary boss farming"


def prepare():
    console.banner(TITLE)
    return (prompts.ask_int("How many times do you want to farm? "),)


def run(num_times):
    launch()

    for run_number in range(1, num_times + 1):
        enter_battle(f"Farming the boss {num_times} times", run_number, num_times)
        fight(is_last_run=run_number == num_times)
