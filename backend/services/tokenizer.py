import tiktoken

def get_tokenizer():
    """Retorna a instância do tokenizador para ser utilizada."""
    return tiktoken.get_encoding("cl100k_base")

def tokenize_chunk(chunk: dict, tokenizer) -> dict:
    """
    Realiza a tokenização explícita de um chunk e calcula a quantidade de tokens (Etapa 8).
    O chunk atualizado inclui a lista de tokens numéricos e a contagem.
    """
    text = chunk["conteudo_textual"]
    tokens = tokenizer.encode(text)
    
    chunk["tokens"] = tokens
    chunk["quantidade_tokens"] = len(tokens)
    
    return chunk

def tokenize_all_chunks(chunks: list[dict]) -> list[dict]:
    """Tokeniza uma lista de chunks."""
    tokenizer = get_tokenizer()
    for chunk in chunks:
        tokenize_chunk(chunk, tokenizer)
    return chunks

if __name__ == "__main__":
    # Teste de tokenização
    exemplo_chunk = {
        "documento_id": "nf_1001.pdf",
        "numero_nota": "1001",
        "posicao_chunk": 0,
        "conteudo_textual": "Nota Fiscal: 1001. Data: 10/10/2026. Fornecedor: Tech Hardware Brasil Ltda."
    }
    
    resultado = tokenize_chunk(exemplo_chunk, get_tokenizer())
    print(f"Texto original: {resultado['conteudo_textual']}")
    print(f"Total de Tokens: {resultado['quantidade_tokens']}")
    print(f"Lista de Tokens: {resultado['tokens']}")
