import pymupdf  # PyMuPDF
import re

def extract_text_from_pdf(filepath: str) -> str:
    """Extrai todo o texto de um arquivo PDF."""
    doc = pymupdf.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_invoice_text(text: str, doc_id: str) -> dict:
    """
    Analisa o texto extraído da Nota Fiscal e estrutura os dados (Etapa 6).
    """
    data = {
        "documento_id": doc_id,
        "numero_nota": None,
        "data_emissao": None,
        "fornecedor": None,
        "cnpj": None,
        "cliente": None,
        "produtos": [],
        "valor_total": None,
        "texto_extraido": text
    }

    # Extração via RegEx simplificada (baseada no formato gerado no Etapa 4)
    match_numero = re.search(r"NOTA FISCAL N[ºo]\s+(\d+)", text)
    if match_numero:
        data["numero_nota"] = match_numero.group(1)

    match_data = re.search(r"Data de Emissão:\s+([0-9/]+)", text)
    if match_data:
        data["data_emissao"] = match_data.group(1)

    match_fornecedor = re.search(r"Fornecedor:\s+(.+)", text)
    if match_fornecedor:
        data["fornecedor"] = match_fornecedor.group(1).strip()

    match_cnpj = re.search(r"CNPJ:\s+([0-9.\-/]+)", text)
    if match_cnpj:
        data["cnpj"] = match_cnpj.group(1)

    match_cliente = re.search(r"Cliente:\s+(.+)", text)
    if match_cliente:
        data["cliente"] = match_cliente.group(1).strip()

    match_total = re.search(r"VALOR TOTAL: R\$ ([\d.]+)", text)
    if match_total:
        data["valor_total"] = float(match_total.group(1))

    # Extração de produtos (linhas que começam com "- ")
    linhas = text.split('\n')
    for linha in linhas:
        if linha.startswith("- "):
            # Ex: "- 2x Notebook Dell XPS - R$ 8500.00 (Total: R$ 17000.00)"
            data["produtos"].append(linha.strip())
            
    return data

def process_documents(directory: str) -> list[dict]:
    """Processa todos os PDFs em um diretório e retorna os dados estruturados."""
    import os
    results = []
    if not os.path.exists(directory):
        return results
        
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            text = extract_text_from_pdf(filepath)
            structured_data = parse_invoice_text(text, doc_id=filename)
            results.append(structured_data)
            
    return results

if __name__ == "__main__":
    # Teste local simples
    import os
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs"))
    documentos_estruturados = process_documents(docs_path)
    for doc in documentos_estruturados:
        print(f"--- Documento Processado: {doc['documento_id']} ---")
        print(f"Nota: {doc['numero_nota']}")
        print(f"Fornecedor: {doc['fornecedor']}")
        print(f"Produtos encontrados: {len(doc['produtos'])}")
        print(f"Valor Total: R$ {doc['valor_total']}")
        print("-" * 30)
