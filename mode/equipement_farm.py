from utils.adb_helper import auto_setup_adb
import time
import os
from utils.equipementFarm import equipement_farm

def run_equipement_farm():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print("Equipment farm mode")
    print("=" * 50)
    
    equipement_farm()

    
    print("Equipment farm mode completed")
