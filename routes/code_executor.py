import os
import subprocess
from fastapi import APIRouter, HTTPException, Query, Body

router = APIRouter()

BASE_PATH = "/app/code_storage"  # Dossier où seront stockés les scripts

# Assurer que le dossier de stockage existe
os.makedirs(BASE_PATH, exist_ok=True)

@router.post("/execute_code")
def execute_code(
    filename: str = Query(None, description="Nom du fichier à exécuter"),
    code: str = Query(None, description="Code Python à exécuter"),
    body: dict = Body(None)
):
    """Exécuter un script Python fourni ou stocké."""
    
    # Si un body JSON est envoyé, récupérer les données de là
    if body:
        filename = body.get("filename", filename)
        code = body.get("code", code)

    if not filename and not code:
        raise HTTPException(status_code=400, detail="Un nom de fichier ou du code est requis")

    file_path = os.path.join(BASE_PATH, filename) if filename else None

    # Si un code est fourni, on l'écrit dans un fichier temporaire
    if code:
        if not filename:
            filename = "temp_script.py"
        file_path = os.path.join(BASE_PATH, filename)
        with open(file_path, "w") as f:
            f.write(code)

    # Vérifier si le fichier existe avant l'exécution
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    try:
        # Exécuter le script en capturant la sortie et les erreurs
        result = subprocess.run(
            ["python3", file_path], capture_output=True, text=True, timeout=10
        )
        output = result.stdout
        error = result.stderr

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="L'exécution du script a dépassé le temps limite")

    return {
        "filename": filename,
        "output": output,
        "error": error
    }
