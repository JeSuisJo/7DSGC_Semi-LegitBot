import re
import subprocess
import time

from .. import config as config_module
from ..paths import PROJECT_ROOT, resolve
from ..prompts import ask_from_list
from .base import Driver

ADB = resolve("platform-tools/adb.exe")


class AdbDriver(Driver):
    def __init__(self, device_id=None):
        if device_id is None:
            device_id = config_module.get_config().get("device_id")
        self.device_id = device_id

    def ensure_ready(self):
        configured = config_module.get_config().get("device_id")

        if configured and self._is_online(configured):
            self.device_id = configured
            return

        devices = self.list_devices()

        if len(devices) == 1:
            self._use_device(devices[0], "ADB device auto-selected")
            return

        if not devices:
            print("No ADB device found, restarting ADB server...")
            self._restart_server()
            devices = self.list_devices()
            if configured and configured in devices:
                self.device_id = configured
                return
            if len(devices) == 1:
                self._use_device(devices[0], "ADB device auto-selected")
                return

        if not devices:
            self.stop("No emulator detected. Start your emulator, then try again.")

        self._use_device(self._ask_device(devices), "ADB device selected")

    @staticmethod
    def list_devices():
        try:
            result = subprocess.run(
                [ADB, "devices"], capture_output=True, text=True, timeout=10
            )
        except (subprocess.SubprocessError, OSError):
            return []
        lines = result.stdout.strip().split("\n")[1:]
        return [line.split("\t")[0] for line in lines if "\tdevice" in line]

    @staticmethod
    def _restart_server():
        subprocess.run([ADB, "kill-server"], capture_output=True, timeout=10)
        time.sleep(1.5)
        subprocess.run([ADB, "start-server"], capture_output=True, timeout=15)
        time.sleep(2)

    @staticmethod
    def _is_online(device_id):
        try:
            result = subprocess.run(
                [ADB, "-s", device_id, "get-state"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (subprocess.SubprocessError, OSError):
            return False
        return result.returncode == 0 and result.stdout.strip() == "device"

    @classmethod
    def _ask_device(cls, devices):
        labels = [cls._describe(device) for device in devices]
        return devices[ask_from_list("Multiple devices connected:", labels) - 1]

    @classmethod
    def _describe(cls, device_id):
        app = cls._foreground_app(device_id)
        return f"{device_id} - {app}" if app else device_id

    @classmethod
    def _foreground_app(cls, device_id):
        dump = cls._probe(device_id, ["dumpsys", "activity", "activities"])
        found = re.findall(
            r"ResumedActivity[:=]\s*ActivityRecord\{\S+ \S+ (\S+)/(\S+)", dump
        )
        for package, activity in found:
            if "launcher" not in f"{package}/{activity}".lower():
                return package
        return found[0][0] if found else ""

    @staticmethod
    def _probe(device_id, cmd):
        try:
            result = subprocess.run(
                [ADB, "-s", device_id, "shell"] + cmd,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except (subprocess.SubprocessError, OSError):
            return ""
        return result.stdout

    def _use_device(self, device_id, note):
        self.device_id = device_id
        config_module.save("device_id", device_id)
        print(f"{note}: {device_id}")

    def _run(self, cmd):
        base = [ADB, "-s", self.device_id] if self.device_id else [ADB]
        result = subprocess.run(
            base + cmd, capture_output=True, text=True, timeout=30, cwd=PROJECT_ROOT
        )
        return result.returncode == 0

    def screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        if not (
            self._run(["shell", "screencap", "-p", "/sdcard/tmp.png"])
            and self._run(["pull", "/sdcard/tmp.png", dest])
        ):
            self.stop(
                "Lost contact with the ADB device while capturing the screen. "
                "Check that your emulator is still running, then try again."
            )
        self._run(["shell", "rm", "/sdcard/tmp.png"])
        return dest

    def tap(self, x, y):
        self._run(["shell", "input", "tap", str(x), str(y)])

    def swipe(self, x1, y1, x2, y2, ms=300):
        self._run(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms)])

    def write(self, text):
        escaped = text.replace(" ", "\\ ").replace("&", "\\&")
        self._run(["shell", "input", "text", escaped])

    def enter(self):
        self._run(["shell", "input", "keyevent", "66"])

    def delete(self):
        self._run(["shell", "input", "keyevent", "67"])
