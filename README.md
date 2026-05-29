# Cortex

Cortex e um aplicativo local para manter notas Markdown, conectar ideias por tags e wiki-links, conversar com uma IA sobre sua base de conhecimento e gerar textos a partir do seu proprio conteudo.

Ele pode rodar apenas localmente com busca TF-IDF, ou integrado ao OpenAI Vector Store.

## Funcionalidades

- Login com usuario e senha definidos no `.env`
- Leitura, criacao e edicao de notas Markdown
- Upload de Markdown, imagens, pastas e subpastas
- Renderizacao de imagens e wiki-links
- Grafo de notas, tags e conexoes
- Chat IA com RAG sobre o Cortex
- Aba Inteligencia para sugerir conexoes e tags
- Aba Escrita para gerar, editar, aprovar e salvar textos em `Artigos/`
- Aprendizado privado de estilo via skill `revisor_pedro`

## Setup apos Git Clone

Requisitos:

- Python 3.11+
- Git
- Uma OpenAI API key, apenas se quiser usar LLM/Vector Store

Clone e instale:

```powershell
git clone <url-do-repositorio>
cd Cortex
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite o `.env` antes de iniciar.

Configuracao minima local:

```env
APP_USER=admin
APP_PASSWORD=troque-esta-senha
SECRET_KEY=gere-uma-chave-grande
NOTES_ROOT=notes
CORTEX_VECTOR_STORE=tfidf
CORTEX_PRIVATE_SKILLS_DIR=.cortex_private_skills
```

Rode:

```powershell
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

## Estrutura Local

Pastas importantes:

```text
notes/                    notas Markdown do Cortex
.cortex_private_skills/   skills privadas e sensiveis
.cortex_sync/             manifesto local de sync com OpenAI
.cortex_vector_cache/     cache local do Vector Store
.cortex_intelligence/     rejeicoes de conexoes sugeridas
```

As pastas `.cortex_*` ficam no `.gitignore` porque podem conter estado local, preferencias privadas ou dados sensiveis.

## Variaveis do `.env`

| Variavel | Uso |
| --- | --- |
| `APP_USER` | Usuario de login. |
| `APP_PASSWORD` | Senha de login. |
| `SECRET_KEY` | Chave interna do Flask. Troque em qualquer ambiente real. |
| `NOTES_ROOT` | Pasta das notas Markdown. Padrao: `notes`. |
| `OPENAI_API_KEY` | Chave da OpenAI para chat, escrita, sync e leitura do Vector Store. |
| `OPENAI_MODEL` | Modelo usado pela IA. |
| `OPENAI_MAX_OUTPUT_TOKENS` | Limite de saida do Chat IA. |
| `OPENAI_WRITING_MAX_OUTPUT_TOKENS` | Limite de saida da escrita. |
| `CORTEX_VECTOR_STORE` | `tfidf` para busca local; `openai` para usar Vector Store/cache. |
| `OPENAI_VECTOR_STORE_ID` | ID do Vector Store OpenAI, por exemplo `vs_...`. |
| `OPENAI_VECTOR_MAX_RESULTS` | Quantidade maxima de resultados em busca viva. |
| `CORTEX_ALLOW_LIVE_VECTOR_SEARCH` | `0` evita busca viva paga; `1` permite consulta remota em tempo real. |
| `CORTEX_PRIVATE_SKILLS_DIR` | Pasta privada para skills sensiveis. Padrao: `.cortex_private_skills`. |
| `OPENAI_FILE_PURPOSE` | Purpose usado no upload de arquivos. Padrao: `assistants`. |

## Modo Local Sem OpenAI

Para usar sem custos de API:

```env
CORTEX_VECTOR_STORE=tfidf
OPENAI_API_KEY=
OPENAI_VECTOR_STORE_ID=
```

Nesse modo, leitura, edicao, grafo, tags e busca local continuam funcionando. O Chat IA e a Escrita usam fallback local quando nao houver chave OpenAI.

## Configurar OpenAI

No `.env`:

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

