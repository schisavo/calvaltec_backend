from fastapi import APIRouter

router = APIRouter()


@router.post("/trigger-n8n")
def trigger_n8n_flow():
    return {"message": "Flujo disparado correctamente"}
