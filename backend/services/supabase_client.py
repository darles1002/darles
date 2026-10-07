import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Garante que as variáveis sejam carregadas (pode estar na raiz do projeto)
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

_supabase = None

def get_supabase_client() -> Client:
    """Retorna o cliente Singleton do Supabase."""
    global _supabase
    if _supabase is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SECRET_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL e SUPABASE_SECRET_KEY não encontrados no .env")
        _supabase = create_client(url, key)
    return _supabase

def salvar_documento(dados_documento: dict):
    """Salva os metadados do documento na tabela `documentos`."""
    supabase = get_supabase_client()
    # Verifica se já existe
    response = supabase.table("documentos").select("id").eq("documento_id", dados_documento["documento_id"]).execute()
    if not response.data:
        # Se não existe, insere
        supabase.table("documentos").insert({
            "documento_id": dados_documento["documento_id"],
            "numero_nota": dados_documento["numero_nota"],
            "data_emissao": dados_documento["data_emissao"],
            "fornecedor": dados_documento["fornecedor"],
            "cnpj": dados_documento["cnpj"],
            "cliente": dados_documento["cliente"],
            "valor_total": dados_documento["valor_total"]
        }).execute()

def salvar_chunks(chunks: list[dict]):
    """Salva os chunks e seus embeddings na tabela `document_chunks`."""
    supabase = get_supabase_client()
    for chunk in chunks:
        # Verifica se o chunk já foi salvo para não duplicar (baseado em documento_id e posicao_chunk)
        resp = supabase.table("document_chunks").select("id").eq("documento_id", chunk["documento_id"]).eq("posicao_chunk", chunk["posicao_chunk"]).execute()
        if not resp.data:
            supabase.table("document_chunks").insert({
                "documento_id": chunk["documento_id"],
                "numero_nota": chunk["numero_nota"],
                "posicao_chunk": chunk["posicao_chunk"],
                "conteudo_textual": chunk["conteudo_textual"],
                "quantidade_tokens": chunk.get("quantidade_tokens", 0),
                "embedding": chunk["embedding"]
            }).execute()
