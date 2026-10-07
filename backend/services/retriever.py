from backend.services.supabase_client import get_supabase_client
from backend.services.embedder import get_embedding_model

def retrieve_documents(query: str, top_k: int = 5, match_threshold: float = 0.5) -> list[dict]:
    """
    Realiza a busca vetorial no Supabase (Etapa 15).
    Retorna os candidatos recuperados.
    """
    # 1. Gera o embedding da pergunta
    model = get_embedding_model()
    # O fastembed retorna um gerador, pegamos o primeiro item (e único) e convertemos para lista
    query_embedding = list(model.embed([query]))[0].tolist()
    
    supabase = get_supabase_client()
    
    # 2. Chama a função RPC `match_document_chunks` configurada no Supabase
    response = supabase.rpc(
        "match_document_chunks",
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": top_k
        }
    ).execute()
    
    # A resposta é uma lista de dicionários com id, documento_id, numero_nota, posicao_chunk, conteudo_textual, similarity
    candidatos = response.data if response.data else []
    return candidatos
