from fastapi import APIRouter
import os

from backend.services.document_processor import process_documents
from backend.services.chunker import chunk_document
from backend.services.tokenizer import tokenize_all_chunks
from backend.services.embedder import embed_chunks
from backend.services.supabase_client import salvar_documento, salvar_chunks

router = APIRouter()

@router.post("/ingest")
def ingest_documents():
    """
    Endpoint (Etapa 11) que executa todo o pipeline de ingestão:
    Leitura de PDF -> Extração -> Chunking -> Tokenização -> Embedding -> Supabase.
    """
    # Define o diretório dos documentos
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs"))
    
    # Etapa 5 & 6: Extração de texto e estruturação
    documentos_estruturados = process_documents(docs_path)
    
    if not documentos_estruturados:
        return {"message": "Nenhum documento encontrado para ingestão.", "status": "aguardando"}
        
    resultado_ingestao = []
    
    for doc in documentos_estruturados:
        doc_id = doc["documento_id"]
        
        # Salva o pai (documento_id) no BD
        salvar_documento(doc)
        
        # Etapa 7: Chunking
        chunks = chunk_document(doc)
        
        # Etapa 8: Tokenização explícita
        chunks_tokenizados = tokenize_all_chunks(chunks)
        
        # Etapa 9: Gerar Embeddings
        chunks_com_vetor = embed_chunks(chunks_tokenizados)
        
        # Etapa 10 (uso): Salvar no Supabase (PGVector)
        salvar_chunks(chunks_com_vetor)
        
        resultado_ingestao.append({
            "documento_id": doc_id,
            "chunks_processados": len(chunks_com_vetor),
            "status": "concluída"
        })
        
    return {
        "message": "Ingestão concluída com sucesso.",
        "detalhes": resultado_ingestao
    }

from pydantic import BaseModel

class QueryRequest(BaseModel):
    pergunta: str
    top_k: int = 5
    # Futuramente: base_id: str para filtro (Etapa 14)

from backend.services.retriever import retrieve_documents
from backend.services.llm_service import ask_llm

@router.post("/query")
def query_rag(request: QueryRequest):
    """
    Endpoint para realizar consultas (Etapas 12 a 18).
    Recebe a pergunta, busca contextos similares e consulta o LLM.
    """
    pergunta = request.pergunta
    
    # Etapa 15: Retrieval com top_k
    candidatos = retrieve_documents(pergunta, top_k=request.top_k)
    
    # Etapas 16, 17 e 18: Construção do prompt e chamada do LLM
    resultado_llm = ask_llm(pergunta, candidatos)
    
    return {
        "pergunta": pergunta,
        "candidatos_recuperados": candidatos, # Para a interface apresentar
        "prompt_utilizado": resultado_llm["prompt_enviado"], # Para a interface apresentar de forma didática
        "resposta_llm": resultado_llm["resposta"]
    }

