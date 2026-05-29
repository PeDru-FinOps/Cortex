# Agente IA do Cortex

## Visao geral

A agente transforma as notas Markdown em um fluxo RAG:

1. Le as notas do diretorio configurado em `NOTES_ROOT`.
2. Divide cada nota em chunks.
3. Cria um indice local em memoria.
4. Recupera os chunks mais relevantes para a pergunta.
5. Detecta padroes, relacoes implicitas, hipoteses e proximas perguntas.
6. Envia pergunta + contexto recuperado para a LLM, se `OPENAI_API_KEY` estiver configurada.

## Configuracao com OpenAI

No arquivo `.env`, configure:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_MODEL=gpt-5.2
OPENAI_MAX_OUTPUT_TOKENS=1200
CORTEX_VECTOR_STORE=openai
OPENAI_VECTOR_STORE_ID=vs_seu_vector_store
OPENAI_VECTOR_MAX_RESULTS=8
```

Instale as dependencias:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Reinicie o app:

```powershell
.\.venv\Scripts\python app.py
```

A aba **Chat IA** fica disponivel quando uma nota esta aberta em modo leitura.

## Comportamento sem chave

Se `OPENAI_API_KEY` nao estiver configurada, a agente continua funcionando em modo local. Nesse modo ela nao chama uma LLM externa; ela retorna sintese, hipoteses e contexto usando o indice TF-IDF local.

## Vector Store atual

O Cortex suporta dois modos de recuperacao:

### `CORTEX_VECTOR_STORE=tfidf`

Este e o fallback local:

- Tipo: indice local em memoria.
- Tecnica: TF-IDF simples.
- Similaridade: cosseno.
- Persistencia: nenhuma.
- Arquivos indexados: Markdown em `NOTES_ROOT`.
- Reindexacao: feita quando a agente e instanciada para responder.

Isso e suficiente para uma primeira etapa, mas nao substitui embeddings semanticos quando o acervo crescer.

### `CORTEX_VECTOR_STORE=openai`

Neste modo, o Cortex usa o OpenAI Vector Store informado em:

```env
OPENAI_VECTOR_STORE_ID=vs_seu_vector_store
```

O fluxo passa a ser:

1. `CortexAgent.search` chama `client.vector_stores.search(...)`.
2. Os resultados viram o bloco **Contexto recuperado** na UI.
3. `CortexAgent.chat` chama `client.responses.create(...)`.
4. A chamada da LLM inclui o tool `file_search` com o mesmo `OPENAI_VECTOR_STORE_ID`.

O Vector Store precisa existir previamente na OpenAI e conter os arquivos indexados.

## Sincronizacao pelo botao Sync

A sidebar possui um botao **Sync** que chama:

```http
POST /api/vector-store/sync
```

Esse endpoint executa `sync_notes_to_openai(repository)`.

O processo:

1. Le todas as notas `.md` em `NOTES_ROOT`.
2. Calcula SHA-256 de cada arquivo.
3. Compara com o manifesto local em `.cortex_sync/`.
4. Envia arquivos novos para a OpenAI Files API.
5. Anexa cada arquivo ao Vector Store via Vector Store Files API.
6. Reenvia arquivos alterados.
7. Remove do Vector Store arquivos que sumiram localmente.

O manifesto local guarda `path`, `sha256`, `file_id` e `vector_store_file_id`. Ele e ignorado pelo Git porque representa estado operacional da sua maquina.

Requisitos:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_VECTOR_STORE_ID=vs_seu_vector_store
```

O Sync nao cria o Vector Store. Ele apenas sincroniza as notas para um Vector Store existente.

Arquivos enviados usam:

```env
OPENAI_FILE_PURPOSE=assistants
```

Se essa variavel nao for definida, `assistants` e usado como padrao.

## Aba Inteligencia

A aba **Inteligencia** concentra duas capacidades:

### Conexoes sugeridas

O agente compara notas relacionadas e sugere conexoes implicitas. Cada recomendacao inclui:

- nota de origem;
- nota de destino;
- motivo da recomendacao;
- score de afinidade;
- confianca estimada;
- link wiki sugerido, como `[[Nome da nota]]`.

Essas sugestoes ainda nao editam os arquivos automaticamente. Elas funcionam como uma fila de curadoria para o usuario decidir quais links devem virar conexoes reais.

Cada sugestao pode ser aprovada pelo botao **Aprovar**. A aprovacao adiciona um wiki-link na nota de origem, dentro da secao:

```markdown
## Conexoes aprovadas

- [[Nome da nota]]
```

Se o link ja existir, o Cortex nao duplica.

Cada sugestao tambem pode ser rejeitada pelo botao **Rejeitar**. Rejeicoes sao salvas em `.cortex_intelligence/rejected_connections.json`, ignorado pelo Git, e a mesma conexao deixa de aparecer nas proximas cargas.

O ranking local usa similaridade de conteudo e conceitos compartilhados como sinais principais. Tags ainda entram como sinal secundario. Quando `OPENAI_API_KEY` esta configurada, a LLM revisa os candidatos e deve aprovar apenas conexoes com relacao conceitual, dependencia operacional, causa e efeito, contraste ou oportunidade real de sintese.

### Escrita com skills

Os botoes de escrita usam skills salvas no proprio Cortex:

- **LinkedIn post** usa `IA/Skills/linkedin_posts_skill.md`.
- **Artigo** usa `IA/Skills/newsletter_skill.md` e `IA/Skills/seo_skill.md`.
- **Solicitado** usa as skills de artigo/SEO como base e respeita o tema informado pelo usuario.

O conteudo e gerado com:

1. tema escolhido pelo usuario ou nota atual;
2. contexto recuperado pelo RAG;
3. skill de escrita como regra de estilo e estrutura;
4. LLM da OpenAI quando `OPENAI_API_KEY` esta configurada;
5. fallback local quando a LLM nao esta disponivel.

## Como trocar o Vector Store futuramente

Mantenha a fronteira de responsabilidades:

- `split_markdown(content)`: chunking.
- `CortexAgent.search(query, focus_path, limit)`: recuperacao.
- `CortexAgent.chat(message, focus_path)`: orquestracao com LLM.
- `build_llm_prompt(message, base)`: montagem do contexto para a LLM.

O proximo passo recomendado e criar uma interface:

```python
class VectorIndex:
    def search(self, query: str, focus_path: str = "", limit: int = 8) -> list[dict]:
        ...
```

Depois, mover os modos atuais para adaptadores:

```python
class TfIdfVectorIndex(VectorIndex):
    ...

class OpenAIVectorStoreIndex(VectorIndex):
    ...
```

E adicionar outros adaptadores alternativos:

- `ChromaVectorIndex`: usa Chroma local.
- `FaissVectorIndex`: usa FAISS local.
- `QdrantVectorIndex`, `PineconeVectorIndex` ou `WeaviateVectorIndex`: usam servicos externos.

## Variaveis sugeridas para troca

```env
CORTEX_VECTOR_STORE=openai
OPENAI_VECTOR_STORE_ID=vs_seu_vector_store
CORTEX_EMBEDDING_MODEL=text-embedding-3-large
CORTEX_VECTOR_COLLECTION=cortex-notes
```

Valores possiveis para `CORTEX_VECTOR_STORE` no futuro:

- `tfidf`
- `openai`
- `chroma`
- `faiss`
- `qdrant`
- `pinecone`

## Referencias oficiais OpenAI

- Quickstart: https://platform.openai.com/docs/quickstart?api-mode=responses&lang=python
- Responses API: https://platform.openai.com/docs/api-reference/responses/create?api-mode=responses
