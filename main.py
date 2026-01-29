import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.adb_helper import StopScriptException

def print_menu():
    os.system('cls')
    print("="*50)
    print(" 7DSGC SemiLegit-Bot")
    print("="*50)
    print("1. Daily")
    print("2. Auto Demon Farm")
    print("3. Equipment Farm")
    print("0. Quit")
    print("="*50)

def run_mode(mode_number: int):
    try:
        if mode_number == 1:
            from mode.daily import run_daily
            run_daily()
            
        elif mode_number == 2:
            from mode.auto_demon_farm import run_auto_demon_farm
            run_auto_demon_farm()
            
        elif mode_number == 3:
            from mode.equipement_farm import run_equipement_farm
            run_equipement_farm()
        
        else:
            print("Invalid mode!")
            return False
            
        return True
        
    except ImportError as e:
        print(f" Error importing: {e}")
        print(" Check if the module exists and is correctly configured")
        return False
    except StopScriptException as e:
        # Exception pour arrêter proprement le script sans fermer immédiatement le terminal
        print(f"\n {e.message}")
        print(" Script stopped by user or automation condition")
        return False
    except Exception as e:
        print(f" Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    while True:
        print_menu()
        
        try:
            choice = input("\n Select a mode (0-3): ").strip()
            
            if choice == "0":
                break
            
            mode_number = int(choice)
            
            if 1 <= mode_number <= 3:
                success = run_mode(mode_number)
            else:
                print("Invalid choice! Please enter a number between 0 and 3")
                
        except ValueError:
            print(" Invalid choice! Please enter a number between 0 and 3")
        except KeyboardInterrupt:
            print("\n Interrupted by user")
            break

if __name__ == "__main__":
    main()

