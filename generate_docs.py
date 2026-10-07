from fpdf import FPDF
import os

def create_invoice(filename, numero, data, fornecedor, cnpj, cliente, produtos, valor_total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    pdf.cell(200, 10, txt=f"NOTA FISCAL Nº {numero}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data de Emissão: {data}", ln=True)
    pdf.cell(200, 10, txt=f"Fornecedor: {fornecedor}", ln=True)
    pdf.cell(200, 10, txt=f"CNPJ: {cnpj}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt="="*50, ln=True)
    
    pdf.cell(200, 10, txt="PRODUTOS:", ln=True)
    for prod in produtos:
        pdf.cell(200, 10, txt=f"- {prod['quantidade']}x {prod['nome']} - R$ {prod['valor_unitario']:.2f} (Total: R$ {prod['quantidade'] * prod['valor_unitario']:.2f})", ln=True)
    
    pdf.cell(200, 10, txt="="*50, ln=True)
    pdf.cell(200, 10, txt=f"VALOR TOTAL: R$ {valor_total:.2f}", ln=True)

    pdf.output(filename)

# Dados fictícios para as 4 notas fiscais
notas = [
    {
        "filename": "docs/nf_1001.pdf",
        "numero": "1001",
        "data": "10/10/2026",
        "fornecedor": "Tech Hardware Brasil Ltda",
        "cnpj": "12.345.678/0001-99",
        "cliente": "Teophilo RAG Solutions",
        "produtos": [
            {"nome": "Notebook Dell XPS", "quantidade": 2, "valor_unitario": 8500.00},
            {"nome": "Mouse Sem Fio Logitech", "quantidade": 5, "valor_unitario": 150.00}
        ],
        "valor_total": 17750.00
    },
    {
        "filename": "docs/nf_1002.pdf",
        "numero": "1002",
        "data": "12/10/2026",
        "fornecedor": "Cloud Services Corp",
        "cnpj": "98.765.432/0001-11",
        "cliente": "Teophilo RAG Solutions",
        "produtos": [
            {"nome": "Servidor Dedicado (Mensalidade)", "quantidade": 1, "valor_unitario": 1200.00},
            {"nome": "Banco de Dados Supabase (Tier Pro)", "quantidade": 1, "valor_unitario": 350.00}
        ],
        "valor_total": 1550.00
    },
    {
        "filename": "docs/nf_1003.pdf",
        "numero": "1003",
        "data": "15/10/2026",
        "fornecedor": "Office Supply Co.",
        "cnpj": "11.222.333/0001-44",
        "cliente": "Teophilo RAG Solutions",
        "produtos": [
            {"nome": "Cadeira de Escritório Ergonomica", "quantidade": 4, "valor_unitario": 900.00},
            {"nome": "Mesa de Trabalho", "quantidade": 2, "valor_unitario": 1100.00}
        ],
        "valor_total": 5800.00
    },
    {
        "filename": "docs/nf_1004.pdf",
        "numero": "1004",
        "data": "18/10/2026",
        "fornecedor": "Software House Inc",
        "cnpj": "44.555.666/0001-77",
        "cliente": "Teophilo RAG Solutions",
        "produtos": [
            {"nome": "Licença Software OCR", "quantidade": 1, "valor_unitario": 2500.00},
            {"nome": "Suporte Técnico 24/7", "quantidade": 1, "valor_unitario": 500.00}
        ],
        "valor_total": 3000.00
    }
]

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    for nota in notas:
        create_invoice(**nota)
        print(f"Criado: {nota['filename']}")
