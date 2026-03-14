import time
import os
from utils.equipementFarm import equipement_farm

def run_equipement_farm():
    os.system('cls')
    print("=" * 50)
    print("Equipment farm mode")
    print("=" * 50)
    
    equipement_farm()

    
    print("Equipment farm mode completed")
