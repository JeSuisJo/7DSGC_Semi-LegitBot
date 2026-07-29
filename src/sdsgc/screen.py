"""Semantic screen interactions: map named coordinates to driver actions."""

import time

from .coords import coords
from .driver import driver


def frame():
    """Answer every check in the ``with`` block from a single capture.

    Never around a ``wait_*``: the image can no longer change.
    """
    return driver.frame()


def tap(name):
    driver.tap(*coords(name)["tap"])


def swipe_to(name):
    driver.swipe(*coords(name)["swipe"])


def see(name, threshold=0.9):
    block = coords(name)
    return driver.compare_image(block["img"], block["region"], threshold)


def wait(name, threshold=0.9, poll=0.5):
    block = coords(name)
    driver.wait_for_image(block["img"], block["region"], threshold, poll)


def find(name, threshold=0.9, scales=None):
    """Template-match the named image in its region; return its centre or None.

    Unlike :func:`see`, the reference may be smaller than the region.
    """
    block = coords(name)
    return driver.find_template(block["img"], block["region"], threshold, scales)


def see_template(name, threshold=0.9, scales=None):
    return find(name, threshold, scales) is not None


def wait_template(name, threshold=0.9, poll=0.5, scales=None):
    """Block until the template is found; return its centre.

    The one to use when the reference is smaller than its region: :func:`wait`
    stretches the reference to fill the region, so it would spin forever.
    """
    block = coords(name)
    return driver.wait_for_template(block["img"], block["region"], threshold, poll, scales)


def see_any_template(*names, threshold=0.9, scales=None):
    with driver.frame():
        return any(see_template(name, threshold, scales) for name in names)


def tap_found(name, dx=0, dy=0, threshold=0.9, poll=0.5, scales=None):
    """Wait for the named element, then tap where it matched, shifted by dx/dy.

    For targets that appear at varying spots inside their region.
    """
    block = coords(name)
    x, y = driver.wait_for_template(block["img"], block["region"], threshold, poll, scales)
    x, y = x + dx, y + dy
    driver.tap(x, y)
    return (x, y)


def sample_point(block):
    """Where to read the colour: ``rgb_at`` when the probe differs from the tap."""
    return block.get("rgb_at", block["tap"])


def is_color(name, tolerance=10):
    block = coords(name)
    x, y = sample_point(block)
    return driver.is_color(x, y, block["rgb"], tolerance)


def wait_color(name, tolerance=10, poll=0.5):
    block = coords(name)
    x, y = sample_point(block)
    driver.wait_for_color(x, y, block["rgb"], tolerance, poll)


def has_color_at(name, region_name, tolerance=10):
    """True when ``name``'s colour shows up anywhere inside ``region_name``.

    Two entries because the same colour is looked for in several regions.
    """
    return driver.has_color(coords(region_name)["region"], coords(name)["rgb"], tolerance)


def see_at(image_path, region_name, threshold=0.9):
    """Match an explicit image inside a named region, for references picked at runtime."""
    return driver.compare_image(image_path, coords(region_name)["region"], threshold)


def find_at(image_path, region_name, threshold=0.9, scales=None):
    """Template twin of :func:`see_at`; returns the match centre or None."""
    return driver.find_template(image_path, coords(region_name)["region"], threshold, scales)


def see_any_at(image_paths, region_name, threshold=0.9, scales=None):
    with driver.frame():
        return any(
            find_at(path, region_name, threshold, scales) is not None for path in image_paths
        )


def see_any(*names, threshold=0.9):
    with driver.frame():
        return any(see(name, threshold) for name in names)


def wait_any(*names, threshold=0.9, poll=0.5):
    while not see_any(*names, threshold=threshold):
        time.sleep(poll)


def _tap_until(name, arrived, poll):
    while not arrived():
        tap(name)
        time.sleep(poll)


def tap_until(name, target, threshold=0.9, poll=0.5):
    """Tap ``name`` until ``target`` shows up. Blocks forever."""
    _tap_until(name, lambda: see(target, threshold), poll)


def tap_until_any(name, *targets, threshold=0.9, poll=0.5):
    """Tap ``name`` until any of ``targets`` shows up. Blocks forever."""
    _tap_until(name, lambda: see_any(*targets, threshold=threshold), poll)


def tap_until_color(name, target, tolerance=10, poll=0.5):
    """Tap ``name`` until ``target``'s probe pixel matches its ``rgb``."""
    _tap_until(name, lambda: is_color(target, tolerance), poll)


def tap_if_color(name, tolerance=10):
    """Tap ``name`` once if its probe pixel matches its ``rgb``. Returns True if it tapped."""
    if is_color(name, tolerance):
        tap(name)
        return True
    return False


def wait_or_tap_color(target, *buttons, threshold=0.9, tolerance=10, poll=0.5):
    """Block until ``target`` is on screen, tapping any ``buttons`` in the way."""
    while True:
        with driver.frame():
            if see(target, threshold):
                return
            pending = [button for button in buttons if is_color(button, tolerance)]
        for button in pending:
            tap(button)
            time.sleep(poll)
        time.sleep(poll)


def wait_home(poll=0.5):
    """Block until the tavern home button is up, tapping ``unblock`` to clear popups."""
    tap_until("unblock", "home", poll=poll)


def go_to_hub(poll=0.5):
    """Walk from the tavern to the hub, the screen every mode starts from."""
    wait_home(poll=poll)

    print("Menu")
    tap("menu_button")
    time.sleep(1)

    wait("hub")


def write(text):
    driver.write(text)


def enter():
    driver.enter()


def delete():
    driver.delete()


def stop(msg="Script stopped"):
    driver.stop(msg)
