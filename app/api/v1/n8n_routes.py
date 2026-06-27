from fastapi import APIRouter, Depends
from app.core.security import get_api_key

router = APIRouter()

@router.post("/trigger-n8n")
def trigger_n8n_flow(api_key: str = Depends(get_api_key)):
    # Aquí llamas al flujo n8n
    return {"message": "Flujo disparado correctamente"}
