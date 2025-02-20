import os
import sys
import logging
import uvicorn
from fastapi import FastAPI, Request

# ✅ Ajouter le répertoire courant au PYTHONPATH si besoin
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ✅ Import des settings et des autres modules locaux
from config.settings import settings
import module_manager
from module_manager import router as module_router, load_modules
import routes.base as base_router
import routes.file_manager as file_router
import routes.code_executor as code_router

# -- Création de l'application FastAPI
app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# -- Inclure les modules dynamiques automatiquement
loaded_modules = load_modules()

# -- Inclure les routers statiques (locaux)
app.include_router(base_router.router)
app.include_router(file_router.router)
app.include_router(code_router.router)
app.include_router(module_router)  # Chargement des modules dynamiques

@app.get("/")
def read_root():
    return {"message": "Orchestrateur Astro est en ligne !"}

@app.get("/ping")
def ping():
    return {"message": "Orchestrateur fonctionne"}

# -- Endpoint `/api/message` pour l'interface web
@app.post("/api/message")
async def receive_message(request: Request):
    data = await request.json()
    print(f"📩 Message reçu : {data}")
    return {"message": f"Tu as envoyé : {data}"}

# -- Endpoint `/api/modules` pour lister les modules chargés
@app.get("/api/modules")
def list_modules():
    """Retourne la liste des modules dynamiquement chargés"""
    return {"loaded_modules": loaded_modules}

# -- Configuration du logging
logging.basicConfig(level=logging.DEBUG)

# -- Affichage des routes pour le debug
print("\n🔍 Vérification : Routes enregistrées dans FastAPI :")
for route in app.router.routes:
    print(f"➡ {route.path} ({route.methods})")

# -- Démarrer l'API si exécuté directement
if __name__ == "__main__":
    print("🚀 Démarrage de FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
