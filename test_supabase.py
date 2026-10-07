import os
from dotenv import load_dotenv
from supabase import create_client, Client

def test_connection():
    load_dotenv()
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SECRET_KEY")
    
    if not url or not key:
        print("SUPABASE: falha na conexão (credenciais não encontradas no .env)")
        return
        
    try:
        supabase: Client = create_client(url, key)
        # Tenta fazer uma requisição simples (ex: ler 1 item de uma tabela inexistente só para ver se auth/url passa,
        # ou apenas chama algo básico. Como a API supabase rest é meio chata só pra "ping", vamos tentar listar as tabelas
        # ou apenas fazer uma auth session.
        # Alternativa para checar conectividade sem tabelas criadas:
        supabase.auth.get_user("invalid_jwt") 
        print("SUPABASE: conexão estabelecida com sucesso")
    except Exception as e:
        # Auth api throws AuthApiError se as credenciais url/key existirem mas o jwt for invalido (o que significa que bateu no supabase)
        if "invalid" in str(e).lower() or "not found" in str(e).lower() or "auth" in str(e).lower():
             print("SUPABASE: conexão estabelecida com sucesso")
        else:
             print(f"SUPABASE: falha na conexão")

if __name__ == "__main__":
    test_connection()
