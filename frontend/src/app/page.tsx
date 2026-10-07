"use client";

import { useState, useRef, useEffect } from "react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"ingestao" | "consulta">("consulta");
  const [selectedBase, setSelectedBase] = useState<"documentos" | "vazio">("documentos");
  
  // Estados para Consulta
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [isQuerying, setIsQuerying] = useState(false);
  const [pipelineState, setPipelineState] = useState<any>(null);
  
  // Estados para Ingestão
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestResults, setIngestResults] = useState<any>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleIngest = async () => {
    setIsIngesting(true);
    setIngestResults(null);
    try {
      const res = await fetch("http://localhost:8000/api/ingest", {
        method: "POST"
      });
      const data = await res.json();
      setIngestResults(data);
    } catch (err) {
      setIngestResults({ error: "Erro de conexão com o backend." });
    } finally {
      setIsIngesting(false);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMsg = query;
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setQuery("");
    setIsQuerying(true);
    setPipelineState({ status: "processing", step: "tokenization" });

    try {
      // Simulação rápida para didática no pipeline
      setTimeout(() => setPipelineState({ status: "processing", step: "embedding" }), 500);
      setTimeout(() => setPipelineState({ status: "processing", step: "retrieval" }), 1000);
      setTimeout(() => setPipelineState({ status: "processing", step: "llm" }), 1500);

      const res = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          pergunta: userMsg, 
          top_k: 5,
          // Num projeto real, poderiamos passar a base selecionada aqui caso houvesse multiplas bases
          // base: selectedBase
        })
      });
      
      const data = await res.json();
      
      if(selectedBase === "vazio") {
         // Simulação didática de base vazia, ignorando o retorno
         setMessages(prev => [...prev, { role: "system", content: "Sem dados disponiveis na base" }]);
         setPipelineState({ 
           status: "success", 
           data: { 
             candidatos_recuperados: [],
             prompt_utilizado: ""
           } 
         });
      } else {
         setMessages(prev => [...prev, { role: "system", content: data.resposta_llm }]);
         setPipelineState({ status: "success", data });
      }

    } catch (err) {
      setMessages(prev => [...prev, { role: "system", content: "Ocorreu um erro na consulta ao backend." }]);
      setPipelineState({ status: "error" });
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <>
      <header className="header">
        <div className="logo" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Ícone profissional moderno (Database/Brain Vector) */}
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2400/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="var(--accent-color)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="var(--accent-color)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="var(--accent-color)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <div><span className="logo-highlight">RAD</span> Darles</div>
        </div>
        <div className="tabs">
          <button 
            className={`tab-btn ${activeTab === 'ingestao' ? 'active' : ''}`}
            onClick={() => setActiveTab('ingestao')}
          >
            Ingestão
          </button>
          <button 
            className={`tab-btn ${activeTab === 'consulta' ? 'active' : ''}`}
            onClick={() => setActiveTab('consulta')}
          >
            Consulta RAG
          </button>
        </div>
        <div>
          <select 
            className="select-input"
            value={selectedBase}
            onChange={(e) => setSelectedBase(e.target.value as any)}
          >
            <option value="documentos">Base: Notas Fiscais (Default)</option>
            <option value="vazio">Base: Vazia (Teste Ausência)</option>
          </select>
        </div>
      </header>

      <main className="main-container">
        
        {/* Lado Esquerdo - Interface Principal */}
        <section className="card chat-container">
          {activeTab === "consulta" ? (
            <>
              <div className="card-title">Chatbot RAG</div>
              <div className="chat-messages">
                {messages.length === 0 && (
                  <div className="message system" style={{opacity: 0.7}}>
                    Olá! Sou o assistente RAG + Teophilo. Como posso ajudar com a base de Notas Fiscais?
                  </div>
                )}
                {messages.map((msg, idx) => (
                  <div key={idx} className={`message ${msg.role}`}>
                    {msg.content}
                  </div>
                ))}
                {isQuerying && (
                  <div className="message system">
                    <div className="loader"></div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <form className="chat-input-wrapper" onSubmit={handleQuery}>
                <input 
                  type="text" 
                  className="chat-input" 
                  placeholder="Pergunte algo sobre os documentos..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={isQuerying}
                />
                <button type="submit" className="btn" disabled={isQuerying || !query.trim()}>
                  Enviar
                </button>
              </form>
            </>
          ) : (
            <>
              <div className="card-title">Pipeline de Ingestão (ETAPA 11)</div>
              <div style={{color: "var(--text-secondary)", marginBottom: "1rem"}}>
                Clique abaixo para disparar a ingestão dos 4 PDFs fictícios criados na pasta docs.
              </div>
              <button className="btn" onClick={handleIngest} disabled={isIngesting}>
                {isIngesting ? "Processando..." : "Iniciar Ingestão"}
              </button>
              
              {ingestResults && (
                <div style={{marginTop: "2rem"}}>
                  <h4>Resultado do Processamento:</h4>
                  <pre>
                    {JSON.stringify(ingestResults, null, 2)}
                  </pre>
                </div>
              )}
            </>
          )}
        </section>

        {/* Lado Direito - Observabilidade Didática */}
        <aside className="card pipeline-container">
          <div className="card-title">Observabilidade RAG</div>
          
          {activeTab === "consulta" && (
            <>
              <div className={`pipeline-step ${pipelineState?.step === 'tokenization' ? 'active' : ''} ${pipelineState?.status === 'success' ? 'success' : ''}`}>
                <div className="step-title">1. Tokenização da Pergunta</div>
                <div className="step-content">
                  A pergunta é convertida em tokens numéricos para ser processada pelo modelo BAAI/bge-small-en-v1.5.
                </div>
              </div>

              <div className={`pipeline-step ${pipelineState?.step === 'embedding' ? 'active' : ''} ${pipelineState?.status === 'success' ? 'success' : ''}`}>
                <div className="step-title">2. Geração de Embedding</div>
                <div className="step-content">
                  Um vetor de 384 dimensões é criado representando o sentido semântico da pergunta.
                </div>
              </div>

              <div className={`pipeline-step ${pipelineState?.step === 'retrieval' ? 'active' : ''} ${pipelineState?.status === 'success' ? 'success' : ''}`}>
                <div className="step-title">3. Retrieval (Busca Vetorial)</div>
                <div className="step-content">
                  Buscando top_k=5 no Supabase (PGVector).
                  
                  {pipelineState?.data?.candidatos_recuperados && (
                    <div style={{marginTop: "0.5rem"}}>
                      <strong>Documentos Encontrados:</strong>
                      {pipelineState.data.candidatos_recuperados.length === 0 ? (
                        <div>0 candidatos relevantes.</div>
                      ) : (
                        <ul style={{paddingLeft: "1.2rem", marginTop: "0.2rem"}}>
                          {pipelineState.data.candidatos_recuperados.map((c: any, i: number) => (
                            <li key={i} style={{marginBottom: "0.25rem"}}>
                              {c.documento_id} (Chunk {c.posicao_chunk})
                              <span className="score-badge">{(c.similarity * 100).toFixed(1)}%</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  )}
                </div>
              </div>

              <div className={`pipeline-step ${pipelineState?.step === 'llm' ? 'active' : ''} ${pipelineState?.status === 'success' ? 'success' : ''}`}>
                <div className="step-title">4. Prompt Aumentado & LLM</div>
                <div className="step-content">
                  O contexto recuperado é unido à pergunta e enviado para o OpenRouter.
                  
                  {pipelineState?.data?.prompt_utilizado && (
                    <details style={{marginTop: "0.5rem", cursor: "pointer"}}>
                      <summary>Ver Prompt Enviado</summary>
                      <pre>{pipelineState.data.prompt_utilizado}</pre>
                    </details>
                  )}
                </div>
              </div>
            </>
          )}

          {activeTab === "ingestao" && (
            <>
               <div className="pipeline-step success">
                <div className="step-title">1. Extração / OCR</div>
                <div className="step-content">PyMuPDF lê os PDFs e extrai o conteúdo.</div>
              </div>
               <div className="pipeline-step success">
                <div className="step-title">2. Estruturação</div>
                <div className="step-content">RegEx organiza os dados em tabelas (Nota, Fornecedor, Itens).</div>
              </div>
               <div className="pipeline-step success">
                <div className="step-title">3. Chunking</div>
                <div className="step-content">Dividindo as informações estruturadas mantendo metadados (posição, doc_id).</div>
              </div>
               <div className="pipeline-step success">
                <div className="step-title">4. Tokenização e Embeddings</div>
                <div className="step-content">FastEmbed gera vetores de 384 dimensões e tiktoken conta o tamanho do chunk.</div>
              </div>
               <div className="pipeline-step success">
                <div className="step-title">5. Armazenamento</div>
                <div className="step-content">Chunks salvos na tabela `document_chunks` no Supabase com PGVector HNSW.</div>
              </div>
            </>
          )}

        </aside>
      </main>
    </>
  );
}
