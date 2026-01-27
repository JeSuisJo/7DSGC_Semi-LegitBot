"""
Exemple complet de toutes les commandes ADB disponibles
Utilisez ce fichier comme référence pour toutes les fonctionnalités
"""

from utils.adb_helper import auto_setup_adb, get_adb, KeyCode
import time

# ==================== INITIALISATION ====================

# Méthode recommandée: Configuration automatique (détecte MuMu, BlueStacks, Nox)
adb = auto_setup_adb(verbose=True)

# Ou méthode manuelle:
# adb = get_adb()
# adb = get_adb(device_id="127.0.0.1:5555")  # Spécifier un appareil


# ==================== GESTION DES APPAREILS ====================

# Lister tous les appareils connectés
devices = adb.get_devices()
print(f"Appareils connectés: {devices}")

# Afficher les appareils avec leur type (MuMu, BlueStacks, Nox, etc.)
adb.print_devices_with_info()

# Détecter un émulateur spécifique
mumu = adb.find_mumu_device()
bluestacks = adb.find_bluestacks_device()
nox = adb.find_nox_device()

# Changer d'appareil
adb.set_device("127.0.0.1:5555")  # Spécifier un ID
current_device = adb.get_current_device()
print(f"Appareil actuel: {current_device}")

# Sélection automatique d'appareil
adb.auto_select_device(prefer_mumu=True)

# Vérifier la connexion
if adb.is_device_connected():
    print("✓ Appareil connecté")
else:
    print("✗ Aucun appareil connecté")

# Attendre qu'un appareil soit connecté
# adb.wait_for_device(timeout=30)


# ==================== CAPTURE D'ÉCRAN ====================

# Prendre un screenshot
adb.screenshot("screen.png")
adb.screenshot("screenshots/battle.png")  # Dans un sous-dossier

# Capturer une région précise (utile pour débogage)
adb.capture_region(
    region=(175, 997, 218, 1032),  # (x1, y1, x2, y2) ou (x, y, width, height)
    save_path="debug_region.png"
)

# Récupérer screenshot en bytes (sans fichier)
screenshot_bytes = adb.get_screenshot_bytes()


# ==================== INPUT (TOUCHES, SWIPES) ====================

# Tap simple
adb.tap(500, 1000)

# Long press (tap avec durée)
adb.tap(500, 1000, duration=1000)  # 1 seconde

# Swipe
adb.swipe(100, 200, 300, 400, duration=300)  # De (100,200) vers (300,400) en 300ms

# Envoyer du texte
adb.input_text("Hello World")

# Touches système
adb.press_back()      # Touche retour
adb.press_home()      # Touche accueil
adb.press_menu()      # Touche menu

# Autres touches (voir KeyCode pour toutes les options)
adb.input_keyevent(KeyCode.BACK)      # 4
adb.input_keyevent(KeyCode.HOME)      # 3
adb.input_keyevent(KeyCode.MENU)      # 187
adb.input_keyevent(KeyCode.POWER)     # 26
adb.input_keyevent(KeyCode.VOLUME_UP) # 24
adb.input_keyevent(KeyCode.VOLUME_DOWN) # 25
adb.input_keyevent(KeyCode.ENTER)    # 66


# ==================== DÉTECTION D'IMAGE ====================

# Chercher un template dans tout l'écran
position = adb.find_image("img/button.png", threshold=0.8)
if position:
    x, y = position
    print(f"Image trouvée à ({x}, {y})")
    adb.tap(x, y)

# Comparer une région précise avec une image de référence
is_match, similarity = adb.compare_region_with_image(
    reference_image_path="img/prep.png",
    region=(175, 997, 218, 1032),  # Format (x1, y1, x2, y2) ou (x, y, width, height)
    threshold=0.9
)
if is_match:
    print(f"Image trouvée! Similarité: {similarity:.2%}")

# Boucle pour attendre qu'une image apparaisse
while True:
    is_match, similarity = adb.compare_region_with_image(
        reference_image_path="img/prep.png",
        region=(175, 997, 218, 1032),
        threshold=0.9
    )
    if is_match:
        print("Image trouvée!")
        break
    time.sleep(0.5)


# ==================== DÉTECTION DE COULEUR ====================

# Récupérer la couleur à une position précise
color = adb.get_color_at(500, 1000)  # Retourne (R, G, B)
if color:
    r, g, b = color
    print(f"Couleur à (500, 1000): RGB({r}, {g}, {b})")
    
    # Vérifier si c'est une couleur spécifique (exact)
    if color == (255, 0, 0):  # Rouge
        print("Bouton rouge détecté!")

