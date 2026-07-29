"""Platform-independent screen matching, on top of a driver's ``screenshot()``."""

import math
import os
import time
from contextlib import contextmanager
from functools import lru_cache

from PIL import Image, ImageChops

from ..paths import resolve


@lru_cache(maxsize=None)
def reference(path):
    """Return a reference image, decoded once and kept in memory."""
    return Image.open(resolve(path)).convert("RGB")


class StopScript(Exception):
    """Raised to abort a run cleanly (no ACT left, defeat, ...)."""

    def __init__(self, msg="Script stopped"):
        super().__init__(msg)


def similarity(img1, img2):
    """Return a 0..1 similarity score between two RGB images."""
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
    hist = ImageChops.difference(img1, img2).histogram()
    total = img1.size[0] * img1.size[1] * 3
    rms = math.sqrt(sum((i % 256) ** 2 * hist[i] for i in range(768)) / total) if total else 255
    return max(0.0, min(1.0, 1.0 - rms / 255.0))


class Driver:
    """Subclasses implement the transport; everything below is shared."""

    # ---------------- To implement ----------------

    def ensure_ready(self):
        """Resolve the target device. Called once before each run."""

    def screenshot(self, dest="temp.png"):
        raise NotImplementedError

    def tap(self, x, y):
        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, ms=300):
        raise NotImplementedError

    def write(self, text):
        raise NotImplementedError

    def enter(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    # ---------------- Frame ----------------

    _frozen = None

    def grab(self):
        """Return the screen as an RGB image, the frozen one inside a frame."""
        if self._frozen is not None:
            return self._frozen
        temp = self.screenshot()
        try:
            return Image.open(temp).convert("RGB")
        finally:
            _remove(temp)

    @contextmanager
    def frame(self):
        """Capture once and answer every match in the block from that capture.

        Never wait inside a frame: the image never changes, so ``wait_*`` would
        spin forever.
        """
        previous = self._frozen
        self._frozen = self.grab()
        try:
            yield
        finally:
            self._frozen = previous

    # ---------------- Image ----------------

    def compare_image(self, reference_path, region, threshold=0.95):
        shot = self.grab().crop(tuple(region))
        return similarity(shot, reference(reference_path)) >= threshold

    def wait_for_image(self, reference_path, region, threshold=0.9, poll=0.5):
        while not self.compare_image(reference_path, region, threshold):
            time.sleep(poll)

    def find_template(self, reference_path, region, threshold=0.9, scales=None):
        """Slide the reference over ``region``; return its centre or None.

        ``scales`` resizes the reference for a template captured at another
        resolution. The sweep stops at the first scale clearing ``threshold``.
        """
        import cv2
        import numpy as np

        if scales is None:
            scales = (1.0, 0.9, 0.8, 0.7, 0.6, 0.5)

        shot = self.grab().crop(tuple(region))
        haystack = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
        ref = cv2.cvtColor(np.array(reference(reference_path)), cv2.COLOR_RGB2BGR)

        h_h, h_w = haystack.shape[:2]
        best_score, best_loc = -1.0, None
        for scale in scales:
            tw, th = int(ref.shape[1] * scale), int(ref.shape[0] * scale)
            if tw < 1 or th < 1 or tw > h_w or th > h_h:
                continue
            template = cv2.resize(ref, (tw, th), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(haystack, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(result)
            if score > best_score:
                cx = region[0] + loc[0] + tw // 2
                cy = region[1] + loc[1] + th // 2
                best_score, best_loc = score, (cx, cy)
            if best_score >= threshold:
                break

        return best_loc if best_score >= threshold else None

    def wait_for_template(self, reference_path, region, threshold=0.9, poll=0.5, scales=None):
        while True:
            found = self.find_template(reference_path, region, threshold, scales)
            if found is not None:
                return found
            time.sleep(poll)

    # ---------------- Colour ----------------

    def get_color(self, x, y):
        return self.grab().getpixel((x, y))

    def is_color(self, x, y, target, tolerance=10):
        return all(abs(a - b) <= tolerance for a, b in zip(self.get_color(x, y), target))

    def has_color(self, region, target, tolerance=10):
        """True when at least one pixel of ``region`` matches ``target``.

        For a marker whose exact spot inside its card is not fixed.
        """
        low = [value - tolerance for value in target]
        high = [value + tolerance for value in target]
        return any(
            all(lo <= value <= hi for value, lo, hi in zip(pixel, low, high))
            for pixel in self.grab().crop(tuple(region)).getdata()
        )

    def wait_for_color(self, x, y, target, tolerance=10, poll=0.5):
        while not self.is_color(x, y, target, tolerance):
            time.sleep(poll)

    # ---------------- Control ----------------

    def stop(self, msg="Script stopped"):
        raise StopScript(msg)


def _remove(path):
    try:
        os.remove(path)
    except OSError:
        pass
