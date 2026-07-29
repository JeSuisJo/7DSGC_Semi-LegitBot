"""Active driver instance."""

from .base import Driver, StopScript


def create_driver():
    """Build a driver for the configured emulator.

    Nothing touches adb here: the device is resolved by ``ensure_ready()``.
    """
    from .adb import AdbDriver

    return AdbDriver()


driver = create_driver()

__all__ = ["Driver", "StopScript", "create_driver", "driver"]
