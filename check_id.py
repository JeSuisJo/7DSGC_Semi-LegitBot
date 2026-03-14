import subprocess
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ADB  = os.path.join(ROOT, "platform-tools", "adb.exe")

if not os.path.exists(ADB):
    print(f"ADB not found: {ADB}")
    input("\nPress Enter to close...")
    exit()

result = subprocess.run([ADB, "devices"], capture_output=True, text=True, timeout=10)
lines = [l for l in result.stdout.strip().split("\n")[1:] if "\tdevice" in l]
devices = [l.split("\t")[0] for l in lines]

print("=" * 50)
if devices:
    print(f"{len(devices)} device(s) connected:")
    for d in devices:
        print(f"  → {d}")
else:
    print("No device connected.")
print("=" * 50)

input("\nPress Enter to close...")
