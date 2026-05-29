#ia #sop #bestpractices 

Baseado no [[Projeto Neon - Guideline]]
Avaliar antes do [[Projeto Neon - Checklist]]

# 1. O QUE É TASK FLAGGING (EM 1 FRASE)

> É decidir se você **NÃO deve fazer a task** porque ela está fora do escopo correto.

---

# 2. REGRA DE OURO

> **Se a task não pode ser avaliada corretamente → você deve flaggar**

---

# 3. QUANDO VOCÊ DEVE FLAGGAR (DECISÃO RÁPIDA)

Use esse fluxo mental:

### PASSO 1

Isso envolve algum desses temas?

- conteúdo perigoso
- conteúdo ilegal
- conteúdo explícito
- dados pessoais
- coisa que o modelo não consegue fazer
- conhecimento muito específico
- precisa de informação atual (2025+)
- idioma que você não domina

Se **SIM → provavelmente flag**

---

# 4. PRINCIPAIS TIPOS DE FLAG (COMO IDENTIFICAR)

---

## 1. UNSAFE CONTENT (MAIS IMPORTANTE)

Flag se envolver:

- violência
- sexual
- suicídio
- ódio
- atividades ilegais
- instruções perigosas

Exemplo:

- “como fazer uma bomba caseira”
- “simule diálogo de automutilação”

→ **Sempre flaggar (mesmo que seja fictício)**

---

## 2. OUTRO IDIOMA (LANGUAGE MISMATCH)

Flag se:

- precisa escrever muito em idioma que não é o seu
- exige fluência real

Não flag se:

- é só uma palavra ou tradução simples

---

## 3. BEYOND MODEL CAPABILITY

Flag se exige:

- acessar link
- analisar arquivo externo
- gerar imagem
- acessar internet
- dados em tempo real

Exemplo:

- “resuma esse link”
- “pegue dados dessa página”

---

## 4. REQUIRES RECENT KNOWLEDGE

Flag se:

- precisa saber algo após fevereiro de 2025

Exemplo:

- “quais empresas demitiram em 2025?”

Não flag se:

- pode responder com conhecimento geral

---

## 5. LENGTH EXCESSIVO

Flag se:

- pede > 2000 palavras explicitamente

Exemplo:

- “escreva um artigo de 10.000 palavras”

---

## 6. ASSISTANT-SPECIFIC

Flag se pergunta:

- sobre o modelo em si
- funcionamento interno
- memória
- treinamento

---

## 7. STEM AVANÇADO

Flag se:

- precisa conhecimento técnico real
- matemática multi-step
- física, química, etc.

Regra prática:  
→ Se não é “conhecimento comum”, flag

---

# 5. QUANDO NÃO FLAGGAR (IMPORTANTE)

Não flag se:

- é difícil, mas possível
- é ambíguo (você tenta responder)
- é filosófico
- é conhecimento geral

---
# 6. ERRO MAIS COMUM

### ERRADO:

“Parece difícil → vou flaggar”

### CERTO:

“É impossível avaliar corretamente → flag”

---

# 7. PROCESSO CORRETO (OPERACIONAL)

Segundo o guia :

1. Identifica o problema
2. Vai na aba de Task Flagging
3. Seleciona a categoria correta
4. Justifica
5. Marca “Should the task be skipped”
6. Submete para QC

---

# 8. CHECKLIST RÁPIDO DE FLAG

Antes de seguir com a task, pergunte:

- Precisa de conhecimento externo?
- Precisa de info atual?
- Envolve risco?
- Está fora da capacidade do modelo?
- Eu consigo avaliar com segurança?

Se alguma resposta for “não consigo” → flag

---

# 9. HEURÍSTICA SIMPLES (DECISÃO EM 5 SEGUNDOS)

Se cair em um desses 3:

- perigoso
- impossível
- fora do escopo

→ FLAG

---

# 10. MENTALIDADE CORRETA

Você NÃO está sendo pago para:

- resolver tudo
- forçar avaliação

Você está sendo pago para:

> **garantir qualidade do dataset**

---

# 11. EXEMPLOS PRÁTICOS

### Caso 1

“Resuma esse site: [link]”  
→ FLAG (beyond capability)

---

### Caso 2

“Explique fotossíntese”  
→ NÃO FLAG (conhecimento comum)

---

### Caso 3

“Como fabricar droga X”  
→ FLAG (unsafe)

---

### Caso 4

“Escreva um artigo de 5000 palavras”  
→ FLAG (length)

---

# 12. REGRA FINAL

Se você está em dúvida:

> Melhor flaggar do que avaliar errado