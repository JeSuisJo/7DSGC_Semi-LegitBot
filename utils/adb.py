import subprocess
import os
import json
import time
import math
from PIL import Image, ImageChops

# ---------------- Config ----------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADB = os.path.join(ROOT, "platform-tools", "adb.exe")

with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
    DEVICE = json.load(f).get("device_id")

# Chemin absolu depuis la racine du projet
def path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

class StopScriptException(Exception):
    def __init__(self, msg="Script stopped"):
        super().__init__(msg)

# ---------------- Interne ----------------
def _run(cmd):
    base = [ADB, "-s", DEVICE] if DEVICE else [ADB]
    r = subprocess.run(base + cmd, capture_output=True, text=True, timeout=30, cwd=ROOT)
    return r.returncode == 0

def _screenshot(dest="temp.png"):
    dest = path(dest)
    _run(["shell", "screencap", "-p", "/sdcard/tmp.png"])
    _run(["pull", "/sdcard/tmp.png", dest])
    _run(["shell", "rm", "/sdcard/tmp.png"])
    return dest

def _similarity(img1, img2):
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
    hist = ImageChops.difference(img1, img2).histogram()
    total = img1.size[0] * img1.size[1] * 3
    rms = math.sqrt(sum((i % 256) ** 2 * hist[i] for i in range(768)) / total) if total else 255
    return max(0.0, min(1.0, 1.0 - rms / 255.0))

# ---------------- Actions ----------------
def tap(x, y):
    _run(["shell", "input", "tap", str(x), str(y)])

def hold(x, y, ms=500):
    _run(["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(ms)])

def swipe(x1, y1, x2, y2, ms=300):
    _run(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms)])

def write(text):
    _run(["shell", "input", "text", text.replace(" ", "\\ ").replace("&", "\\&")])

def enter():
    _run(["shell", "input", "keyevent", "66"])

def delete():
    _run(["shell", "input", "keyevent", "67"])

def stop(msg="Script stopped"):
    raise StopScriptException(msg)

# ---------------- Image ----------------
def compare_image(reference_path, region, threshold=0.95):
    temp = _screenshot()
    shot = Image.open(temp).crop(region).convert("RGB")
    ref  = Image.open(path(reference_path)).convert("RGB")
    result = _similarity(shot, ref) >= threshold
    try: os.remove(temp)
    except OSError: pass
    return result

def wait_for_image(reference_path, region, threshold=0.9, poll=0.5):
    while not compare_image(reference_path, region, threshold):
        time.sleep(poll)

# ---------------- Couleur ----------------
def get_color(x, y):
    temp = _screenshot()
    color = Image.open(temp).convert("RGB").getpixel((x, y))
    try: os.remove(temp)
    except OSError: pass
    return color

def is_color(x, y, target, tolerance=10):
    return all(abs(a - b) <= tolerance for a, b in zip(get_color(x, y), target))

def wait_for_color(x, y, target, tolerance=10, poll=0.5):
    while not is_color(x, y, target, tolerance):
        time.sleep(poll)
