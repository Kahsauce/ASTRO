from fastapi import FastAPI, Request
import sys
import os
import importlib
from dotenv import load_dotenv

# 📌 Charger les variables d'environnement
load_dotenv('/mnt/user/ASTRO/.env')  # Assurez-vous que le fichier .env est bien présent

# 📌 Configuration de l'API
sys.path.append("/mnt/ASTRO/")
sys.path.append("/mnt/ASTRO/backend")
from module_manager import load_modules  # ✅ Charge les modules dynamiquement
from config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# 📌 Inclure les modules dynamiques automatiquement
loaded_modules = load_modules(app)

@app.get("/")
def read_root():
    return {"message": "Orchestrateur Astro est en ligne !"}

@app.get("/ping")
def ping():
    return {"message": "Orchestrateur fonctionne"}

# ✅ Endpoint `/api/message` pour l'interface web
@app.post("/api/message")
async def receive_message(request: Request):
    """Reçoit un message de l'interface web et retourne une réponse"""
    data = await request.json()
    print(f"📩 Message reçu : {data}")  # 🔍 Debug
    return {"message": f"Tu as envoyé : {data}"}

# ✅ Vérifier quels modules sont chargés
@app.get("/api/modules")
def list_modules():
    """Retourne la liste des modules dynamiquement chargés"""
    return {"loaded_modules": loaded_modules}

if __name__ == '__main__':
    import uvicorn
    print("🚀 Démarrage de FastAPI...")  # 🔍 Debug
    uvicorn.run(app, host='0.0.0.0', port=settings.PORT)
