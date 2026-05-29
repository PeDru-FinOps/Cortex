#ia 

Interessante utilizar o [[ICON-REAL Framework]] para o Fine Tuning
## Criar dataset (JSONL)

![[Pasted image 20260414102626.png]]
## Utilizar uma ferramenta de Fine Tuning

LoRA é leve e viável localmente.

## Treinar

![[Pasted image 20260414102724.png]]

________________________________________

Você usa o modelo + adapter LoRA no seu runner (tipo LM Studio, Ollama, etc.)

Fine-tuning NÃO é bom para:

- Corrigir fatos isolados ❌
- Evitar erros pontuais ❌
- Pequenas melhorias ❌

Para isso, use **prompt + RAG**

_______________________________

# Regra de ouro

Use essa ordem:

1. Prompt engineering
2. Exemplos (few-shot)
3. RAG
4. **Só então fine-tuning**