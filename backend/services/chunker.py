def chunk_document(structured_data: dict) -> list[dict]:
    """
    Realiza o chunking dos dados estruturados da nota fiscal (Etapa 7).
    """
    chunks = []
    doc_id = structured_data["documento_id"]
    numero_nota = structured_data["numero_nota"]
    
    # Chunk 1: Cabeçalho e Informações Gerais
    header_text = (
        f"Nota Fiscal: {numero_nota}. "
        f"Data: {structured_data['data_emissao']}. "
        f"Fornecedor: {structured_data['fornecedor']} (CNPJ: {structured_data['cnpj']}). "
        f"Cliente: {structured_data['cliente']}. "
        f"Valor Total: R$ {structured_data['valor_total']}."
    )
    chunks.append({
        "documento_id": doc_id,
        "numero_nota": numero_nota,
        "posicao_chunk": 0,
        "conteudo_textual": header_text
    })
    
    # Chunks de Produtos (um chunk para cada linha de produto)
    for i, produto_str in enumerate(structured_data["produtos"], start=1):
        produto_text = f"Produto na Nota Fiscal {numero_nota}: {produto_str.replace('- ', '')}"
        chunks.append({
            "documento_id": doc_id,
            "numero_nota": numero_nota,
            "posicao_chunk": i,
            "conteudo_textual": produto_text
        })
        
    return chunks

if __name__ == "__main__":
    # Teste isolado do chunking
    exemplo = {
        "documento_id": "nf_teste.pdf",
        "numero_nota": "9999",
        "data_emissao": "01/01/2026",
        "fornecedor": "Fornecedor Teste",
        "cnpj": "00.000.000/0000-00",
        "cliente": "Cliente Teste",
        "valor_total": 1000.0,
        "produtos": ["- 1x Item A - R$ 500.0", "- 1x Item B - R$ 500.0"]
    }
    
    chunks_resultado = chunk_document(exemplo)
    for c in chunks_resultado:
        print(f"[{c['posicao_chunk']}] Doc: {c['documento_id']} | Conteúdo: {c['conteudo_textual']}")
