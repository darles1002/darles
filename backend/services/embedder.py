from fastembed import TextEmbedding

# Modelo padrão do fastembed (leve e eficiente para a maioria dos casos de RAG)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
_embedding_model = None

def get_embedding_model():
    """Retorna uma instância única do modelo (Singleton)."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)
    return _embedding_model

def get_embedding_dimension() -> int:
    """Retorna a dimensão do vetor para ajudar a criar a tabela no PGVector (Etapa 10)."""
    # Para o modelo BAAI/bge-small-en-v1.5, a dimensão é 384
    return 384

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Gera o embedding vetorial para o conteúdo textual de cada chunk (Etapa 9).
    O vetor será anexado ao chunk.
    """
    if not chunks:
        return chunks
        
    model = get_embedding_model()
    
    # Extrai apenas os textos
    textos = [chunk["conteudo_textual"] for chunk in chunks]
    
    # Gera os embeddings em batch (retorna um gerador iterável de numpy arrays)
    embeddings_gerador = model.embed(textos)
    
    # Anexa ao dicionário, convertendo numpy array para lista de floats para serialização e persistência
    for chunk, vetor_np in zip(chunks, embeddings_gerador):
        chunk["embedding"] = vetor_np.tolist()
        
    return chunks

if __name__ == "__main__":
    # Teste de Embedding
    exemplo_chunks = [
        {"conteudo_textual": "Nota Fiscal: 1001. Data: 10/10/2026. Fornecedor: Tech Hardware Brasil Ltda."},
        {"conteudo_textual": "Produto: Notebook Dell XPS"}
    ]
    
    print(f"Dimensão esperada: {get_embedding_dimension()}")
    resultados = embed_chunks(exemplo_chunks)
    
    for i, c in enumerate(resultados):
        vetor = c["embedding"]
        print(f"Chunk {i} Vetor gerado de tamanho: {len(vetor)}")
        print(f"Primeiros 5 valores: {vetor[:5]}")
