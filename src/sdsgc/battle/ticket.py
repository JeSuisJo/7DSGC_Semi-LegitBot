import time

from .. import screen


def run_battle_preparation_ticket():
    screen.wait("battle_prep")

    print("Ticket menu")
    screen.tap("ticket_menu_button")
    time.sleep(1)

    screen.wait_color("ticket_menu_ok")

    while not screen.is_color("ticket_max"):
        screen.tap("ticket_max")
        print("Clicking for the maximum tickets use")
        time.sleep(1)

    print("Starting level with tickets")
    screen.tap("ticket_start")
    time.sleep(1.5)

    if screen.see("no_potions"):
        screen.stop("No more ACT and no more potions")

    screen.tap_until("ticket_skip", "in_menu")
    print("Level finished")

    time.sleep(1.5)
    print("Return")
    screen.tap("ticket_back")
    time.sleep(1)
