#cloud8 

A conversa foi uma reunião estratégica e operacional sobre análise de billing, margens e expansão de FinOps usando a plataforma Cloud8 para clientes da Movit.

Principais pontos:

- Vinicius apresentou análises detalhadas de custos e descontos da GCP, incluindo:
    
    - Reseller Margin
        
    - CUD (Committed Use Discount)
        
    - SUD (Sustained Use Discount)
        
    - Créditos promocionais
        
    - Impacto dos descontos na margem real da Movit.
        
- Polyanna explicou que:
    
    - A margem varia muito conforme compromissos comerciais com o Google.
        
    - Alguns clientes chegam a ter margem abaixo de 5%.
        
    - Em certos produtos, a margem praticamente desaparece devido a CUDs e acordos anuais.
        
- O cliente mais crítico identificado foi a Funcional Health:
    
    - Grande volume de billing.
        
    - Margem considerada muito baixa.
        
    - Necessidade de investigação detalhada produto a produto.
        
- Foram analisados também:
    
    - Tidas
        
    - Box
        
    - Eletromídia
        
    - Henticars
        
    - Clientes consumindo Gemini API com custos altos inesperados.
        
- Discussão técnica relevante:
    
    - Gemini API possui custo híbrido:
        
        - assinatura por usuário
            
        - excedente por consumo de tokens
            
    - Diferença entre “taxa Google” e câmbio de mercado devido impostos embutidos.
        
- Cloud8 foi posicionado como:
    
    - Ferramenta de investigação de margem
        
    - Plataforma de FinOps
        
    - Possível mecanismo de retenção de clientes
        
    - Base para dashboards, chargeback/showback e governança multicloud.
        
- Polyanna trouxe um direcionamento estratégico importante:
    
    - Não vender a ideia internamente como “vocês estão perdendo dinheiro”.
        
    - Posicionar o Cloud8 como:
        
        - agregador de valor
            
        - retenção de clientes
            
        - diferenciação comercial
            
        - expansão de serviços de sustentação e FinOps.
            
- Ela destacou que:
    
    - O diretor Edilson é a pessoa-chave para convencer a diretoria.
        
    - Ricardo é operacional/técnico.
        
    - A venda estratégica precisa envolver liderança e área comercial.
        
- Também surgiram oportunidades futuras:
    
    - FinOps multicloud (AWS, OCI, Azure)
        
    - Projetos de tagging e chargeback
        
    - Dashboards financeiros por centro de custo
        
    - Consultoria FinOps como serviço adicional.
        
- Conclusão prática:
    
    - Priorizar clientes já com sustentação.
        
    - Expandir valor percebido do Cloud8.
        
    - Criar estratégia de FinOps consultivo.
        
    - Treinar ou contratar perfil analítico focado em billing/FinOps.
        
    - Aproximar diretoria da proposta estratégica.

## Sobre a Tidas

A Tidas apareceu como um caso relevante por consumo elevado e particularidades de faturamento.

Pontos principais:

- Houve um consumo muito alto de Gemini API:
    
    - cerca de R$ 81 mil em apenas dois dias.
        
    - Isso levantou preocupação de possível uso indevido ou consumo não percebido pelo cliente.
        
- Vinicius alertou que:
    
    - o cliente provavelmente reclamaria da cobrança;
        
    - seria importante avisar rapidamente o responsável da conta.
        
- Foi discutido que o Gemini API possui:
    
    - cobrança por usuário/mês;
        
    - e também cobrança adicional por consumo de tokens.
        
- A Tidas possui uma estrutura de faturamento dividida:
    
    - dois CNPJs;
        
    - rateio interno;
        
    - separação baseada no nome dos projetos dentro da GCP.
        
- Polyanna explicou que:
    
    - o rateio não é manual;
        
    - os próprios projetos já indicam qual empresa pertence cada custo.
        
- Vinicius sugeriu:
    
    - criar tags sintéticas no Cloud8;
        
    - automatizar esse tipo de separação e faturamento.
        
- Também identificaram:
    
    - margem alta em Security Command Center (~25%);
        
    - comparação de valores faturados vs cálculos do Cloud8 para validar consistência da cobrança.
        

---

## Sobre o Flamengo

O Flamengo foi discutido como um caso complexo de FinOps e governança financeira.

Pontos principais:

- O cliente quer:
    
    - visão por centro de custo;
        
    - consumo separado por projeto;
        
    - dashboards orçamentários;
        
    - acompanhamento financeiro detalhado.
        
- O Ricardo tentou resolver isso diretamente na GCP:
    
    - mas concluiu que a console não entregava exatamente o que o cliente queria.
        
- Como consequência:
    
    - a Movit desenvolveu um aplicativo próprio;
        
    - além de usar Cloud8;
        
    - além de planilhas auxiliares;
        
    - criando um ecossistema operacional complexo.
        
- Polyanna comentou que:
    
    - o Flamengo é um cliente muito exigente;
        
    - tende a pedir soluções altamente customizadas;
        
    - exige adaptação ao modelo deles.
        
- Vinicius comentou que:
    
    - esse tipo de demanda é comum em grandes empresas;
        
    - trata-se essencialmente de um projeto de chargeback/showback FinOps.
        
- O Flamengo foi citado como exemplo de:
    
    - oportunidade estratégica de retenção via FinOps;
        
    - cliente que pode ficar “preso” à plataforma caso dashboards, alertas e governança sejam implementados corretamente.
        
- Também houve um ponto comercial importante:
    
    - a Movit praticamente não cobra sustentação do Flamengo;
        
    - porque o contrato foi vendido como um “pacotão” com vários produtos e serviços inclusos.
        
- Polyanna explicou que:
    
    - o Flamengo é um cliente estratégico;
        
    - altamente influenciado pelo diretor Edilson;
        
    - e que o relacionamento é delicado devido às constantes demandas.