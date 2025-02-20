import os
import subprocess
from fastapi import APIRouter, HTTPException, Query, Body
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement
load_dotenv('/mnt/user/ASTRO/.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()
BASE_PATH = "/mnt/user/ASTRO/code_storage"  # Dossier où seront stockés les scripts

# Assurer que le dossier de stockage existe
os.makedirs(BASE_PATH, exist_ok=True)

@router.post("/generate_and_execute")
def generate_and_execute_code(
    prompt: str = Query(..., description="Demande à OpenAI pour générer du code"),
    filename: str = Query("generated_script.py", description="Nom du fichier pour stocker le code généré")
):
    """ Génère un script avec OpenAI, le stocke et l'exécute. """
    
    try:
        # Générer du code avec OpenAI
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Tu es un assistant qui génère du code Python efficace et optimisé."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )

        if not response.choices or not response.choices[0].message:
            raise HTTPException(status_code=500, detail="Réponse vide de l'API OpenAI.")

        generated_code = response.choices[0].message["content"]

        # Stocker le code généré dans un fichier
        file_path = os.path.join(BASE_PATH, filename)
        with open(file_path, "w") as f:
            f.write(generated_code)

        # Vérifier si le fichier existe avant l'exécution
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Fichier introuvable après génération")

        # Exécuter le script en capturant la sortie et les erreurs
        try:
            result = subprocess.run(
                ["python3", file_path], capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            error = result.stderr
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=500, detail="L'exécution du script a dépassé le temps limite")

        return {
            "filename": filename,
            "generated_code": generated_code,
            "output": output,
            "error": error
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
