import sys
import os
import importlib.util
from fastapi import APIRouter

sys.path.append("/mnt/user/ASTRO/")  # ✅ Ajout du chemin correct

router = APIRouter()

MODULES_PATH = "/mnt/ASTRO/modules"
SPECIAL_MODULES = ["/mnt/ASTRO/backend/routes/chat.py"]  # 📌 Liste des modules spécifiques à inclure

# ✅ Assurez-vous que tout est bien indenté à l'intérieur de la fonction load_modules()
def load_modules():
    """ Charge dynamiquement tous les modules trouvés dans le dossier /modules et les modules spéciaux """
    loaded_modules = []

    if not os.path.exists(MODULES_PATH):
        print(f"❌ Le dossier des modules {MODULES_PATH} n'existe pas.")
        return []

    # 📌 Charger tous les modules depuis `/modules`
    for module_name in os.listdir(MODULES_PATH):
        module_path = os.path.join(MODULES_PATH, module_name, f"{module_name}.py")

        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "router"):
                router.include_router(module.router, prefix=f"/{module_name}")  # ✅ Ajout du module à l'API
                loaded_modules.append(module_name)
                print(f"✅ Module {module_name} chargé avec succès !")
            else:
                print(f"⚠️ Module {module_name} ignoré (pas de router détecté).")

    # 📌 Charger aussi `chat.py` (et autres modules spéciaux)
    for special_module in SPECIAL_MODULES:
        if os.path.exists(special_module):
            module_name = os.path.basename(special_module).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, special_module)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(f"🔍 Vérification du module {module_name}: {module}")

            if hasattr(module, "router"):
                print(f"✅ Le module {module_name} a bien un routeur FastAPI !")
                router.include_router(module.router, prefix=f"/{module_name}")  # ✅ Ajout automatique
                print(f"🚀 Route ajoutée dynamiquement : /{module_name}")  # ✅ Log pour vérification
                loaded_modules.append(module_name)
                print(f"✅ Module spécial {module_name} chargé avec succès !")
            else:
                print(f"⚠️ Le module {module_name} N'A PAS de routeur FastAPI. Il sera ignoré.")

    return loaded_modules  # ✅ Bien indenté à l'intérieur de `load_modules()`

# 📌 Charger les modules au démarrage
load_modules()
