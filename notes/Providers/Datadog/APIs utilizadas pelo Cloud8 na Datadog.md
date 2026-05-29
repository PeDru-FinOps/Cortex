#cloud8 #finops #datadog #cloudcomputing 

## Usage Metering

A principal fonte de consumo e uso será a  [[API - Usage Metering]] da Datadog.

Esses endpoints permitem coletar:

- uso por produto
- uso horário
- uso diário
- métricas de billing
- consumo de infraestrutura
- consumo de logs
- APM
- containers
- custom metrics
- indexed logs
- ingestão

---

## Monthly Cost Attribution

Quando disponível no ambiente do cliente, a Cloud8 poderá utilizar dados de:

- Monthly Cost Attribution
- Cloud Cost Management

para melhorar a precisão da atribuição financeira.

---

## Importante sobre fechamento mensal

Em contas com direct billing Datadog, os dados do mês anterior normalmente ficam disponíveis após fechamento do ciclo de faturamento.

Em muitos casos, isso ocorre até o dia 19 do mês corrente.

---

# APIs de APM

O cliente também pode disponibilizar APIs relacionadas a APM.

Exemplo:

```
GET /api/v2/apm/services
```

Importante:

Esses endpoints são úteis para:

- inventário técnico
- identificação de serviços
- categorização operacional
- enriquecimento de metadata

Porém, eles não devem ser considerados como fonte primária de custos.

Para billing e consumo financeiro, a integração prioriza:

- Usage Metering
- Cost Attribution
- Billing APIs

## Referências

https://docs.datadoghq.com/account_management/billing/usage_attribution/?utm_source=chatgpt.com

https://docs.datadoghq.com/api/latest/usage-metering/?utm_source=chatgpt.com

https://docs.datadoghq.com/account_management/plan_and_usage/cost_details/?utm_source=chatgpt.com