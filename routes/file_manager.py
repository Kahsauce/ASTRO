import os
from fastapi import APIRouter, HTTPException, Query, Body

router = APIRouter()

BASE_PATH = "/app/storage"  # Dossier de stockage dans le conteneur

# Assurer que le dossier de stockage existe
os.makedirs(BASE_PATH, exist_ok=True)

@router.post("/create_file")
def create_file(
    filename: str = Query(None, description="Nom du fichier"),
    content: str = Query("", description="Contenu du fichier"),
    body: dict = Body(None)
):
    """Créer un fichier avec du contenu."""
    # Prioriser les données JSON si fournies
    if body:
        filename = body.get("filename", filename)
        content = body.get("content", content)

    if not filename:
        raise HTTPException(status_code=400, detail="Le nom du fichier est requis")

    file_path = os.path.join(BASE_PATH, filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Fichier déjà existant")
    
    with open(file_path, "w") as f:
        f.write(content)

    return {"message": "Fichier créé", "filename": filename}

@router.get("/read_file")
def read_file(filename: str = Query(..., description="Nom du fichier")):
    """Lire le contenu d'un fichier."""
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    
    with open(file_path, "r") as f:
        content = f.read()
    
    return {"filename": filename, "content": content}

@router.put("/update_file")
def update_file(
    filename: str = Query(None, description="Nom du fichier à mettre à jour"),
    content: str = Query(None, description="Nouveau contenu à écrire"),
    body: dict = Body(None)
):
    """Mettre à jour un fichier existant."""
    # Prioriser les données JSON si fournies
    if body:
        filename = body.get("filename", filename)
        content = body.get("content", content)

    if not filename or not content:
        raise HTTPException(status_code=400, detail="Filename et content sont requis")

    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    with open(file_path, "w") as f:
        f.write(content)

    return {"message": "Fichier mis à jour", "filename": filename}

@router.delete("/delete_file")
def delete_file(filename: str = Query(..., description="Nom du fichier à supprimer")):
    """Supprimer un fichier."""
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    
    os.remove(file_path)
    return {"message": "Fichier supprimé", "filename": filename}
