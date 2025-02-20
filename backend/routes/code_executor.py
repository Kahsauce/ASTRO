from fastapi import APIRouter

router = APIRouter()

@router.get("/execute")
def execute_code():
    return {"message": "Exécution de code prête"}
