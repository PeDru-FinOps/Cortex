#agent #ia #crewai
## Curso completo de CrewAI — do zero ao multi-agente

```
Conteúdo: CrewAI
Subtópicos que serão cobertos:
1. O que é CrewAI?
2. Agentes
3. Tarefas (Tasks)
4. Ferramentas (Tools)
5. Crew e Process
6. Memória
7. Projeto completo
```

---

### Módulo 01 — O que é o CrewAI?

#### Conceito central

Um único LLM tem limites. Ele não consegue, ao mesmo tempo, pesquisar na internet, analisar dados, escrever um relatório e revisá-lo com qualidade. A solução é dividir o trabalho entre vários agentes especializados que colaboram — exatamente como uma equipe humana.

O **CrewAI** é um framework Python que permite criar esse tipo de sistema: você define agentes com papéis específicos, atribui tarefas a eles, dá ferramentas para que possam agir no mundo, e o sistema executa tudo de forma coordenada.

**Analogia:** pense em uma agência de marketing. Tem o pesquisador que levanta dados, o redator que escreve o texto, e o gerente que coordena tudo. Cada um é especialista no que faz. O CrewAI é o sistema que permite montar essa "agência" com IAs.

#### Os 4 pilares

**Agent** — o "funcionário". Um LLM com papel, objetivo e ferramentas definidos. [[Agente]]

**Task** — o "trabalho". Uma instrução específica com descrição e critério de conclusão.

**Tool** — a "capacidade". Funções que o agente pode usar: buscar na web, ler arquivos, executar código.

**Crew** — o "sistema". A equipe completa: agentes + tarefas + processo de execução.

#### Fluxo de execução

```
Entrada → Orquestrador → Agente A → Agente B → Saída
(sua instrução)  (planeja/delega)  (task 1)   (task 2)  (resultado)
```

#### Instalação

bash

```bash
pip install crewai crewai-tools

# Para usar com Ollama (modelo local):
pip install langchain-ollama
```

> **Dica:** crie sempre um ambiente virtual antes: `python -m venv venv && source venv/bin/activate`

---

### Módulo 02 — Agentes

#### Conceito central

Um **Agent** é um objeto Python que encapsula: um modelo de linguagem (LLM), um papel (`role`), um objetivo (`goal`), uma história de fundo (`backstory`) e, opcionalmente, uma lista de ferramentas. Esses parâmetros formam o "prompt de sistema" do agente — tudo o que define como ele pensa e age.

**Analogia:** o agente é uma ficha de personagem de RPG. O `role` é a classe (guerreiro, mago), o `goal` é a missão, o `backstory` é a história que explica por que ele é bom no que faz. Quanto mais rica a ficha, mais focado e consistente é o comportamento.

#### Parâmetros do Agent

|Parâmetro|O que faz|Obrigatório?|
|---|---|---|
|`role`|Define a especialidade do agente|✅ Sim|
|`goal`|O objetivo que ele persegue|✅ Sim|
|`backstory`|Contexto que molda o comportamento|✅ Sim|
|`llm`|Qual modelo usar (padrão: GPT-4)|⚠️ Recomendado|
|`tools`|Ferramentas que pode usar|❌ Opcional|
|`verbose`|Imprime o raciocínio no terminal|❌ Opcional|
|`allow_delegation`|Pode delegar para outros agentes?|❌ Padrão: False|
|`max_iter`|Máximo de iterações de raciocínio|❌ Padrão: 15|

#### Exemplo 1 — agente simples

python

```python
from crewai import Agent

redator = Agent(
    role="Redator especializado em tecnologia",
    goal="Criar artigos claros e precisos sobre temas de IA",
    backstory="""
        Você é jornalista técnico com 10 anos de experiência.
        Seu estilo é direto, evita jargão desnecessário e
        sempre usa exemplos concretos para explicar conceitos.
    """,
    verbose=True
)
```

#### Exemplo 2 — agente com Ollama (modelo local)

python

```python
from crewai import Agent
from langchain_ollama import OllamaLLM

llm_local = OllamaLLM(model="qwen2.5:14b")

pesquisador = Agent(
    role="Pesquisador de mercado",
    goal="Coletar e sintetizar informações relevantes sobre um tema",
    backstory="""
        Você é analista sênior com habilidade em encontrar
        padrões e insights em grandes volumes de informação.
    """,
    llm=llm_local,
    verbose=True
)
```

#### Erros comuns

**Role e goal vagos demais.** "Agente útil" e "fazer coisas boas" não dizem nada. Seja específico: "Especialista em SEO" e "Otimizar texto para ranking no Google".

**`allow_delegation` sem orquestrador.** Ativar delegação em agentes executores sem um agente orquestrador causa loops. Só ative no agente de coordenação.

