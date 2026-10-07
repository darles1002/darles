from backend.api.endpoints import ingest_documents

if __name__ == "__main__":
    try:
        print("Iniciando pipeline de ingestão...")
        resultado = ingest_documents()
        print("Resultado:")
        print(resultado)
    except Exception as e:
        print(f"Erro durante a ingestão: {e}")
