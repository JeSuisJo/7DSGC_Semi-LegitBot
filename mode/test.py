from utils.adb_helper import auto_setup_adb
import time
import os
from utils.DailyPvp import Daily_pvp
from utils.test_thing import test

def run_test():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print(" Test mode")
    print("=" * 50)

    Daily_pvp()
    
    print("Test mode completed")

