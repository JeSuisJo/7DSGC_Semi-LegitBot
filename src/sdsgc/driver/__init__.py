from .base import Driver, StopScript


def create_driver():
    from .adb import AdbDriver

    return AdbDriver()


driver = create_driver()

__all__ = ["Driver", "StopScript", "create_driver", "driver"]
