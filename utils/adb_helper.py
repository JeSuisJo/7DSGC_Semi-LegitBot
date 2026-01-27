import subprocess
import os
import json
from typing import Tuple, Optional, List
from PIL import Image, ImageChops
import math

# ==================== CLASSE ADBHelper ====================

class ADBHelper:
    """Helper class pour exécuter des commandes ADB"""
    
    def __init__(self, adb_path: Optional[str] = None, device_id: Optional[str] = None):
        """
        Initialise l'helper ADB
        
        Args:
            adb_path: Chemin vers adb.exe. Si None, utilise le chemin relatif depuis utils/
            device_id: ID de l'appareil/émulateur à utiliser. Si None, utilise le premier disponible
        """
        if adb_path is None:
            # Chemin relatif depuis utils/ vers platform-tools/
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
        """
        Résout un chemin relatif vers la racine du projet
        
        Args:
            path: Chemin relatif ou absolu
        
        Returns:
            Chemin absolu résolu
        """
        # Si c'est déjà un chemin absolu, le retourner tel quel
        if os.path.isabs(path):
            return path
        
        # Sinon, le résoudre depuis la racine du projet
        return os.path.join(self.project_root, path)
    
    def _check_adb_exists(self):
        """Vérifie que adb.exe existe"""
        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(f"ADB non trouvé à: {self.adb_path}")
    
    def _execute_command(self, command: List[str], timeout: int = 30) -> Tuple[str, int]:
        """
        Exécute une commande ADB
        
        Args:
            command: Liste des arguments de la commande
            timeout: Timeout en secondes
            
        Returns:
            Tuple (stdout, return_code)
        """
        # Ajouter -s device_id si un appareil spécifique est sélectionné
        if self.device_id:
            # La commande "devices" ne prend pas -s, on l'ignore pour cette commande
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
    
    # ==================== Méthodes de vérification ====================
    
    def get_devices(self) -> List[str]:
        """
        Liste tous les appareils connectés
        
        Returns:
            Liste des IDs d'appareils connectés
        """
        output, code = self._execute_command(["devices"])
        if code != 0:
            return []
        
        devices = []
        lines = output.split('\n')[1:]  # Ignore la première ligne "List of devices attached"
        for line in lines:
            if line.strip() and '\tdevice' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        
        return devices
    
    def print_devices(self):
        """Affiche tous les appareils connectés avec leur statut"""
        output, code = self._execute_command(["devices"])
        if code == 0:
            print(output)
        else:
            print("Erreur lors de la récupération des appareils")
    
    def set_device(self, device_id: Optional[str] = None):
        """
        Change l'appareil utilisé par ADBHelper
        
        Args:
            device_id: ID de l'appareil à utiliser. Si None, utilise le premier disponible
        """
        self.device_id = device_id
    
    def get_current_device(self) -> Optional[str]:
        """
        Retourne l'ID de l'appareil actuellement utilisé
        
        Returns:
            ID de l'appareil ou None si aucun appareil spécifique n'est sélectionné
        """
        return self.device_id
    
    def find_mumu_device(self) -> Optional[str]:
        """
        Trouve automatiquement l'ID d'un appareil MuMuPlayer
        
        MuMuPlayer utilise généralement:
        - Port 7555 (127.0.0.1:7555) - MuMu par défaut
        - Port 5555 (127.0.0.1:5555) - Autre configuration MuMu
        - Ou d'autres ports si plusieurs instances sont ouvertes.
        
        Returns:
            ID du premier appareil MuMu trouvé, ou None si aucun
        """
        devices = self.get_devices()
        
        # Chercher des ports MuMu typiques (7555, 5555, 7556, etc. ou formats emulator)
        for device_id in devices:
            # MuMu utilise souvent 127.0.0.1:XXXX (localhost)
            if '127.0.0.1' in device_id or 'localhost' in device_id:
                # Tous les appareils localhost:XXXX sont considérés comme MuMu/émulateurs
                # Car MuMu peut utiliser différents ports (5555, 7555, etc.)
                return device_id
            # Parfois MuMu apparaît aussi comme emulator-XXXX
            if 'emulator' in device_id.lower():
                return device_id
        
        # Si un seul appareil est connecté et qu'on n'a pas trouvé spécifiquement MuMu, le retourner
        if len(devices) == 1:
            return devices[0]
        
        return None
    
    def find_bluestacks_device(self) -> Optional[str]:
        """
        Trouve automatiquement l'ID d'un appareil BlueStacks
        
        BlueStacks utilise généralement:
        - Port 5555 (127.0.0.1:5555) - BlueStacks par défaut
        - Ports 5565, 5575, 5585, 5595, etc. pour multiples instances
        - Format parfois: emulator-5554 ou localhost:5555
        
        Returns:
            ID du premier appareil BlueStacks trouvé, ou None si aucun
        """
        devices = self.get_devices()
        
        for device_id in devices:
            # BlueStacks utilise souvent 127.0.0.1:5555 (ou ports similaires)
            if '127.0.0.1' in device_id or 'localhost' in device_id:
                if ':' in device_id:
                    port = device_id.split(':')[-1]
                    if port.isdigit():
                        port_num = int(port)
                        # BlueStacks utilise généralement 5555, 5565, 5575, 5585, 5595, etc.
                        # (multiples de 10 à partir de 5555)
                        if port_num == 5555 or (5565 <= port_num <= 5605 and (port_num - 5555) % 10 == 0):
                            return device_id
            # BlueStacks peut aussi apparaître comme emulator-5554
            if 'emulator-5554' in device_id or 'emulator-5556' in device_id:
                return device_id
        
        return None
    
    def find_nox_device(self) -> Optional[str]:
        """
        Trouve automatiquement l'ID d'un appareil NoxPlayer
        
        NoxPlayer utilise généralement:
        - Port 62001 (127.0.0.1:62001) - Première instance Nox
        - Port 62002 (127.0.0.1:62002) - Deuxième instance Nox
        - Port 62003, 62004, etc. pour autres instances
        
        Returns:
            ID du premier appareil NoxPlayer trouvé, ou None si aucun
        """
        devices = self.get_devices()
        
        for device_id in devices:
            # NoxPlayer utilise généralement 127.0.0.1:62001, 62002, 62003, etc.
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
        """
        Identifie le type d'émulateur basé sur l'ID de l'appareil
        
        Args:
            device_id: ID de l'appareil à identifier
        
        Returns:
            Type d'émulateur ("MuMu", "BlueStacks", "Nox", "Emulator", "Physical", "Unknown")
        """
        if not device_id:
            return "Unknown"
        
        # NoxPlayer - ports 62001-62099
        if '127.0.0.1' in device_id or 'localhost' in device_id:
            if ':' in device_id:
                port = device_id.split(':')[-1]
                if port.isdigit():
                    port_num = int(port)
                    if 62001 <= port_num <= 62099:
                        return "Nox"
                    # BlueStacks - ports 5555, 5565, 5575, etc.
                    if port_num == 5555 or (5565 <= port_num <= 5605 and (port_num - 5555) % 10 == 0):
                        return "BlueStacks"
                    # MuMu - autres localhost (généralement 7555, 5555, etc.)
                    return "MuMu"
        
        # Formats emulator-XXXX (peut être n'importe quel émulateur)
        if 'emulator' in device_id.lower():
            return "Emulator"
        
        # Si c'est un ID long avec lettres/chiffres, probablement un appareil physique
        if len(device_id) > 10 and not ':' in device_id and not '127.0.0.1' in device_id:
            return "Physical"
        
        return "Unknown"
    
    def list_devices_with_info(self) -> List[Tuple[str, str]]:
        """
        Liste tous les appareils connectés avec leur type d'émulateur
        
        Returns:
            Liste de tuples (device_id, emulator_type)
        """
        devices = self.get_devices()
        result = []
        
        for device_id in devices:
            emulator_type = self.identify_emulator_type(device_id)
            result.append((device_id, emulator_type))
        
        return result
    
    def print_devices_with_info(self):
        """
        Affiche tous les appareils connectés avec leur type d'émulateur identifié
        """
        devices_info = self.list_devices_with_info()
        
        if not devices_info:
            print("❌ Aucun appareil connecté!")
            return
        
        print("\n" + "="*60)
        print("📱 Appareils connectés:")
        print("="*60)
        
        for i, (device_id, emulator_type) in enumerate(devices_info, 1):
            emoji = {
                "MuMu": "🟢",
                "BlueStacks": "🔵",
                "Nox": "🟣",
                "Emulator": "⚪",
                "Physical": "📱",
                "Unknown": "❓"
            }.get(emulator_type, "❓")
            
            print(f"{i}. {emoji} {device_id:<25} [{emulator_type}]")
        
        print("="*60 + "\n")
        
        # Suggestions
        mumu = self.find_mumu_device()
        bluestacks = self.find_bluestacks_device()
        nox = self.find_nox_device()
        
        suggestions = []
        if mumu:
            suggestions.append(f"MuMuPlayer: {mumu}")
        if bluestacks:
            suggestions.append(f"BlueStacks: {bluestacks}")
        if nox:
            suggestions.append(f"NoxPlayer: {nox}")
        
        if suggestions:
            print("💡 Émulateurs détectés:")
            for suggestion in suggestions:
                print(f"   • {suggestion}")
            print()
    
    def auto_select_device(self, prefer_mumu: bool = True) -> Optional[str]:
        """
        Sélectionne automatiquement un appareil
        
        Args:
            prefer_mumu: Si True, préfère MuMuPlayer si disponible
        
        Returns:
            ID de l'appareil sélectionné, ou None si aucun disponible
        """
        devices = self.get_devices()
        
        if not devices:
            return None
        
        if prefer_mumu:
            mumu_device = self.find_mumu_device()
            if mumu_device:
                self.set_device(mumu_device)
                return mumu_device
        
        # Sinon, utiliser le premier disponible
        self.set_device(devices[0])
        return devices[0]
    
    def is_device_connected(self) -> bool:
        """Vérifie si au moins un appareil est connecté"""
        return len(self.get_devices()) > 0
    
    def wait_for_device(self, timeout: int = 30) -> bool:
        """
        Attend qu'un appareil soit connecté
        
        Args:
            timeout: Timeout en secondes
            
        Returns:
            True si un appareil est connecté, False sinon
        """
        output, code = self._execute_command(["wait-for-device"], timeout=timeout)
        return code == 0
    
    # ==================== Méthodes de capture d'écran ====================
    
    def screenshot(self, save_path: str = "screenshot.png") -> bool:
        """
        Prend une capture d'écran
        
        Args:
            save_path: Chemin où sauvegarder l'image (relatif au projet)
            
        Returns:
            True si succès, False sinon
        """
        # Capture sur le device
        output, code1 = self._execute_command([
            "shell", "screencap", "-p", "/sdcard/adb_screenshot.png"
        ])
        
        if code1 != 0:
            return False
        
        # Récupère le fichier
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(current_dir, save_path)
        output, code2 = self._execute_command([
            "pull", "/sdcard/adb_screenshot.png", full_path
        ])
        
        # Nettoie le fichier sur le device (optionnel)
        self._execute_command(["shell", "rm", "/sdcard/adb_screenshot.png"])
        
        return code2 == 0
    
    def get_screenshot_bytes(self) -> Optional[bytes]:
        """
        Récupère une capture d'écran en bytes (sans fichier temporaire)
        
        Returns:
            Bytes de l'image ou None si erreur
        """
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "screencap", "-p"],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                # ADB ajoute parfois \r\n, on les enlève
                return result.stdout.replace(b'\r\n', b'\n')
            return None
        except Exception:
            return None
    
    def capture_region(self, region: Tuple[int, int, int, int], save_path: str = "captured_region.png", screenshot_path: Optional[str] = None) -> bool:
        """
        Capture une région précise du screenshot et la sauvegarde pour débogage
        
        Utile pour voir exactement ce que le code voit dans une région spécifique
        
        Args:
            region: Tuple (x, y, width, height) ou (x1, y1, x2, y2) de la région à capturer
            save_path: Chemin où sauvegarder la région capturée
            screenshot_path: Chemin du screenshot (optionnel, prend un screenshot si None)
        
        Returns:
            True si succès, False sinon
        """
        temp_screenshot = "temp_region_capture.png"
        
        # Prendre un screenshot si nécessaire
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return False
            screenshot_path = temp_screenshot
        
        try:
            # Charger le screenshot
            screenshot = Image.open(screenshot_path)
            
            # Extraire la région (même logique que compare_region)
            if len(region) == 4:
                x1, y1, val3, val4 = region
                if val3 > x1 and val4 > y1:
                    # Format (x1, y1, x2, y2)
                    region_img = screenshot.crop((x1, y1, val3, val4))
                else:
                    # Format (x, y, width, height)
                    region_img = screenshot.crop((x1, y1, x1 + val3, y1 + val4))
            else:
                region_img = screenshot.crop(region)
            
            # Sauvegarder la région
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(current_dir, save_path)
            region_img.save(full_path)
            
            print(f"📸 Région capturée sauvegardée: {save_path}")
            print(f"   Taille: {region_img.size[0]}x{region_img.size[1]} pixels")
            
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la capture de la région: {e}")
            return False
        finally:
            # Nettoyer le screenshot temporaire si on l'a créé
            if screenshot_path == temp_screenshot and os.path.exists(temp_screenshot):
                try:
                    import time
                    time.sleep(0.1)
                    os.remove(temp_screenshot)
                except:
                    pass
    
    # ==================== Méthodes d'input (touches, swipes, etc.) ====================
    
    def tap(self, x: int, y: int, duration: Optional[int] = None) -> bool:
        """
        Simule un tap à la position (x, y)
        
        Args:
            x: Coordonnée X
            y: Coordonnée Y
            duration: Durée du tap en ms (optionnel, pour long press)
            
        Returns:
            True si succès, False sinon
        """
        if duration:
            # Long press si duration spécifié
            return self.swipe(x, y, x, y, duration)
        
        output, code = self._execute_command(["shell", "input", "tap", str(x), str(y)])
        return code == 0
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """
        Simule un swipe de (x1, y1) vers (x2, y2)
        
        Args:
            x1: Coordonnée X de départ
            y1: Coordonnée Y de départ
            x2: Coordonnée X d'arrivée
            y2: Coordonnée Y d'arrivée
            duration: Durée du swipe en ms
            
        Returns:
            True si succès, False sinon
        """
        output, code = self._execute_command([
            "shell", "input", "swipe", 
            str(x1), str(y1), str(x2), str(y2), str(duration)
        ])
        return code == 0
    
    def input_text(self, text: str) -> bool:
        """
        Envoie du texte (attention: caractères spéciaux limités)
        
        Args:
            text: Texte à envoyer
            
        Returns:
            True si succès, False sinon
        """
        # Échappe les caractères spéciaux pour le shell
        escaped_text = text.replace(' ', '\\ ').replace('&', '\\&')
        output, code = self._execute_command(["shell", "input", "text", escaped_text])
        return code == 0
    
    def input_keyevent(self, keycode: int) -> bool:
        """
        Simule une touche système
        
        Args:
            keycode: Code de la touche (ex: 4 = BACK, 3 = HOME, 187 = MENU)
            
        Returns:
            True si succès, False sinon
        """
        output, code = self._execute_command(["shell", "input", "keyevent", str(keycode)])
        return code == 0
    
    def press_back(self) -> bool:
        """Presse la touche retour"""
        return self.input_keyevent(4)
    
    def press_home(self) -> bool:
        """Presse la touche accueil"""
        return self.input_keyevent(3)
    
    def press_menu(self) -> bool:
        """Presse la touche menu"""
        return self.input_keyevent(187)
    
    # ==================== Méthodes shell ====================
    
    def shell(self, command: str) -> Tuple[str, int]:
        """
        Exécute une commande shell sur le device
        
        Args:
            command: Commande shell à exécuter
            
        Returns:
            Tuple (stdout, return_code)
        """
        return self._execute_command(["shell", command])
    
    # ==================== Méthodes d'applications ====================
    
    def get_current_package(self) -> Optional[str]:
        """
        Récupère le nom du package de l'application en cours
        
        Returns:
            Nom du package ou None
        """
        output, code = self.shell("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")
        if code == 0 and output:
            # Parse le résultat pour extraire le package name
            parts = output.split('/')
            if len(parts) > 0:
                package_part = parts[0]
                if package_part.startswith('mCurrentFocus') or package_part.startswith('mFocusedApp'):
                    # Format: mCurrentFocus=Window{... package/activity}
                    for part in parts:
                        if '.' in part and '}' not in part:
                            return part.strip()
        return None
    
    def launch_app(self, package_name: str, activity_name: str) -> bool:
        """
        Lance une application
        
        Args:
            package_name: Nom du package
            activity_name: Nom de l'activité (ex: .MainActivity)
            
        Returns:
            True si succès, False sinon
        """
        output, code = self.shell(f"am start -n {package_name}/{activity_name}")
        return code == 0
    
    def stop_app(self, package_name: str) -> bool:
        """
        Arrête une application
        
        Args:
            package_name: Nom du package
            
        Returns:
            True si succès, False sinon
        """
        output, code = self.shell(f"am force-stop {package_name}")
        return code == 0
    
    # ==================== Méthodes de fichiers ====================
    
    def push_file(self, local_path: str, remote_path: str) -> bool:
        """
        Envoie un fichier vers le device
        
        Args:
            local_path: Chemin local du fichier
            remote_path: Chemin sur le device
            
        Returns:
            True si succès, False sinon
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_local_path = os.path.join(current_dir, local_path)
        output, code = self._execute_command(["push", full_local_path, remote_path])
        return code == 0
    
    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """
        Récupère un fichier depuis le device
        
        Args:
            remote_path: Chemin sur le device
            local_path: Chemin local où sauvegarder
            
        Returns:
            True si succès, False sinon
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_local_path = os.path.join(current_dir, local_path)
        output, code = self._execute_command(["pull", remote_path, full_local_path])
        return code == 0
    
    # ==================== Méthodes de détection d'image ====================
    
    def get_image_comparator(self) -> 'ImageComparator':
        """Retourne une instance ImageComparator liée à cet ADBHelper"""
        if self._image_comparator is None:
            self._image_comparator = ImageComparator(self)
        return self._image_comparator
    
    def find_image(
        self,
        template_path: str,
        screenshot_path: Optional[str] = None,
        threshold: float = 0.8,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> Optional[Tuple[int, int]]:
        """
        Cherche un template (petite image) dans un screenshot
        Prend un screenshot si screenshot_path n'est pas fourni
        
        Args:
            template_path: Chemin de l'image template à chercher
            screenshot_path: Chemin du screenshot (optionnel, prend un screenshot si None)
            threshold: Seuil de correspondance minimum
        
        Returns:
            Tuple (x, y) du centre trouvé, ou None si pas trouvé
        """
        comparator = self.get_image_comparator()
        
        # Prendre un screenshot si nécessaire
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return None
            screenshot_path = temp_screenshot
        
        try:
            return comparator.find_template_in_screenshot(
                screenshot_path,
                template_path,
                threshold
            )
        finally:
            # Nettoyer le fichier temporaire si on l'a créé
            if screenshot_path == temp_screenshot and os.path.exists(temp_screenshot):
                os.remove(temp_screenshot)
    
    def compare_region_with_image(
        self,
        reference_image_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.95,
        screenshot_path: Optional[str] = None,
        temp_screenshot: str = "temp_screenshot.png"
    ) -> Tuple[bool, float]:
        """
        Compare une région précise du screenshot avec une image de référence
        
        Args:
            reference_image_path: Chemin de l'image de référence
            region: Tuple (x, y, width, height) de la région
            threshold: Seuil de similarité
            screenshot_path: Chemin du screenshot (optionnel)
            temp_screenshot: Nom du screenshot temporaire
        
        Returns:
            Tuple (is_match: bool, similarity_score: float)
        """
        comparator = self.get_image_comparator()
        
        # Prendre un screenshot si nécessaire
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
            # Nettoyer le fichier temporaire si on l'a créé
            # Attendre un peu pour s'assurer que les fichiers sont fermés
            import time
            time.sleep(0.1)  # Petit délai pour libérer le fichier
            if screenshot_path == temp_screenshot:
                # Résoudre le chemin pour le nettoyage
                resolved_temp_path = self._resolve_path(temp_screenshot)
                if os.path.exists(resolved_temp_path):
                    try:
                        os.remove(resolved_temp_path)
                    except (PermissionError, OSError):
                        # Si le fichier est encore verrouillé, on ignore l'erreur
                        # Il sera nettoyé au prochain appel ou à la fin du script
                        pass
    
    # ==================== Méthodes de détection de couleur ====================
    
    @staticmethod
    def color_matches(color1: Tuple[int, int, int], color2: Tuple[int, int, int], tolerance: int = 10) -> bool:
        """
        Vérifie si deux couleurs correspondent avec une tolérance
        
        Args:
            color1: Première couleur RGB (R, G, B)
            color2: Deuxième couleur RGB (R, G, B)
            tolerance: Tolérance ±tolerance pour chaque canal RGB
        
        Returns:
            True si les couleurs correspondent (dans la tolérance), False sinon
        
        Exemple:
            color1 = (255, 0, 0)  # Rouge
            color2 = (250, 5, 8)  # Rouge légèrement différent
            ADBHelper.color_matches(color1, color2, tolerance=10)  # True
        """
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
        """
        Récupère la couleur RGB à une position précise.

        - Si `target_color` est fourni : retourne la couleur seulement si elle
          correspond (dans la tolérance), sinon `None`.
        - Si `target_color` est `None` : retourne toujours la couleur lue.
        """
        temp_screenshot = "temp_color_check.png"

        # Prendre un screenshot si nécessaire
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return None
            screenshot_path = temp_screenshot

        # Résoudre le chemin du screenshot vers la racine du projet
        resolved_screenshot_path = self._resolve_path(screenshot_path)

        try:
            img = Image.open(resolved_screenshot_path)
            rgb_img = img.convert("RGB")
            color = rgb_img.getpixel((x, y))

            # Si une couleur cible est spécifiée, vérifier la correspondance
            if target_color is not None:
                if ADBHelper.color_matches(color, target_color, tolerance):
                    return color
                return None  # Ne correspond pas à la cible

            return color
        except Exception as e:
            # Debug: afficher l'erreur si problème
            print(f"Error in get_color_at: {e}")
            return None
        finally:
            # Nettoyer le fichier temporaire avec le chemin résolu
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
        """
        Vérifie simplement si une position (x, y) correspond à une couleur cible.

        C'est un raccourci lisible pour le cas binaire
        "est-ce que ce pixel est de cette couleur ou non ?".
        """
        color = self.get_color_at(
            x,
            y,
            screenshot_path=screenshot_path,
            target_color=target_color,
            tolerance=tolerance,
        )
        return color is not None
    
    def find_color_in_region(
        self,
        target_color: Tuple[int, int, int],
        region: Tuple[int, int, int, int],
        tolerance: int = 10,
        screenshot_path: Optional[str] = None
    ) -> List[Tuple[int, int]]:
        """
        Trouve toutes les occurrences d'une couleur dans une région
        
        Args:
            target_color: Couleur RGB cible (R, G, B)
            region: Tuple (x, y, width, height) de la région à chercher
            tolerance: Tolérance de couleur (±tolerance pour chaque canal RGB)
            screenshot_path: Chemin du screenshot (optionnel)
            
        Returns:
            Liste de positions (x, y) où la couleur a été trouvée
        """
        temp_screenshot = "temp_color_search.png"
        matches = []
        
        # Prendre un screenshot si nécessaire
        if screenshot_path is None:
            if not self.screenshot(temp_screenshot):
                return matches
            screenshot_path = temp_screenshot
        
        try:
            img = Image.open(screenshot_path)
            rgb_img = img.convert('RGB')
            
            x, y, w, h = region
            target_r, target_g, target_b = target_color
            
            # Parcourir la région
            for py in range(y, min(y + h, rgb_img.height)):
                for px in range(x, min(x + w, rgb_img.width)):
                    r, g, b = rgb_img.getpixel((px, py))
                    
                    # Vérifier si la couleur est dans la tolérance (utilise la méthode globale)
                    if self.color_matches((r, g, b), target_color, tolerance):
                        matches.append((px, py))
            
            return matches
        except Exception:
            return matches
        finally:
            if screenshot_path == temp_screenshot and os.path.exists(temp_screenshot):
                os.remove(temp_screenshot)
    
    def wait_for_color(
        self,
        target_color: Tuple[int, int, int],
        position: Tuple[int, int],
        tolerance: int = 10,
        timeout: float = 5.0,
        check_interval: float = 0.5
    ) -> bool:
        """
        Attend qu'une couleur spécifique apparaisse à une position
        
        Args:
            target_color: Couleur RGB cible (R, G, B)
            position: Position (x, y) à vérifier
            tolerance: Tolérance de couleur
            timeout: Timeout en secondes
            check_interval: Intervalle entre les vérifications en secondes
            
        Returns:
            True si la couleur est trouvée, False si timeout
        """
        import time
        start_time = time.time()
        target_r, target_g, target_b = target_color
        x, y = position
        
        while time.time() - start_time < timeout:
            color = self.get_color_at(x, y, target_color=target_color, tolerance=tolerance)
            if color:  # Si color est retourné, c'est qu'il correspond (grâce à target_color)
                return True
            
            time.sleep(check_interval)
        
        return False


# ==================== SINGLETON ====================

_adb_instance: Optional[ADBHelper] = None

def get_adb(device_id: Optional[str] = None, force_new: bool = False) -> ADBHelper:
    """
    Retourne l'instance globale ADBHelper (singleton)
    
    Args:
        device_id: ID de l'appareil/émulateur à utiliser. Si None, utilise le premier disponible
        force_new: Si True, crée une nouvelle instance même si une existe déjà
    
    Returns:
        Instance ADBHelper
    """
    global _adb_instance
    if _adb_instance is None or force_new:
        _adb_instance = ADBHelper(device_id=device_id)
    elif device_id is not None:
        # Si on change le device_id, mettre à jour l'instance existante
        _adb_instance.set_device(device_id)
    return _adb_instance


def auto_setup_adb(prefer_emulator: Optional[str] = None, verbose: bool = True) -> ADBHelper:
    """
    Configure automatiquement ADB en utilisant le device_id depuis config.json
    
    Args:
        prefer_emulator: Ignoré (conservé pour compatibilité)
        verbose: Si True, affiche des messages informatifs
    
    Returns:
        Instance ADBHelper configurée avec l'appareil depuis config.json
    
    Exemple:
        # Dans n'importe quel fichier Python, une seule ligne!
        adb = auto_setup_adb()
        adb.tap(500, 1000)
    """
    adb = get_adb()
    
    # Charger le device_id depuis config.json
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
    
    # Si device_id est trouvé dans config.json, l'utiliser directement
    if device_id_from_config:
        # Vérifier que l'appareil est connecté
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
    
    # Si pas de device_id dans config.json ou appareil non connecté, utiliser la détection automatique
    devices = adb.get_devices()
    if not devices:
        if verbose:
            print("❌ Aucun appareil connecté!")
            print("Assurez-vous que votre émulateur est démarré et que le débogage USB est activé.")
        return adb
    
    selected_device = None
    emulator_type = None
    
    # Détection selon la préférence ou ordre par défaut
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
        # Ordre par défaut: MuMu -> BlueStacks -> Nox -> premier disponible
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
    
    # Si aucun émulateur spécifique trouvé, utiliser le premier disponible
    if not selected_device:
        selected_device = devices[0]
        emulator_type = adb.identify_emulator_type(selected_device)
        if emulator_type == "Unknown":
            emulator_type = "Émulateur"
    
    # Configurer l'appareil sélectionné
    adb.set_device(selected_device)
    
    if verbose:
        print(f"✅ {emulator_type} détecté: {selected_device}")
        print(f"📱 Appareil configuré: {selected_device}\n")
    
    return adb


# ==================== EXCEPTION PERSONNALISÉE ====================

class StopScriptException(Exception):
    """
    Exception personnalisée pour arrêter proprement le script
    Au lieu d'utiliser sys.exit(), utilisez cette exception qui sera
    capturée dans main.py pour un arrêt propre sans fermer immédiatement le terminal
    """
    def __init__(self, message: str = "Script stopped"):
        self.message = message
        super().__init__(self.message)


# ==================== FONCTION UTILITAIRE ====================

def get_project_path(relative_path: str) -> str:
    """
    Résout un chemin relatif vers la racine du projet
    Peut être utilisée depuis n'importe quel fichier Python du projet
    
    Args:
        relative_path: Chemin relatif depuis la racine du projet (ex: "img/prep.png")
    
    Returns:
        Chemin absolu résolu depuis la racine du projet
    
    Exemple:
        get_project_path("img/prep.png")  # Retourne: "C:/Users/.../REBUILD/img/prep.png"
    """
    # Si c'est déjà un chemin absolu, le retourner tel quel
    if os.path.isabs(relative_path):
        return relative_path
    
    # Obtenir le répertoire du fichier actuel (utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Remonter d'un niveau pour avoir la racine du projet
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, relative_path)


