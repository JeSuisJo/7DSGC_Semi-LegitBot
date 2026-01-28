from utils.adb_helper import auto_setup_adb
import time
import os
from utils.DailyPvp import Daily_pvp
from utils.recyclingEquipement import recycle_equipement

def run_test():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print(" Test mode")
    print("=" * 50)

    recycle_equipement()
    
    print("Test mode completed")

