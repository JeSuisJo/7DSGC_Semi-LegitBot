import subprocess
import os

def get_adb_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(current_dir, "platform-tools", "adb.exe")
    return adb_path

def check_devices():
    adb_path = get_adb_path()
    
    if not os.path.exists(adb_path):
        print(f"ADB not found at: {adb_path}")
        return
    
    try:
        # Exécuter la commande adb devices
        result = subprocess.run(
            [adb_path, "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("=" * 50)
            print("All devices connected:")
            print("=" * 50)
            print(result.stdout)
            print("=" * 50)
        else:
            print(f"Error executing adb devices")
            print(f"Return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        print("Timeout executing adb devices")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_devices()
    input("\nPress Enter to close...")