# ==================== CLASSE ImageComparator ====================

class ImageComparator:
    """Classe pour comparer des images, utilisable avec ADBHelper"""
    
    def __init__(self, adb_helper=None):
        """
        Args:
            adb_helper: Instance de ADBHelper (optionnel)
        """
        self.adb = adb_helper
    
    def compare_region(
        self, 
        screenshot_path: str, 
        reference_image_path: str, 
        region: Tuple[int, int, int, int],
        threshold: float = 0.95
    ) -> Tuple[bool, float]:
        """
        Compare une région du screenshot avec une image de référence
        
        Args:
            screenshot_path: Chemin du screenshot complet
            reference_image_path: Chemin de l'image de référence à comparer
            region: Tuple (x, y, width, height) ou (x1, y1, x2, y2) de la région à extraire
            threshold: Seuil de similarité (0.0 à 1.0), au-dessus duquel c'est considéré comme match
        
        Returns:
            Tuple (is_match: bool, similarity_score: float)
        """
        # Résoudre les chemins relatifs vers la racine du projet
        if self.adb:
            resolved_screenshot_path = self.adb._resolve_path(screenshot_path)
            resolved_reference_path = self.adb._resolve_path(reference_image_path)
        else:
            # Si pas d'ADBHelper, utiliser les chemins tel quel
            resolved_screenshot_path = screenshot_path
            resolved_reference_path = reference_image_path
        
        # Vérifier que les fichiers existent
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
            # Charger les images avec les chemins résolus
            screenshot = Image.open(resolved_screenshot_path)
            reference = Image.open(resolved_reference_path)
            
            # Extraire la région du screenshot
            # Accepte deux formats: (x, y, width, height) ou (x1, y1, x2, y2)
            if len(region) == 4:
                x1, y1, val3, val4 = region
                # Détection automatique du format:
                # Si val3 > x1 ET val4 > y1, c'est probablement (x1, y1, x2, y2)
                # Sinon, c'est (x, y, width, height)
                if val3 > x1 and val4 > y1:
                    # Format (x1, y1, x2, y2) - utiliser directement
                    screenshot_region = screenshot.crop((x1, y1, val3, val4))
                else:
                    # Format (x, y, width, height)
                    screenshot_region = screenshot.crop((x1, y1, x1 + val3, y1 + val4))
            else:
                screenshot_region = screenshot.crop(region)
            
            # Redimensionner si nécessaire (les images doivent avoir la même taille)
            if screenshot_region.size != reference.size:
                screenshot_region = screenshot_region.resize(reference.size, Image.Resampling.LANCZOS)
            
            # Calculer la similarité
            similarity = self._calculate_similarity(screenshot_region, reference)
            
            return similarity >= threshold, similarity
        finally:
            # Fermer les images pour libérer les fichiers
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
        """
        Prend un screenshot, extrait une région et la compare avec une référence
        (Méthode tout-en-un si vous avez un ADBHelper)
        
        Args:
            reference_image_path: Chemin de l'image de référence
            region: Tuple (x, y, width, height) de la région
            threshold: Seuil de similarité
            temp_screenshot: Nom temporaire pour le screenshot
        
        Returns:
            Tuple (is_match: bool, similarity_score: float)
        """
        if not self.adb:
            raise ValueError("ADBHelper requis pour cette méthode")
        
        # Prendre un screenshot
        if not self.adb.screenshot(temp_screenshot):
            return False, 0.0
        
        try:
            # Comparer la région
            return self.compare_region(
                temp_screenshot, 
                reference_image_path, 
                region, 
                threshold
            )
        finally:
            # Nettoyer le fichier temporaire (optionnel)
            if os.path.exists(temp_screenshot):
                os.remove(temp_screenshot)
    
    def _calculate_similarity(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Calcule la similarité entre deux images (0.0 à 1.0)
        
        Args:
            img1: Première image (PIL Image)
            img2: Deuxième image (PIL Image)
        
        Returns:
            Score de similarité entre 0.0 et 1.0
        """
        # Convertir en RGB si nécessaire
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        if img2.mode != 'RGB':
            img2 = img2.convert('RGB')
        
        # Vérifier que les images ont la même taille
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
        
        # Méthode: Différence RMS (Root Mean Square Error)
        diff = ImageChops.difference(img1, img2)
        
        # Calculer le RMS depuis l'histogramme de différence
        # L'histogramme retourne [R0...R255, G0...G255, B0...B255]
        hist = diff.histogram()
        total_pixels = img1.size[0] * img1.size[1] * 3  # 3 canaux RGB
        
        # Calculer la somme des carrés des différences
        # Pour chaque canal (R, G, B), on a 256 valeurs (0-255)
        sum_squared_diff = 0.0
        for channel in range(3):  # R, G, B
            for pixel_value in range(256):
                count = hist[channel * 256 + pixel_value]
                # La valeur du pixel représente la différence (0 = identique, 255 = max diff)
                sum_squared_diff += (pixel_value ** 2) * count
        
        # Calculer RMS (Root Mean Square)
        if total_pixels > 0:
            rms = math.sqrt(sum_squared_diff / total_pixels)
        else:
            rms = 255.0
        
        # Normaliser: RMS max = 255 (différence maximale), min = 0 (images identiques)
        # Similarité = 1 - (RMS / 255)
        similarity = 1.0 - (rms / 255.0)
        
        return max(0.0, min(1.0, similarity))  # Clamper entre 0 et 1
    
    def find_template_in_screenshot(
        self,
        screenshot_path: str,
        template_path: str,
        threshold: float = 0.8
    ) -> Optional[Tuple[int, int]]:
        """
        Cherche un template (petite image) dans un screenshot
        Retourne la position (x, y) du centre du template trouvé, ou None
        
        Args:
            screenshot_path: Chemin du screenshot complet
            template_path: Chemin de l'image template à chercher
            threshold: Seuil de correspondance minimum
        
        Returns:
            Tuple (x, y) du centre trouvé, ou None si pas trouvé
        """
        try:
            import numpy as np
            from scipy import ndimage
        except ImportError:
            print("scipy requis pour find_template_in_screenshot. Installez: pip install scipy")
            return None
        
        # Résoudre le chemin du template vers la racine du projet
        if self.adb:
            resolved_template_path = self.adb._resolve_path(template_path)
        else:
            resolved_template_path = template_path
        
        screenshot = np.array(Image.open(screenshot_path))
        template = np.array(Image.open(resolved_template_path))
        
        # Convertir en niveaux de gris
        if len(screenshot.shape) == 3:
            screenshot_gray = np.mean(screenshot, axis=2)
        else:
            screenshot_gray = screenshot
        
        if len(template.shape) == 3:
            template_gray = np.mean(template, axis=2)
        else:
            template_gray = template
        
        # Template matching simple (corrélation normalisée)
        result = ndimage.correlate(
            screenshot_gray.astype(float),
            template_gray.astype(float),
            mode='constant'
        )
        
        # Normaliser le résultat
        result = result / (np.max(result) + 1e-10)
        
        # Trouver le maximum
        max_val = np.max(result)
        if max_val >= threshold:
            max_pos = np.unravel_index(np.argmax(result), result.shape)
            # Retourner le centre du template
            template_center_x = max_pos[1] + template.shape[1] // 2
            template_center_y = max_pos[0] + template.shape[0] // 2
            return (template_center_x, template_center_y)
        
        return None


# ==================== Constantes ====================

class KeyCode:
    """Constantes pour les codes de touches Android"""
    BACK = 4
    HOME = 3
    MENU = 187
    RECENT = 187
    POWER = 26
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    ENTER = 66
    DELETE = 67
