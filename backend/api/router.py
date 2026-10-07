from fastapi import APIRouter
from backend.api.endpoints import router as ingest_router

api_router = APIRouter()

@api_router.get("/status")
def api_status():
    return {"message": "API Router is configured."}

# Adiciona as rotas dos endpoints
api_router.include_router(ingest_router, tags=["ingestion"])

