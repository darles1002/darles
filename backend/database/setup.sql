-- Habilitar a extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabela para armazenar os documentos processados
CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    documento_id TEXT UNIQUE NOT NULL,
    numero_nota TEXT,
    data_emissao TEXT,
    fornecedor TEXT,
    cnpj TEXT,
    cliente TEXT,
    valor_total NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para armazenar os chunks e seus embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    documento_id TEXT REFERENCES documentos(documento_id) ON DELETE CASCADE,
    numero_nota TEXT,
    posicao_chunk INTEGER,
    conteudo_textual TEXT,
    quantidade_tokens INTEGER,
    -- Como usamos o BAAI/bge-small-en-v1.5, a dimensão é 384
    embedding vector(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice HNSW para busca vetorial rápida no PGVector
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- Função RPC para buscar documentos similares
CREATE OR REPLACE FUNCTION match_document_chunks (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id bigint,
  documento_id text,
  numero_nota text,
  posicao_chunk integer,
  conteudo_textual text,
  similarity float
)
LANGUAGE sql STABLE
AS $$
  SELECT
    id,
    documento_id,
    numero_nota,
    posicao_chunk,
    conteudo_textual,
    1 - (document_chunks.embedding <=> query_embedding) AS similarity
  FROM document_chunks
  WHERE 1 - (document_chunks.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
$$;
