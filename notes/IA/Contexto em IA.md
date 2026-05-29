#ia 
Contexto são as informações específicas e importantes para o usuário e seu negócio. Abaixo uma forma de organizar contexto de uma forma geral e replicável, independente do modelo.

## Pasta PKA

***Personal Knowledge Assistance (PKA)*** é um trabalho manual de gerenciar conhecimento, uma camada leve de automação para conectar informações. O grande insight é que é sempre um trabalho manual, como o que estou fazendo nesse Vault do Obsidian. Ela é composta por subpastas.

- Capturar informações
- Organizar informações
- Transformar informações
- Reutilizar informações
### IA.md

Arquivo .md com a identidade do agente que está sendo configurado, funcionando como um orquestrador para as pastas de contexto do Agente. É um setup básico.

- Quem é a IA
- Como ela pensa
- Como ela usa o conhecimento

Utiliza o [[Modelo de Comportamento do Agente]]

Interessante configurar neste documento os [[Princípios de Comportamento de um Modelo]] para não precisar repetir em cada [[IA/Skills]].

Modelo: [[Model - Agent Identity]]
### SessionLogging.md

Serve como memórias de sessão / rastreamento de interações.

Após concluir uma sessão, acionar o comando para IA criar um session Logging com base nos insights, temas e conclusões gerados.

Modelo: [[Model - SessionLogging]]

Conteúdo:

- Objetivo do Agente
- Tom de voz
- Regras de resposta
- Onde buscar informação
### Personal Inbox

Notas não catalogadas e categorizadas.
### AI Team Inbox

Conhecimento gerado pela IA que não foi validado.

- Respostas
- Análises geradas
- Brainstorms
- Drafts

Você cria um folder para cada Agente dentro desse Inbox.
### Business Knowledge Management

#### SOPs: 
Processos repetitíveis.
#### Expert Knowledge: 

O conhecimento técnico organizado. No meu contexto, pode ser adaptado para utilizar o Vault da Obsidian.
#### Skills: 

[[IA/Skills]] são blocos reutilizáveis de comportamento + lógica + contexto. 

Modelo: [[Model - Skill]]
#### Assets: 

Modelos e exemplos que podem ser utilizados como base para criar gráficos, imagens, banners, etc.