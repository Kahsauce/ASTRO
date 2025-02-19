from fastapi import FastAPI
from routes.base import router as base_router
from routes.file_manager import router as file_router
from routes.code_executor import router as code_router  # ✅ Import OK
from app.config.settings import settings

# 🔥 Ajout de root_path pour gérer la redirection via "/api/"
app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION, root_path="/api")

# 📌 Inclure les routes
app.include_router(base_router)
app.include_router(file_router)
app.include_router(code_router)  # ✅ Inclusion OK

@app.get("/")
def read_root():
    return {"message": "Orchestrateur Astro est en ligne !"}

@app.get("/ping")
def ping():
    return {"message": "Orchestrateur fonctionne"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings.PORT)
