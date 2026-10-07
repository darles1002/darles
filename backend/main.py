from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import api_router

app = FastAPI(
    title="RAG + Teophilo API",
    description="API para ingestão e consulta de documentos usando RAG.",
    version="1.0.0"
)

# Configurando CORS para permitir que o frontend converse com o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Atenção: Em produção, especificar a origem real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend FastAPI rodando."}
