import time

from ... import console, screen


def launch():
    time.sleep(1)
    print("Launching the boss")
    screen.tap("lb_start")
    time.sleep(3)

    if screen.see("no_act"):
        print("No stamina, refill potions")
        screen.tap("refill_act")
        time.sleep(1.5)
        print("Restarting the boss")
        screen.tap("lb_start")
        time.sleep(1.7)


def enter_battle(title, run_number, total):
    while True:
        console.banner(title, f"Run {run_number}/{total}")

        time.sleep(1.5)
        if screen.see("no_act"):
            print("No stamina, refill potions")
            screen.tap("refill_act")
            time.sleep(1.5)

        if screen.see("lb_in_battle"):
            return

        screen.tap("lb_screen_tap")
        time.sleep(1)


def fight(is_last_run):
    while True:
        if screen.see("lb_finish"):
            if is_last_run:
                print("Finished farming the boss")
                time.sleep(1)
                screen.tap("lb_exit")
                return

            print("Restarting the boss")
            screen.tap("lb_restart")
            time.sleep(1.5)
            return

        if screen.see("lb_auto", threshold=0.98):
            screen.tap("lb_auto_toggle")
            time.sleep(1.5)

        screen.tap("lb_screen_tap")

        if screen.see("lb_loss"):
            screen.stop("Defeat")
        time.sleep(1)
