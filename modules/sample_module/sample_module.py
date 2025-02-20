from fastapi import APIRouter

router = APIRouter()

@router.get("/test_endpoint")
async def test():
    return {"message": "Module Sample fonctionne"}