Crie o Vector Store na OpenAI, copie o ID para `OPENAI_VECTOR_STORE_ID` e reinicie o Flask.

## Sync, Vector Store e Cache

O botao **Sync** envia notas locais para o OpenAI Vector Store.

Ele:

- envia notas novas;
- reenvia notas alteradas;
- remove do Vector Store arquivos apagados localmente;
- grava manifesto local em `.cortex_sync/`.

O botao **Ler Vector** monta o cache local:

```text
.cortex_vector_cache/openai_vector_store.json
```

Depois que o cache estiver utilizavel, chat e escrita usam esse cache antes de qualquer fallback local. Com `CORTEX_ALLOW_LIVE_VECTOR_SEARCH=0`, o Cortex evita busca viva paga no Vector Store.

Fluxo recomendado para economizar:

1. Clique em **Sync** depois de alterar bastante sua base.
2. Clique em **Ler Vector** para atualizar o cache.
3. Gere textos e converse usando o cache.
4. Deixe `CORTEX_ALLOW_LIVE_VECTOR_SEARCH=0`, salvo quando quiser pagar por busca remota em tempo real.

## Skills Privadas

Skills privadas ficam fora das notas e sao ignoradas pelo Git.

Padrao:

```text
.cortex_private_skills/
```

Voce pode alterar:

```env
CORTEX_PRIVATE_SKILLS_DIR=C:\Users\seu-usuario\Documents\cortex-private-skills
```

Estrutura esperada:

```text
agente_security/
  SKILL.md
security_reviwer/
  SKILL.md
revisor_pedro/
  SKILL.md
```

As skills `agente_security` e `security_reviwer` sao carregadas sempre que existirem, em chat, revisao de conexoes e escrita. Elas devem ficar privadas porque podem conter guardrails, criterios internos e dados sensiveis.

A skill `revisor_pedro` e criada automaticamente quando voce edita um texto gerado e clica em **Aprovar e salvar**. Ela registra aprendizados de estilo, preferencias e recusas explicitas, sem salvar isso nas notas do Cortex.

## Notas, Tags e Grafo

As notas ficam em Markdown dentro de `NOTES_ROOT`.

Use:

- `#tags` para enriquecer o grafo;
- `[[Wiki Links]]` para conectar notas;
- imagens via upload ou links Markdown.

Ao criar uma nota manualmente, ha um campo de tags com autocomplete baseado nas tags ja existentes. Na aba **Inteligencia**, o Cortex tambem sugere tags para a nota atual, mas elas so sao aplicadas quando voce aprova.

## Escrita

Na aba **Escrita**, voce pode gerar:

- LinkedIn post
- Artigo
- Texto solicitado

O texto gerado nao e salvo automaticamente.

Fluxo:

1. Gere o texto.
2. Edite o bloco principal, se quiser.
3. Ajuste as tags aprovadas.
4. Clique em **Aprovar e salvar**.

O arquivo aprovado vai para:

```text
notes/Artigos/
```

Se a pasta nao existir, o Cortex cria automaticamente.

## Inteligencia

A aba **Inteligencia** sugere:

- conexoes entre notas;
- tags relevantes para enriquecer o grafo.

Conexoes e tags precisam ser aprovadas manualmente. Rejeicoes de conexoes ficam em `.cortex_intelligence/`.

## Trocar o Mecanismo de Vector Store

A fronteira principal esta em `cortex_notes/agent.py`:

- `split_markdown`: prepara chunks;
- `CortexAgent.search`: recupera contexto relevante;
- `CortexAgent.chat`: envia pergunta e contexto para a LLM.

Um caminho futuro e extrair uma interface `VectorIndex.search(query, focus_path, limit)` e criar adaptadores para:

- OpenAI Vector Stores
- Chroma ou FAISS local
- Pinecone, Qdrant ou Weaviate

Assim a UI e a chamada da LLM continuam iguais; apenas o mecanismo de recuperacao muda.

## Testes

Rode:

```powershell
python -m unittest discover -s tests
python -m compileall app.py cortex_notes tests
```
