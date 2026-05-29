#ia #skill #sop #model 

Baseado no modelo de [[Estrutura do Bullet Journal]]

---
name: bullet-journal
description: >
  Capturar, classificar, organizar e manter entradas no Bullet Journal, garantindo
  consistência entre Registro Diário, Registro Mensal, Registro Futuro e Índice.
  
  Ative esta skill sempre que o usuário estiver operando explicitamente seu Bullet Journal —
  por exemplo: registrando tarefas, eventos ou notas; consultando ou atualizando registros;
  realizando migrações; ou pedindo para organizar, revisar ou estruturar entradas do BuJo.
  
  NÃO ative para conversas genéricas, perguntas técnicas ou qualquer mensagem que não
  tenha relação com o gerenciamento do Bullet Journal do usuário.
---

# Bullet Journal Skill

## Visão Geral

Esta skill implementa o método Bullet Journal (BuJo) original com uma extensão opcional
de Migração Diária.

---

## Classificação de Entradas

Toda entrada deve ser classificada em exatamente um tipo:

| Marcador | Tipo    | Critério                          |
|----------|---------|-----------------------------------|
| `( . )`  | Tarefa  | Contém ação executável            |
| `( ∘ )`  | Evento  | Ocorrência com data específica    |
| `( - )`  | Nota    | Informação ou insight             |

**Regras de decisão:**
- Se contém ação → Tarefa
- Se contém data explícita e é uma ocorrência → Evento
- Caso contrário → Nota

> ⚠️ Uma tarefa com data futura **não vira Evento**. Ela permanece Tarefa e recebe o
> marcador `( < )` (agendada), sendo encaminhada ao Registro Futuro.

---

## Marcadores Completos

| Marcador           | Significado         |
|--------------------|---------------------|
| `( . )`            | Tarefa pendente     |
| `( x )`            | Tarefa concluída    |
| `( > )`            | Tarefa migrada      |
| `( < )`            | Tarefa agendada     |
| ~~texto riscado~~  | Tarefa irrelevante  |
| `( ∘ )`            | Evento              |
| `( - )`            | Nota                |

---

## Roteamento

O **Registro Diário é sempre o ponto de captura** — toda entrada começa aqui, sem exceção.
A partir daí, algumas entradas também aparecem em outros registros com funções distintas.

| Entrada                            | Diário | Mensal | Futuro |
|------------------------------------|--------|--------|--------|
| Tarefa sem data                    | ✅      | Pode ser promovida | —  |
| Tarefa com data no mês atual       | ✅      | —      | —      |
| Tarefa com data futura `( < )`     | ✅      | —      | ✅      |
| Evento no mês atual                | ✅      | —      | —      |
| Evento fora do mês atual           | ✅      | —      | ✅      |
| Nota                               | ✅      | —      | —      |

**Importante:** aparecer no Mensal ou no Futuro não remove a entrada do Diário.
São registros com funções diferentes, não destinos exclusivos.

---

## Estrutura de Entrada

**Formato obrigatório:**
```
MARCADOR TÓPICO ESTRUTURADO
    Sub-tarefa (opcional, com tabulação)
```

**Tópico obrigatório** — seguir o padrão:
```
DD/MM.DDD / Contexto / Assunto
```

**Exemplo:**
```
( . ) 21/04.TER / Estudos / Navegação costeira
    Revisar cartas náuticas
    Resolver exercícios
```

---

## Paginação

- Cada Registro Diário ocupa uma nova página
- Registros com mesma data podem ocupar a mesma página
- Registro Mensal ocupa duas páginas:
  - Página 1: calendário (número do dia + dia da semana)
  - Página 2: lista de tarefas do mês
- Registro Futuro ocupa páginas dedicadas
- Coleções ocupam páginas próprias com título

---

## Coleções

Uma Coleção é um conjunto de entradas relacionadas que merece páginas próprias.

**Quando criar:** quando uma tarefa acumular muitas sub-tarefas, ela deve ser convertida
em uma Coleção — isso é um sinal de que o tema é complexo o suficiente para ter espaço dedicado.

**Como criar:**
1. Atribuir um título claro à Coleção
2. Anotar o número da página
3. Registrar no Índice
4. Referenciar a partir do Registro Diário com o número da página

---

## Índice

O Índice é um mecanismo de **localização**, não de lógica. Deve ser atualizado a cada
nova entrada relevante.

**Estrutura:**
```
TAREFAS
  Item — p.X

NOTAS
  Item — p.X

COLEÇÕES
  Nome da Coleção — p.X

ARQUIVO
  Item — p.X
```

**Regras de atualização:**

| Situação                  | Ação no Índice                    |
|---------------------------|-----------------------------------|
| Nova Tarefa ou Nota       | Adicionar na seção correspondente |
| `( x )` concluída         | Mover para ARQUIVO                |
| `( > )` migrada           | Mover para ARQUIVO                |
| `( < )` agendada          | Mover para ARQUIVO                |
| Nova Coleção              | Adicionar em COLEÇÕES             |
| `( ∘ )` Evento            | Não indexar                       |

---

## Migração

### Migração Mensal 

Ao final do mês:
- Avaliar todas as tarefas pendentes
- Para cada uma, decidir: **migrar**, **agendar** ou **remover**
- Tarefas migradas: copiar para o novo mês e marcar com `( > )` no mês anterior
- Tarefas agendadas para data futura: mover para o Registro Futuro com `( < )`

### Migração Anual 

Ao final do ano:
- Revisar todo o conteúdo do Bullet Journal
- Migrar o que ainda é relevante para o novo caderno

### Migração Diária

Ao final do dia:
- Avaliar tarefas não concluídas
- Decidir: manter para o dia seguinte, migrar ao Mensal ou remover

> Esta é uma extensão do método original. Útil para quem usa o BuJo ativamente
> no dia a dia, mas não faz parte do sistema base de Ryder Carroll.

**Regra geral:** nenhuma tarefa deve permanecer ativa sem passar por processo de migração.

---

## Entradas Escaneadas (imagens)

Ao receber uma imagem do Bullet Journal, reconhecer entradas pelos marcadores:

| Marcador visual      | Interpretação       |
|----------------------|---------------------|
| `( . )`              | Tarefa pendente     |
| `( x )`              | Tarefa concluída    |
| `( > )`              | Tarefa migrada      |
| `( < )`              | Tarefa agendada     |
| Texto riscado        | Tarefa irrelevante  |
| `( ∘ )`              | Evento              |
| `( - )`              | Nota                |

---

## Processo de Execução

Para cada nova entrada recebida:

1. **Classificar** — Tarefa, Evento ou Nota
2. **Determinar destino** — Diário (sempre) + Mensal ou Futuro se aplicável
3. **Estruturar** — marcador + tópico formatado + sub-tarefas se houver
4. **Inserir** no(s) registro(s) adequado(s)
5. **Atualizar o Índice** — se for Tarefa, Nota ou Coleção

---

## Regras de Consistência

- Toda entrada deve ter marcador
- Toda entrada deve ter tópico estruturado
- Uma tarefa só pode ser concluída se todas as sub-tarefas estiverem concluídas
- Tarefas com muitas sub-tarefas devem ser convertidas em Coleções
- O Registro Diário é sempre o ponto de captura — nunca pule esta etapa

---

## Hierarquia de Registros

```
Entrada → Registro Diário → (Mensal ou Futuro) → Execução → Migração → Arquivo
```