**`max_iter` muito alto.** Se o agente não resolve em 10 iterações, o problema está no prompt — não aumente o limite.

---

### Módulo 03 — Tarefas (Tasks)

#### Conceito central

Uma **Task** descreve uma unidade de trabalho: o que precisa ser feito (`description`), o formato do resultado esperado (`expected_output`), e qual agente é responsável (`agent`). Opcionalmente recebe o resultado de outra task como contexto (`context`).

**Analogia:** se o agente é o funcionário, a Task é o brief do projeto. Um bom brief tem o que entregar, como deve ser o formato, e quem é o responsável. Sem brief claro, o funcionário entrega o que acha certo — que pode não ser o que você queria.

#### Parâmetros da Task

|Parâmetro|O que faz|Exemplo|
|---|---|---|
|`description`|O que o agente deve fazer|"Pesquise as 5 principais notícias de IA da semana"|
|`expected_output`|Como deve ser o resultado|"Lista com título, resumo e fonte de cada notícia"|
|`agent`|Qual agente executa|`pesquisador`|
|`context`|Tasks anteriores como insumo|`[task_pesquisa]`|
|`output_file`|Salva resultado em arquivo|`"resultado.md"`|
|`async_execution`|Executa em paralelo|`True`|

#### Exemplo 1 — task simples

python

```python
from crewai import Task

task_pesquisa = Task(
    description="""
        Pesquise as 5 principais notícias sobre Inteligência Artificial
        publicadas nos últimos 7 dias. Foque em avanços técnicos
        e lançamentos de novos modelos.
    """,
    expected_output="""
        Uma lista numerada com 5 notícias, cada uma contendo:
        - Título da notícia
        - Resumo de 2-3 frases
        - Fonte e data de publicação
    """,
    agent=pesquisador
)
```

#### Exemplo 2 — task com contexto (encadeamento)

python

```python
task_artigo = Task(
    description="""
        Com base nas notícias pesquisadas, escreva um artigo de blog
        de 600 palavras analisando as tendências encontradas.
        Use tom jornalístico e inclua uma conclusão com previsões.
    """,
    expected_output="""
        Artigo completo em Markdown com:
        - Título principal (H1)
        - 3 seções temáticas (H2)
        - Conclusão com 2-3 previsões
        - Aproximadamente 600 palavras
    """,
    agent=redator,
    context=[task_pesquisa],   # recebe o resultado da pesquisa
    output_file="artigo_ia.md" # salva automaticamente
)
```

#### Erros comuns

**`description` e `expected_output` idênticos.** Description diz o que fazer. Expected_output diz como o resultado deve ser. São coisas diferentes.

**Esquecer de encadear com `context`.** Se a Task B depende do resultado da Task A, você precisa passar `context=[task_a]`. Sem isso, o agente B não sabe o que A produziu.

**Task muito ampla.** Quebre em tasks atômicas: uma para pesquisar, outra para redigir, outra para revisar.

---

### Módulo 04 — Ferramentas (Tools)

#### Conceito central

Uma **Tool** é uma função Python que o agente pode chamar durante o raciocínio. O agente decide sozinho quando e como usá-la, com base na descrição da tool e no que a task pede.

**Analogia:** o agente é o analista. As tools são os aplicativos no computador dele: browser, Excel, terminal. Você não diz "abra o Chrome agora" — ele mesmo decide qual ferramenta usar para resolver o problema.

#### Tools prontas do CrewAI

`SerperDevTool` — busca no Google via API. Ideal para notícias e informações atuais.

`ScrapeWebsiteTool` — extrai o conteúdo de qualquer URL.

`FileReadTool` — lê arquivos locais (txt, md, json).

`PDFSearchTool` — busca semântica dentro de PDFs.

`CSVSearchTool` — pesquisa em arquivos CSV.

`RAGTool` — busca vetorial em uma coleção de documentos.

#### Exemplo 1 — usando tools prontas

python

```python
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool
import os

os.environ["SERPER_API_KEY"] = "sua_chave_aqui"
busca_web = SerperDevTool()
scraper = ScrapeWebsiteTool()
pdf_tool = PDFSearchTool(pdf="meus_documentos/manual.pdf")

pesquisador = Agent(
    role="Pesquisador",
    goal="Coletar informações relevantes",
    backstory="Analista experiente em coleta de dados",
    tools=[busca_web, scraper, pdf_tool],
    llm=llm_local
)
```

#### Exemplo 2 — criando uma tool personalizada

python

