from fastapi import FastAPI, Request
from routes.base import router as base_router
from routes.file_manager import router as file_router
from routes.code_executor import router as code_router
import sys
sys.path.append("/mnt/ASTRO/")  # ✅ Ajout du bon chemin

from backend.module_manager import router as module_router  # ✅ Ajout des modules dynamiques

from config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)  # Supprimer root_path="/api"

# 📌 Inclure les routes
app.include_router(base_router)
app.include_router(file_router)
app.include_router(code_router)
app.include_router(module_router)  # ✅ Assurer que les modules sont bien inclus

@app.get("/")
def read_root():
    return {"message": "Orchestrateur Astro est en ligne !"}

@app.get("/ping")
def ping():
    return {"message": "Orchestrateur fonctionne"}

# ✅ Ajout de l'endpoint `/api/message`
@app.post("/api/message")
async def receive_message(request: Request):
    """Reçoit un message de l'interface web et retourne une réponse"""
    data = await request.json()
    print(f"📩 Message reçu : {data}")  # 🔍 Debug
    return {"message": f"Tu as envoyé : {data}"}

if __name__ == '__main__':
    import uvicorn
    print("🚀 Démarrage de FastAPI...")  # 🔍 Debug
    uvicorn.run(app, host='0.0.0.0', port=settings.PORT)
