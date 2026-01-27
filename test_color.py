"""
Script de test pour vérifier la couleur RGB à un endroit précis
Utile pour déboguer et trouver les bonnes coordonnées/couleurs
"""

from utils.adb_helper import auto_setup_adb
import time

# Configuration automatique de ADB
adb = auto_setup_adb(verbose=True)

print("\n" + "="*60)
print("🎨 TEST DE DÉTECTION DE COULEUR RGB")
print("="*60)

# Coordonnées à tester (modifiez selon vos besoins)
x = 551
y = 189

# Couleur cible avec tolérance (optionnel)
# Si défini, le script vérifiera si la couleur correspond à la cible
target_color = None  # Exemple: (255, 0, 0) pour rouge
tolerance = 10  # Tolérance ±10 pour chaque canal RGB

# Exemple d'utilisation:
# target_color = (255, 0, 0)  # Chercher du rouge
# tolerance = 15  # Avec une tolérance de ±15

print(f"\n📍 Position à tester: ({x}, {y})")
if target_color:
    print(f"🎯 Couleur cible: RGB{target_color} (tolérance: ±{tolerance})")
print("💡 Modifiez les variables x, y, target_color et tolerance dans le script\n")

# Prendre un screenshot pour référence
print("📸 Capture d'écran...")
adb.screenshot("test_color_screen.png")
print("✓ Screenshot sauvegardé: test_color_screen.png\n")

# Boucle pour vérifier la couleur en continu
print("🔄 Vérification de la couleur en continu (Ctrl+C pour arrêter)...")
print("-" * 60)

try:
    while True:
        # Récupérer la couleur à la position
        color = adb.get_color_at(x, y)
        
        if color:
            r, g, b = color
            # Afficher la couleur avec un code couleur ANSI (si supporté)
            print(f"RGB({r:3d}, {g:3d}, {b:3d}) à ({x}, {y})", end="")
            
            # Vérifier si la couleur correspond à la cible (avec tolérance)
            if target_color:
                target_r, target_g, target_b = target_color
                match = (
                    abs(r - target_r) <= tolerance and
                    abs(g - target_g) <= tolerance and
                    abs(b - target_b) <= tolerance
                )
                
                if match:
                    print(" ✅ MATCH!", end="")
                else:
                    # Afficher la différence
                    diff_r = r - target_r
                    diff_g = g - target_g
                    diff_b = b - target_b
                    print(f" ❌ (diff: R{diff_r:+d}, G{diff_g:+d}, B{diff_b:+d})", end="")
            
            # Afficher un aperçu de la couleur (approximatif)
            if r > 200 and g < 50 and b < 50:
                print(" 🔴 (Rouge)")
            elif r < 50 and g > 200 and b < 50:
                print(" 🟢 (Vert)")
            elif r < 50 and g < 50 and b > 200:
                print(" 🔵 (Bleu)")
            elif r > 200 and g > 200 and b < 50:
                print(" 🟡 (Jaune)")
            elif r > 200 and g > 200 and b > 200:
                print(" ⚪ (Blanc)")
            elif r < 50 and g < 50 and b < 50:
                print(" ⚫ (Noir)")
            else:
                print()
        else:
            print(f"❌ Impossible de récupérer la couleur à ({x}, {y})")
        
        time.sleep(0.5)  # Attendre 0.5 secondes entre chaque vérification

except KeyboardInterrupt:
    print("\n\n✅ Test arrêté par l'utilisateur")

print("\n" + "="*60)
print("💡 ASTUCES:")
print("="*60)
print("1. Modifiez x et y dans le script pour tester d'autres positions")
print("2. Définissez target_color pour vérifier une couleur spécifique")
print("3. Ajustez tolerance pour être plus ou moins strict (±10 par défaut)")
print("4. Utilisez le screenshot 'test_color_screen.png' pour voir l'écran")
print("5. Les valeurs RGB vont de 0 à 255")
print("\n📝 Exemple d'utilisation avec tolérance:")
print("   target_color = (255, 0, 0)  # Rouge")
print("   tolerance = 15  # Accepte RGB(240-255, 0-15, 0-15)")
print("="*60)

