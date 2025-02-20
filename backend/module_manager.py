import sys
import os
import json
import importlib.util
from fastapi import APIRouter

sys.path.append("/mnt/ASTRO/")  # ✅ Ajout du chemin correct

router = APIRouter()

modules_dir = "/mnt/ASTRO/modules"

def load_modules():
    """ Charge dynamiquement tous les modules trouvés dans le dossier /modules """
    loaded_modules = []
    
    if not os.path.exists(modules_dir):
        print(f"❌ Le dossier des modules {modules_dir} n'existe pas.")
        return []

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name, f"{module_name}.py")
        
        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            router.include_router(module.router, prefix=f"/{module_name}")  # ✅ Ajout du module à l'API
            loaded_modules.append(module_name)

    print(f"✅ Modules chargés : {loaded_modules}")
    return loaded_modules
load_modules()  # Charger les modules au démarrage