```python
from crewai.tools import tool
import feedparser  # pip install feedparser

@tool("Leitor de RSS de notícias")
def ler_rss_noticias(url_feed: str) -> str:
    """
    Lê um feed RSS e retorna as últimas 5 notícias.
    Use quando precisar de notícias atualizadas de uma fonte específica.
    Entrada: URL do feed RSS (ex: https://g1.globo.com/rss/g1/tecnologia/)
    """
    feed = feedparser.parse(url_feed)
    resultado = []
    for entry in feed.entries[:5]:
        resultado.append(f"Título: {entry.title}\nResumo: {entry.summary[:200]}\n")
    return "\n---\n".join(resultado)

agente_noticias = Agent(
    role="Monitor de notícias",
    goal="Manter-se atualizado sobre eventos relevantes",
    backstory="Curador de conteúdo especializado",
    tools=[ler_rss_noticias],
    llm=llm_local
)
```

> **Regra de ouro:** a docstring da função é o que o agente lê para decidir quando e como usar a tool. Escreva como se estivesse explicando para um humano: o que faz, quando usar, qual o formato da entrada.

---

### Módulo 05 — Crew e Process

#### Conceito central

A **Crew** é o objeto que reúne agentes, tasks e o modo de execução. O **Process** define como as tasks são executadas: em sequência (`sequential`) ou com um agente gerente que delega dinamicamente (`hierarchical`).

#### Os dois tipos de Process

**Sequential** — as tasks executam em ordem: task 1 → task 2 → task 3. O resultado de cada task alimenta a próxima. Previsível, fácil de debugar. Use quando o fluxo é linear e bem definido.

**Hierarchical** — um agente gerente analisa o objetivo e delega tasks dinamicamente para os agentes certos. Mais flexível e poderoso. Use quando você tem muitos agentes e quer delegação automática. É o processo do seu projeto.

#### Exemplo 1 — Process Sequential

python

```python
from crewai import Crew, Process

crew = Crew(
    agents=[pesquisador, redator],
    tasks=[task_pesquisa, task_artigo], # ordem importa
    process=Process.sequential,
    verbose=True
)

resultado = crew.kickoff()
print(resultado)
```

#### Exemplo 2 — Process Hierarchical

python

```python
from crewai import Crew, Process, Agent

gerente = Agent(
    role="Gerente de projetos",
    goal="Coordenar a equipe para entregar resultados de alta qualidade",
    backstory="Gerente experiente que sabe delegar e consolidar trabalhos",
    allow_delegation=True,  # OBRIGATÓRIO no gerente
    llm=llm_local
)

crew = Crew(
    agents=[pesquisador, redator, analista],
    tasks=[task_principal],
    process=Process.hierarchical,
    manager_agent=gerente,
    verbose=True
)

resultado = crew.kickoff(inputs={"tema": "tendências de IA em 2025"})
```

#### Variáveis dinâmicas nas Tasks

python

```python
# Use {variavel} na description para tornar a task dinâmica
task_flexivel = Task(
    description="Pesquise notícias sobre {tema} dos últimos {dias} dias",
    expected_output="Lista de 5 notícias relevantes sobre {tema}",
    agent=pesquisador
)

resultado = crew.kickoff(inputs={
    "tema": "inteligência artificial",
    "dias": "7"
})
```

> **Atenção:** no Process Hierarchical, o gerente consome tokens extras para planejar e delegar. Com modelos locais menores (7B), prefira o Sequential — modelos pequenos têm dificuldade com raciocínio de delegação complexo.

---

### Módulo 06 — Memória

#### O problema sem memória

Por padrão, cada `crew.kickoff()` é uma execução isolada. Os agentes não lembram do que fizeram antes. Se você pedir para resumir emails toda manhã, o agente não vai saber que já resumiu os de ontem.

#### Os 4 tipos de memória

1. **Short-term Memory** — guarda o contexto da execução atual. Os agentes compartilham o que aprenderam durante aquele kickoff. Habilitada automaticamente.
2. **Long-term Memory** — persiste informações entre execuções usando um banco SQLite local. Ideal para guardar preferências e resultados anteriores.
3. **Entity Memory** — extrai e memoriza entidades mencionadas (pessoas, empresas, produtos). Perfeito para manter contexto sobre clientes ou projetos específicos.
4. **Contextual Memory** — combina as três anteriores automaticamente. A forma mais prática de habilitar tudo de uma vez.

#### Habilitando memória na Crew

python

```python
from crewai import Crew, Process

crew = Crew(
    agents=[pesquisador, redator],
    tasks=[task_pesquisa, task_artigo],
    process=Process.sequential,
    memory=True,            # habilita memória contextual
    embedder={              # define como gerar embeddings
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",  # modelo local de embedding
            "base_url": "http://localhost:11434"
        }
    },
    verbose=True
)
```

> Para usar embeddings locais, baixe o modelo: `ollama pull nomic-embed-text`. É leve (274MB) e específico para embeddings.

