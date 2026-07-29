"""Detect which demon sits in each village, then clear them one by one."""

import time
from collections import Counter

from ... import console, screen
from ...coords import demon_image
from .fight import fight_demon

DEMON_NAMES = ["bellmoth", "grey", "howlex", "indura", "red", "original_demon"]
VILLAGES = range(1, 7)


def detect_demons_in_villages():
    """Return ``{village: demon_name or None}`` for the six villages."""
    if screen.is_color("multi_clear_disabled"):
        print("Activated achievement auto")
        screen.tap("multi_clear_disabled")
        time.sleep(1)

    detected = {}
    # One capture answers all 36 thumbnail comparisons.
    with screen.frame():
        for village in VILLAGES:
            slot = f"village_{village}_slot"
            match = None
            for demon_name in DEMON_NAMES:
                if screen.see_at(demon_image(village, demon_name), slot):
                    match = demon_name
                    break
            detected[village] = match
            print(f"Village {village}: {match if match else 'No demon detected'}")
    return detected


def free_villages():
    """Return the villages holding no demon yet, in order.

    A village that already spawned a demon keeps its slot taken until that
    demon is cleared, so farming it is wasted ACT.
    """
    return [village for village, demon in detect_demons_in_villages().items() if demon is None]


def done_villages():
    """Return the villages already finished, in order.

    Two and three star villages cap the clears per day: once a village hits
    that cap it keeps its marker until the daily reset and cannot be farmed
    again. One star has no cap and never shows the marker.
    """
    with screen.frame():
        done = [
            village
            for village in VILLAGES
            if screen.has_color_at("village_done", f"village_{village}_done")
        ]
    for village in done:
        print(f"Village {village}: already finished")
    return done


def villages_to_farm(skip_done=False):
    """Return the villages worth entering, or ``None`` when all are finished.

    ``None`` is the case where the whole chore is pointless: no village can be
    farmed and no demon can spawn, so the caller has nothing left to clear.
    """
    done = done_villages() if skip_done else []
    if len(done) == len(VILLAGES):
        return None
    return [village for village in free_villages() if village not in done]


def clear_demons(target_demons=None):
    """Fight one demon per distinct kind found, most frequent first.

    A single fight clears every village holding that demon, so only the first
    village of each kind is entered.
    """
    detected = detect_demons_in_villages()

    if target_demons:
        found = {v: d for v, d in detected.items() if d in target_demons}
    else:
        found = {v: d for v, d in detected.items() if d is not None}

    if not found:
        print("\nNo demons detected to clear.")
        return

    ordered = [name for name, _ in Counter(found.values()).most_common()]

    for demon_name in ordered:
        village = next(v for v, d in found.items() if d == demon_name)
        console.banner(f"Clear demons : {demon_name}")
        screen.tap(f"village_{village}_slot")
        time.sleep(1)
        fight_demon(demon_name)

    print("\nAll demons cleared!")
