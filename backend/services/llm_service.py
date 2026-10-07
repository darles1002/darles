import os
from openai import OpenAI
from backend.services.retriever import retrieve_documents
from backend.services.tokenizer import get_tokenizer

def build_augmented_prompt(question: str, context_chunks: list[dict]) -> str:
    """
    Constrói o prompt aumentado com o contexto recuperado (Etapa 17).
    """
    context_text = "\n\n".join([
        f"--- INÍCIO DO DOCUMENTO {c['documento_id']} (Chunk {c['posicao_chunk']}) ---\n"
        f"{c['conteudo_textual']}\n"
        f"--- FIM DO DOCUMENTO ---"
        for c in context_chunks
    ])
    
    prompt = f"""PERGUNTA DO USUÁRIO:
{question}

CONTEXTO RECUPERADO:
{context_text}

INSTRUÇÕES DO SISTEMA:
Você é um assistente virtual especializado em analisar Notas Fiscais.
Responda à pergunta do usuário baseando-se EXCLUSIVAMENTE no contexto fornecido acima.
Se a resposta não estiver contida no contexto, não invente informações.
Seja objetivo, claro e educado.
=====================
"""
    return prompt

def ask_llm(question: str, context_chunks: list[dict]) -> dict:
    """
    Comunica com o LLM via OpenRouter enviando o prompt aumentado (Etapa 18).
    """
    # Etapa 16: Regra de ausência de dados
    if not context_chunks:
        return {
            "resposta": "Sem dados disponiveis na base",
            "contexto_utilizado": [],
            "prompt_enviado": ""
        }
        
    prompt_aumentado = build_augmented_prompt(question, context_chunks)
    
    # Obtém a chave da API do .env de forma segura
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY não configurada no .env")
        
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # O modelo especificado em rag.txt é openrouter/auto
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {"role": "user", "content": prompt_aumentado}
        ],
        temperature=0.0
    )
    
    resposta_final = response.choices[0].message.content
    
    return {
        "resposta": resposta_final,
        "contexto_utilizado": context_chunks,
        "prompt_enviado": prompt_aumentado
    }