#### Knowledge — injetando seus documentos

O Knowledge permite que todos os agentes consultem seus documentos sem precisar de uma tool explícita. É a forma mais simples de RAG no CrewAI.

python

```python
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

meus_pdfs = PDFKnowledgeSource(
    file_paths=["docs/manual_empresa.pdf", "docs/processos.pdf"]
)

meus_textos = TextFileKnowledgeSource(
    file_paths=["notas/briefing.txt"]
)

crew = Crew(
    agents=[redator, analista],
    tasks=[task_redacao],
    knowledge_sources=[meus_pdfs, meus_textos],
    embedder={
        "provider": "ollama",
        "config": {"model": "nomic-embed-text"}
    },
    verbose=True
)
```

---

### Módulo 07 — Projeto completo

#### O que vamos construir

Um sistema com agente orquestrador que delega para 3 especialistas: um pesquisador (scraping de notícias via RSS), um redator (gera textos com base nos seus documentos) e um analista (resume emails). Com memória persistente e modelos 100% locais via Ollama.

#### Estrutura de arquivos

```
meu_sistema/
├── main.py           # ponto de entrada
├── agents.py         # definição de todos os agentes
├── tasks.py          # definição de todas as tasks
├── tools.py          # ferramentas personalizadas
├── crew.py           # montagem da crew
├── docs/             # seus documentos para RAG
│   └── base_conhecimento.pdf
└── .env              # variáveis de ambiente
```

#### tools.py

python

```python
from crewai.tools import tool
from crewai_tools import ScrapeWebsiteTool
import feedparser

@tool("Leitor de RSS")
def rss_tool(url_feed: str) -> str:
    """
    Lê um feed RSS e retorna as últimas 5 notícias.
    Use para coletar notícias de fontes como G1, TechCrunch, etc.
    Entrada: URL do feed RSS.
    """
    feed = feedparser.parse(url_feed)
    resultado = []
    for entry in feed.entries[:5]:
        resultado.append(f"Título: {entry.title}\nResumo: {entry.summary[:300]}\n")
    return "\n---\n".join(resultado)

scraper_tool = ScrapeWebsiteTool()
```

#### agents.py

python

```python
from crewai import Agent
from langchain_ollama import OllamaLLM
from tools import rss_tool, scraper_tool

llm = OllamaLLM(model="qwen2.5:14b")

orquestrador = Agent(
    role="Orquestrador de automações",
    goal="Entender a solicitação e delegar para o especialista correto",
    backstory="Gerente técnico experiente em coordenar equipes de IA",
    allow_delegation=True,
    llm=llm,
    verbose=True
)

pesquisador = Agent(
    role="Pesquisador de notícias e tendências",
    goal="Coletar informações atualizadas de fontes confiáveis",
    backstory="Jornalista de dados com foco em tecnologia e negócios",
    tools=[rss_tool, scraper_tool],
    llm=llm,
    verbose=True
)

redator = Agent(
    role="Redator de conteúdo especializado",
    goal="Criar textos de alta qualidade baseados em documentos e briefings",
    backstory="Escritor com 15 anos de experiência em conteúdo corporativo",
    llm=llm,
    verbose=True
)

analista = Agent(
    role="Analista de comunicações",
    goal="Resumir e classificar emails e documentos de forma eficiente",
    backstory="Assistente executivo especializado em gestão de informações",
    llm=llm,
    verbose=True
)
```

#### main.py

python

```python
from crewai import Crew, Process, Task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from agents import orquestrador, pesquisador, redator, analista

base_docs = PDFKnowledgeSource(file_paths=["docs/base_conhecimento.pdf"])

task_geral = Task(
    description="""
        Solicitação: {solicitacao}

        Analise a solicitação acima e execute:
        1. Se pedir notícias/pesquisa → delegue ao pesquisador
        2. Se pedir geração de texto/artigo → delegue ao redator
        3. Se pedir resumo de emails → delegue ao analista

        Consolide os resultados e entregue uma resposta completa.
    """,
    expected_output="Resultado completo e bem formatado da solicitação",
    agent=orquestrador
)

crew = Crew(
    agents=[orquestrador, pesquisador, redator, analista],
    tasks=[task_geral],
    process=Process.hierarchical,
    manager_agent=orquestrador,
    memory=True,
    knowledge_sources=[base_docs],
    embedder={
        "provider": "ollama",
        "config": {"model": "nomic-embed-text"}
    },
    verbose=True
)

if __name__ == "__main__":
    pedido = input("O que você quer fazer? → ")
    resultado = crew.kickoff(inputs={"solicitacao": pedido})
    print("\n═══ RESULTADO ═══\n")
    print(resultado)
```