# Détection avec tolérance (nouveau!)
color_with_tolerance = adb.get_color_at(
    500, 1000,
    target_color=(255, 0, 0),  # Chercher du rouge
    tolerance=15  # Tolérance ±15 pour chaque canal
)
if color_with_tolerance:
    print("Bouton rouge détecté (avec tolérance)!")

# Comparer deux couleurs avec tolérance (méthode globale)
from utils.adb_helper import ADBHelper
color1 = (255, 0, 0)
color2 = (250, 5, 8)  # Rouge légèrement différent
if ADBHelper.color_matches(color1, color2, tolerance=10):
    print("Les couleurs correspondent!")

# Chercher une couleur dans une région
matches = adb.find_color_in_region(
    target_color=(255, 0, 0),  # Rouge
    region=(0, 0, 500, 500),   # (x, y, width, height)
    tolerance=10               # Tolérance ±10 pour chaque canal RGB
)
print(f"Trouvé {len(matches)} pixels avec cette couleur")

# Attendre qu'une couleur apparaisse à une position
found = adb.wait_for_color(
    target_color=(255, 0, 0),  # Rouge
    position=(500, 1000),
    tolerance=10,
    timeout=5.0,               # Timeout de 5 secondes
    check_interval=0.5          # Vérifier toutes les 0.5 secondes
)
if found:
    print("Couleur trouvée!")


# ==================== COMMANDES SHELL ====================

# Exécuter une commande shell sur l'appareil
output, return_code = adb.shell("echo 'Hello from Android'")
print(f"Output: {output}, Code: {return_code}")

# Exemples de commandes shell utiles
adb.shell("pm list packages")  # Lister les packages
adb.shell("dumpsys battery")    # Info batterie
adb.shell("getprop ro.build.version.release")  # Version Android


# ==================== GESTION D'APPLICATIONS ====================

# Obtenir le package de l'app en cours
current_package = adb.get_current_package()
print(f"Application actuelle: {current_package}")

# Lancer une application
adb.launch_app("com.example.app", "com.example.app.MainActivity")

# Arrêter une application
adb.stop_app("com.example.app")


# ==================== TRANSFERT DE FICHIERS ====================

# Envoyer un fichier vers l'appareil
adb.push_file("local_file.txt", "/sdcard/remote_file.txt")

# Récupérer un fichier depuis l'appareil
adb.pull_file("/sdcard/remote_file.txt", "local_file.txt")


# ==================== EXEMPLE COMPLET: AUTOMATISATION ====================

def exemple_automatisation():
    """Exemple d'automatisation complète"""
    adb = auto_setup_adb(verbose=False)
    
    # 1. Attendre qu'un bouton apparaisse
    print("Attente du bouton...")
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path="img/start_button.png",
            region=(100, 200, 150, 50),
            threshold=0.85
        )
        if is_match:
            print(f"Bouton trouvé! Similarité: {similarity:.2%}")
            break
        time.sleep(0.5)
    
    # 2. Cliquer sur le bouton
    adb.tap(175, 225)  # Centre de la région
    time.sleep(1)
    
    # 3. Attendre qu'une couleur change (indique que l'action est terminée)
    found = adb.wait_for_color(
        target_color=(0, 255, 0),  # Vert
        position=(500, 500),
        tolerance=10,
        timeout=10.0
    )
    
    if found:
        print("Action terminée!")
        # 4. Prendre un screenshot final
        adb.screenshot("result.png")


# ==================== CONSTANTES KEYCODE ====================

# Toutes les touches disponibles via KeyCode:
print("\nTouches disponibles:")
print(f"BACK = {KeyCode.BACK}")
print(f"HOME = {KeyCode.HOME}")
print(f"MENU = {KeyCode.MENU}")
print(f"POWER = {KeyCode.POWER}")
print(f"VOLUME_UP = {KeyCode.VOLUME_UP}")
print(f"VOLUME_DOWN = {KeyCode.VOLUME_DOWN}")
print(f"ENTER = {KeyCode.ENTER}")
print(f"DELETE = {KeyCode.DELETE}")


# ==================== NOTES IMPORTANTES ====================

"""
FORMATS DE RÉGION:
- Format 1: (x1, y1, x2, y2) - Coordonnées de début et fin
  Exemple: (175, 997, 218, 1032)
  
- Format 2: (x, y, width, height) - Position + dimensions
  Exemple: (175, 997, 43, 35)

Le code détecte automatiquement le format utilisé.

CHEMINS D'IMAGES:
- Les chemins sont relatifs à la racine du projet
- Exemple: "img/prep.png" cherche dans le dossier img/ à la racine

THRESHOLDS:
- threshold=0.9 signifie 90% de similarité minimum
- Plus le threshold est bas, plus c'est permissif
- Recommandé: 0.85-0.95 pour la plupart des cas
"""
