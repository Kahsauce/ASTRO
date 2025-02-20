import sys
import os
import importlib.util
from fastapi import APIRouter, FastAPI, HTTPException

sys.path.append("/mnt/user/ASTRO/")  # ✅ Assurer que le chemin est pris en compte

router = APIRouter()
MODULES_PATH = "/mnt//ASTRO/modules"  # 📌 Dossier des modules dynamiques

def load_modules(app: FastAPI):
    """Charge dynamiquement tous les modules dans /modules et les ajoute à FastAPI"""
    modules_loaded = []

    # 📌 Vérifier que le dossier des modules existe
    if not os.path.exists(MODULES_PATH):
        os.makedirs(MODULES_PATH)

    for module_name in os.listdir(MODULES_PATH):
        module_path = os.path.join(MODULES_PATH, module_name, f"{module_name}.py")

        # 📌 Vérifier que le module est valide avant de l'importer
        if os.path.exists(module_path):
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 📌 Vérifier si le module a une variable `router`
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=f"/api/{module_name}")
                    modules_loaded.append(module_name)
                    print(f"✅ Module {module_name} chargé avec succès !")
                else:
                    print(f"⚠️ Le module {module_name} n'a pas de `router`, il n'est pas ajouté à l'API.")

            except Exception as e:
                print(f"❌ Erreur lors du chargement du module {module_name} : {e}")

    return modules_loaded

@router.post("/modules/install")
def install_module(module_name: str):
    """Simule l'installation d'un module"""
    module_path = os.path.join(MODULES_PATH, module_name)

    if os.path.exists(module_path):
        raise HTTPException(status_code=400, detail="Le module existe déjà")

    os.makedirs(module_path)
    with open(os.path.join(module_path, "__init__.py"), "w") as f:
        f.write("# Module Auto-généré\n")

    # 📌 Générer un fichier de route dynamique pour le module
    route_code = f"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello():
    return {{"message": "Module {module_name} installé avec succès !"}}
    """
    with open(os.path.join(module_path, f"{module_name}.py"), "w") as f:
        f.write(route_code)

    return {"message": f"Module {module_name} installé et prêt à être utilisé !"}

