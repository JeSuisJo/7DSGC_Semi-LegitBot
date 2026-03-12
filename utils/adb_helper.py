import subprocess
import os
import json
from typing import Tuple, Optional, List
from PIL import Image, ImageChops
import math

# ---------------- ADB helper principal ----------------

class ADBHelper:
    def __init__(self, adb_path: Optional[str] = None, device_id: Optional[str] = None):
        if adb_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            adb_path = os.path.join(project_root, "platform-tools", "adb.exe")
        
        self.adb_path = adb_path
        self._check_adb_exists()
        self._image_comparator = None
        self.device_id = device_id
        
        # Calculer la racine du projet une fois
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(current_dir)
    
    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return os.path.join(self.project_root, path)
    
    def _check_adb_exists(self):
        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(f"ADB non trouvé à: {self.adb_path}")
    
    def _execute_command(self, command: List[str], timeout: int = 30) -> Tuple[str, int]:
        if self.device_id:
            if command[0] != "devices":
                full_command = [self.adb_path, "-s", self.device_id] + command
            else:
                full_command = [self.adb_path] + command
        else:
            full_command = [self.adb_path] + command
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            return result.stdout.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "Timeout", -1
        except Exception as e:
            return str(e), -1
    
    # ---------------- Vérification et détection d'appareils ----------------
    
    def get_devices(self) -> List[str]:
        output, code = self._execute_command(["devices"])
        if code != 0:
            return []
        
        devices = []
        lines = output.split('\n')[1:]
        for line in lines:
            if line.strip() and '\tdevice' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        
        return devices
    
    def set_device(self, device_id: Optional[str] = None):
        self.device_id = device_id
    
    def find_mumu_device(self) -> Optional[str]:
        devices = self.get_devices()
        
        for device_id in devices:
            if '127.0.0.1' in device_id or 'localhost' in device_id:
                return device_id
            if 'emulator' in device_id.lower():
                return device_id
        
        if len(devices) == 1:
            return devices[0]
        
        return None
    
    def find_bluestacks_device(self) -> Optional[str]:
        devices = self.get_devices()
        
        for device_id in devices:
            if '127.0.0.1' in device_id or 'localhost' in device_id:
                if ':' in device_id:
                    port = device_id.split(':')[-1]
                    if port.isdigit():
                        port_num = int(port)
                        if port_num == 5555 or (5565 <= port_num <= 5605 and (port_num - 5555) % 10 == 0):
                            return device_id
            # BlueStacks peut aussi apparaître comme emulator-5554
            if 'emulator-5554' in device_id or 'emulator-5556' in device_id:
                return device_id
        
        return None
    
    def find_nox_device(self) -> Optional[str]:
        devices = self.get_devices()
        
        for device_id in devices:
            if '127.0.0.1' in device_id or 'localhost' in device_id:
                if ':' in device_id:
                    port = device_id.split(':')[-1]
                    if port.isdigit():
                        port_num = int(port)
                        # NoxPlayer utilise généralement des ports 62001, 62002, 62003, etc.
                        if 62001 <= port_num <= 62099:
                            return device_id
        
        return None
    
    def identify_emulator_type(self, device_id: str) -> str:
        if not device_id:
            return "Unknown"
        
        if '127.0.0.1' in device_id or 'localhost' in device_id:
            if ':' in device_id:
                port = device_id.split(':')[-1]
                if port.isdigit():
                    port_num = int(port)
                    if 62001 <= port_num <= 62099:
                        return "Nox"
                    if port_num == 5555 or (5565 <= port_num <= 5605 and (port_num - 5555) % 10 == 0):
                        return "BlueStacks"
                    return "MuMu"
        
        if 'emulator' in device_id.lower():
            return "Emulator"
        
        if len(device_id) > 10 and not ':' in device_id and not '127.0.0.1' in device_id:
            return "Physical"
        
        return "Unknown"
    
    # ---------------- Capture d'écran ----------------
    
    def screenshot(self, save_path: str = "screenshot.png") -> bool:
        output, code1 = self._execute_command([
            "shell", "screencap", "-p", "/sdcard/adb_screenshot.png"
        ])
        
        if code1 != 0:
            return False
        
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(current_dir, save_path)
        output, code2 = self._execute_command([
            "pull", "/sdcard/adb_screenshot.png", full_path
        ])
        
        self._execute_command(["shell", "rm", "/sdcard/adb_screenshot.png"])
        
        return code2 == 0
    
    # ---------------- Inputs (touches, swipes, texte) ----------------
    
    def tap(self, x: int, y: int, duration: Optional[int] = None) -> bool:
        if duration:
            return self.swipe(x, y, x, y, duration)
        
        output, code = self._execute_command(["shell", "input", "tap", str(x), str(y)])
        return code == 0
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        output, code = self._execute_command([
            "shell", "input", "swipe", 
            str(x1), str(y1), str(x2), str(y2), str(duration)
        ])
        return code == 0
    
    def input_text(self, text: str) -> bool:
        escaped_text = text.replace(' ', '\\ ').replace('&', '\\&')
        output, code = self._execute_command(["shell", "input", "text", escaped_text])
        return code == 0
    
    def input_keyevent(self, keycode: int) -> bool:
        output, code = self._execute_command(["shell", "input", "keyevent", str(keycode)])
        return code == 0
    
    # ---------------- Détection d'image ----------------
    
    def get_image_comparator(self) -> 'ImageComparator':
        if self._image_comparator is None:
            self._image_comparator = ImageComparator(self)
        return self._image_comparator
    
    def _compare_region_with_image_impl(
        self,
        reference_image_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.95,
        screenshot_path: Optional[str] = None,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> Tuple[bool, float]:
        comparator = self.get_image_comparator()
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return False, 0.0
            screenshot_path = temp_screenshot
        try:
            return comparator.compare_region(
                screenshot_path,
                reference_image_path,
                region,
                threshold
            )
        finally:
            import time
            time.sleep(0.1)
            if screenshot_path == temp_screenshot:
                resolved_temp_path = self._resolve_path(temp_screenshot)
                if os.path.exists(resolved_temp_path):
                    try:
                        os.remove(resolved_temp_path)
                    except (PermissionError, OSError):
                        pass

    def compare_region_with_image(
        self,
        reference_image_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.95,
        screenshot_path: Optional[str] = None,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> bool:
        return self._compare_region_with_image_impl(
            reference_image_path, region, threshold, screenshot_path, temp_screenshot
        )[0]

    def compare_region_with_image_detailed(
        self,
        reference_image_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.95,
        screenshot_path: Optional[str] = None,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> Tuple[bool, float]:
        return self._compare_region_with_image_impl(
            reference_image_path, region, threshold, screenshot_path, temp_screenshot
        )
    
    # ---------------- Détection de couleur ----------------
    
    @staticmethod
    def color_matches(color1: Tuple[int, int, int], color2: Tuple[int, int, int], tolerance: int = 10) -> bool:
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        return (
            abs(r1 - r2) <= tolerance and
            abs(g1 - g2) <= tolerance and
            abs(b1 - b2) <= tolerance
        )
    
    def get_color_at(
        self,
        x: int,
        y: int,
        screenshot_path: Optional[str] = None,
        target_color: Optional[Tuple[int, int, int]] = None,
        tolerance: int = 10,
    ) -> Optional[Tuple[int, int, int]]:
        temp_screenshot = "temp_color_check.png"
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return None
            screenshot_path = temp_screenshot
    
        resolved_screenshot_path = self._resolve_path(screenshot_path)
    
        try:
            img = Image.open(resolved_screenshot_path)
            rgb_img = img.convert("RGB")
            color = rgb_img.getpixel((x, y))
            if target_color is not None:
                if ADBHelper.color_matches(color, target_color, tolerance):
                    return color
                return None
            return color
        except Exception:
            return None
        finally:
            if screenshot_path == temp_screenshot:
                resolved_temp_path = self._resolve_path(temp_screenshot)
                if os.path.exists(resolved_temp_path):
                    try:
                        import time
                        time.sleep(0.1)
                        os.remove(resolved_temp_path)
                    except:
                        pass

    def is_color_at(
        self,
        x: int,
        y: int,
        target_color: Tuple[int, int, int],
        tolerance: int = 10,
        screenshot_path: Optional[str] = None,
    ) -> bool:
        color = self.get_color_at(
            x,
            y,
            screenshot_path=screenshot_path,
            target_color=target_color,
            tolerance=tolerance,
        )
        return color is not None


# ---------------- Singleton ADB ----------------

_adb_instance: Optional[ADBHelper] = None

def get_adb(device_id: Optional[str] = None, force_new: bool = False) -> ADBHelper:
    global _adb_instance
    if _adb_instance is None or force_new:
        _adb_instance = ADBHelper(device_id=device_id)
    elif device_id is not None:
        _adb_instance.set_device(device_id)
    return _adb_instance


def auto_setup_adb(prefer_emulator: Optional[str] = None, verbose: bool = True) -> ADBHelper:
    adb = get_adb()
    
    config_path = get_project_path("config.json")
    device_id_from_config = None
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            device_id_from_config = config.get("device_id")
    except FileNotFoundError:
        if verbose:
            print(f"⚠️  config.json non trouvé à {config_path}")
    except json.JSONDecodeError:
        if verbose:
            print(f"⚠️  Erreur de lecture du JSON dans config.json")
    except Exception as e:
        if verbose:
            print(f"⚠️  Erreur lors de la lecture de config.json: {e}")
    
    if device_id_from_config:
        devices = adb.get_devices()
        if device_id_from_config in devices:
            adb.set_device(device_id_from_config)
            emulator_type = adb.identify_emulator_type(device_id_from_config)
            if emulator_type == "Unknown":
                emulator_type = "Émulateur"
            
            if verbose:
                print(f"✅ Appareil configuré depuis config.json: {device_id_from_config}")
                print(f"📱 Type: {emulator_type}\n")
            return adb
        else:
            if verbose:
                print(f"⚠️  L'appareil '{device_id_from_config}' du config.json n'est pas connecté!")
                print(f"   Appareils disponibles: {devices}")
    
    devices = adb.get_devices()
    if not devices:
        if verbose:
            print("❌ Aucun appareil connecté!")
            print("Assurez-vous que votre émulateur est démarré et que le débogage USB est activé.")
        return adb
    
    selected_device = None
    emulator_type = None
    
    if prefer_emulator:
        prefer_emulator = prefer_emulator.lower()
        if prefer_emulator == "mumu":
            selected_device = adb.find_mumu_device()
            emulator_type = "MuMuPlayer"
        elif prefer_emulator == "bluestacks":
            selected_device = adb.find_bluestacks_device()
            emulator_type = "BlueStacks"
        elif prefer_emulator == "nox":
            selected_device = adb.find_nox_device()
            emulator_type = "NoxPlayer"
    else:
        selected_device = adb.find_mumu_device()
        if selected_device:
            emulator_type = "MuMuPlayer"
        else:
            selected_device = adb.find_bluestacks_device()
            if selected_device:
                emulator_type = "BlueStacks"
            else:
                selected_device = adb.find_nox_device()
                if selected_device:
                    emulator_type = "NoxPlayer"
    
    if not selected_device:
        selected_device = devices[0]
        emulator_type = adb.identify_emulator_type(selected_device)
        if emulator_type == "Unknown":
            emulator_type = "Émulateur"
    
    adb.set_device(selected_device)
    
    if verbose:
        print(f"✅ {emulator_type} détecté: {selected_device}")
        print(f"📱 Appareil configuré: {selected_device}\n")
    
    return adb


# ---------------- Exception personnalisée pour arrêter le bot ----------------

class StopScriptException(Exception):
    def __init__(self, message: str = "Script stopped"):
        self.message = message
        super().__init__(self.message)


# ---------------- Utilitaire chemin projet ----------------

def get_project_path(relative_path: str) -> str:
    if os.path.isabs(relative_path):
        return relative_path
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, relative_path)


# ---------------- Comparaison d'images ----------------

class ImageComparator:
    def __init__(self, adb_helper=None):
        self.adb = adb_helper
    
    def compare_region(
        self, 
        screenshot_path: str, 
        reference_image_path: str, 
        region: Tuple[int, int, int, int],
        threshold: float = 0.95
    ) -> Tuple[bool, float]:
        if self.adb:
            resolved_screenshot_path = self.adb._resolve_path(screenshot_path)
            resolved_reference_path = self.adb._resolve_path(reference_image_path)
        else:
            resolved_screenshot_path = screenshot_path
            resolved_reference_path = reference_image_path
        
        if not os.path.exists(resolved_screenshot_path):
            print(f"❌ Screenshot non trouvé: {screenshot_path}")
            print(f"   Chemin résolu: {resolved_screenshot_path}")
            return False, 0.0
        
        if not os.path.exists(resolved_reference_path):
            print(f"❌ Fichier de référence non trouvé: {reference_image_path}")
            print(f"   Chemin résolu: {resolved_reference_path}")
            return False, 0.0
        
        screenshot = None
        reference = None
        try:
            screenshot = Image.open(resolved_screenshot_path)
            reference = Image.open(resolved_reference_path)
            
            if len(region) == 4:
                x1, y1, val3, val4 = region
                if val3 > x1 and val4 > y1:
                    screenshot_region = screenshot.crop((x1, y1, val3, val4))
                else:
                    screenshot_region = screenshot.crop((x1, y1, x1 + val3, y1 + val4))
            else:
                screenshot_region = screenshot.crop(region)
            
            if screenshot_region.size != reference.size:
                screenshot_region = screenshot_region.resize(reference.size, Image.Resampling.LANCZOS)
            
            similarity = self._calculate_similarity(screenshot_region, reference)
            
            return similarity >= threshold, similarity
        finally:
            if screenshot:
                screenshot.close()
            if reference:
                reference.close()
    
    def compare_region_from_screenshot(
        self,
        reference_image_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.95,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> Tuple[bool, float]:
        if not self.adb:
            raise ValueError("ADBHelper requis pour cette méthode")
        
        if not self.adb.screenshot(temp_screenshot):
            return False, 0.0
        
        try:
            return self.compare_region(
                temp_screenshot, 
                reference_image_path, 
                region, 
                threshold
            )
        finally:
            if os.path.exists(temp_screenshot):
                os.remove(temp_screenshot)
    
    def _calculate_similarity(self, img1: Image.Image, img2: Image.Image) -> float:
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        if img2.mode != 'RGB':
            img2 = img2.convert('RGB')
        
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
        
        diff = ImageChops.difference(img1, img2)
        
        hist = diff.histogram()
        total_pixels = img1.size[0] * img1.size[1] * 3
        
        sum_squared_diff = 0.0
        for channel in range(3):
            for pixel_value in range(256):
                count = hist[channel * 256 + pixel_value]
                sum_squared_diff += (pixel_value ** 2) * count
        
        if total_pixels > 0:
            rms = math.sqrt(sum_squared_diff / total_pixels)
        else:
            rms = 255.0
        
        similarity = 1.0 - (rms / 255.0)
        
        return max(0.0, min(1.0, similarity))  # Clamper entre 0 et 1


# ---------------- Constantes de touches Android ----------------

class KeyCode:
    ENTER = 66
    DELETE = 67
