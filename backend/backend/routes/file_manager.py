from fastapi import APIRouter

router = APIRouter()

@router.get("/files")
def list_files():
    return {"message": "Gestion des fichiers prête"}
