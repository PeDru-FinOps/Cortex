# Cortex

Repositorio local de notas Markdown correlacionadas por pastas e hashtags.

## Funcionalidades

- Login com usuario e senha definidos no `.env`
- Diretorio de pastas, subpastas e arquivos `.md`
- Criacao, leitura e alteracao de notas Markdown
- Pre-visualizacao em HTML
- Grafo gerado a partir de diretorios e hashtags
- Chat IA com RAG sobre as notas do Cortex

## Como rodar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Depois acesse `http://127.0.0.1:5000`.

Edite o arquivo `.env` antes de usar em um ambiente real.

## Configuracao da IA

Adicione sua chave no `.env`:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_MODEL=gpt-5.2
OPENAI_MAX_OUTPUT_TOKENS=1200
OPENAI_WRITING_MAX_OUTPUT_TOKENS=2400
CORTEX_VECTOR_STORE=openai
OPENAI_VECTOR_STORE_ID=vs_seu_vector_store
OPENAI_VECTOR_MAX_RESULTS=8
CORTEX_ALLOW_LIVE_VECTOR_SEARCH=0
```

Depois reinicie o Flask. A aba **Chat IA** aparece na tela de leitura de uma nota. Ela recupera contexto das notas, envia esse contexto para a OpenAI quando a chave existe e usa um fallback local quando a chave ou o SDK nao estao disponiveis.

### Variaveis do `.env`

| Variavel | Uso |
| --- | --- |
| `APP_USER` | Usuario de login da aplicacao. |
| `APP_PASSWORD` | Senha de login da aplicacao. |
| `SECRET_KEY` | Chave interna do Flask para sessao. Troque em producao. |
| `NOTES_ROOT` | Pasta local onde ficam as notas Markdown. Padrao: `notes`. |
| `OPENAI_API_KEY` | Chave da OpenAI usada para chat, escrita, sync e leitura do Vector Store. |
| `OPENAI_MODEL` | Modelo usado para respostas e escrita. |
| `OPENAI_MAX_OUTPUT_TOKENS` | Limite de saida para o Chat IA. |
| `OPENAI_WRITING_MAX_OUTPUT_TOKENS` | Limite de saida para textos gerados na aba Inteligencia. |
| `CORTEX_VECTOR_STORE` | `tfidf` usa busca local; `openai` usa cache/Vector Store OpenAI. |
| `OPENAI_VECTOR_STORE_ID` | ID do Vector Store da OpenAI, por exemplo `vs_...`. |
| `OPENAI_VECTOR_MAX_RESULTS` | Quantidade maxima de resultados em busca viva do Vector Store, quando habilitada. |
| `CORTEX_ALLOW_LIVE_VECTOR_SEARCH` | `0` evita busca viva paga e usa cache/local. `1` permite consultar o Vector Store em tempo real. |
| `OPENAI_FILE_PURPOSE` | Purpose usado no upload dos arquivos. Padrao: `assistants`. |

## RAG e Vector Store

O Cortex suporta dois modos:

- `CORTEX_VECTOR_STORE=tfidf`: indice local, em memoria, baseado em TF-IDF e similaridade por cosseno sobre chunks de Markdown.
- `CORTEX_VECTOR_STORE=openai`: usa o OpenAI Vector Store indicado em `OPENAI_VECTOR_STORE_ID`, preferindo o cache local em `.cortex_vector_cache/`.

No modo OpenAI, a aplicacao foi configurada para economizar chamadas pagas:

- A escrita e o Chat IA procuram primeiro no cache local do Vector Store.
- Se o cache existe e tem texto utilizavel, clicar em **Ler Vector** reutiliza o cache e nao relê remotamente.
- A busca viva no Vector Store fica desligada por padrao com `CORTEX_ALLOW_LIVE_VECTOR_SEARCH=0`.
- A chamada final para a LLM ainda custa tokens do modelo, mas nao usa `file_search` automaticamente.

Use `CORTEX_ALLOW_LIVE_VECTOR_SEARCH=1` apenas quando quiser permitir consultas em tempo real ao Vector Store. Isso pode gerar custos adicionais de File Search/busca.

### Sincronizar notas

Use o botao **Sync** na sidebar para enviar as notas locais ao OpenAI Vector Store configurado em `OPENAI_VECTOR_STORE_ID`.

O Sync:

- envia notas novas;
- reenvia notas alteradas;
- remove do Vector Store arquivos que foram apagados localmente;
- guarda um manifesto local em `.cortex_sync/`, ignorado pelo Git.

O Sync nao cria o Vector Store automaticamente. Crie o Vector Store na OpenAI, coloque o ID no `.env` e depois clique em **Sync**.

### Ler Vector e cache

Use o botao **Ler Vector** na aba **Inteligencia** para montar o cache local a partir do Vector Store. Esse cache fica em:

```text
.cortex_vector_cache/openai_vector_store.json
```

Esse diretorio e ignorado pelo Git. Depois que o cache aparece como utilizavel, novas geracoes de texto reaproveitam esse arquivo e nao precisam reler o Vector Store.

Fluxo recomendado para economizar:

1. Configure `OPENAI_VECTOR_STORE_ID`.
2. Clique em **Sync** quando alterar notas locais e quiser enviar mudancas para a OpenAI.
3. Clique em **Ler Vector** somente depois de um Sync relevante ou quando quiser atualizar o cache.
4. Gere textos normalmente. A escrita usara o cache.

Se o cache estiver ausente, vazio ou inutilizavel, a escrita cai para um briefing local rapido a partir das notas. A interface mostra essa situacao no painel de progresso.

## Aba Inteligencia

A aba **Inteligencia** sugere conexoes implicitas entre notas e gera textos usando as skills de escrita salvas no Cortex.

As conexoes sugeridas podem ser aprovadas ou rejeitadas. Ao aprovar, o Cortex adiciona um wiki-link na nota de origem, dentro da secao `## Conexoes aprovadas`. Rejeicoes ficam em `.cortex_intelligence/`, ignorado pelo Git, e deixam de aparecer nas proximas sugestoes. O ranking usa similaridade de conteudo/conceitos como sinal principal; tags sao apenas sinal secundario. Com OpenAI configurada, a LLM revisa os candidatos antes de exibir.

Opcoes de escrita:

- **LinkedIn post**: usa `IA/Skills/linkedin_posts_skill.md`.
- **Artigo**: usa `IA/Skills/newsletter_skill.md` e `IA/Skills/seo_skill.md`.
- **Solicitado**: voce informa um tema e a IA gera um texto com base no Cortex.

Para trocar futuramente por outro Vector Store, mantenha a mesma fronteira de codigo em `cortex_notes/agent.py`:

- `split_markdown`: prepara chunks.
- `CortexAgent.search`: recupera os chunks relevantes.
- `CortexAgent.chat`: envia pergunta + contexto para a LLM.

O caminho recomendado e extrair uma interface de recuperacao, por exemplo `VectorIndex.search(query, focus_path, limit)`, e implementar adaptadores para:

- OpenAI Vector Stores/File Search
- Chroma ou FAISS local
- Pinecone, Qdrant ou Weaviate

Com isso, a UI e a chamada da LLM continuam iguais; apenas o mecanismo de recuperacao muda.
