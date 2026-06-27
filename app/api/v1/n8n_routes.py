from fastapi import APIRouter, Depends
from app.api.deps import require_api_key

router = APIRouter()

@router.post("/trigger-n8n", dependencies=[Depends(require_api_key)])
def trigger_n8n_flow():
    # Aquí llamas al flujo n8n
    return {"message": "Flujo disparado correctamente"}
