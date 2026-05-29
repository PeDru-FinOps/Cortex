#datadog #finops #data_governance 

As APIs de Usage Metering do Datadog permitem consultar:

- Métricas de uso
- Consumo faturável
- Estimativas de custo
- Custos históricos
- Projeções de custo
- Atribuição de custos por tags

A principal diferença entre os endpoints é:

| Categoria | O que retorna |
|---|---|
| Usage APIs | Métricas de consumo/utilização |
| Cost APIs | Valores monetários ou estimativas financeiras |

Documentação oficial:  
https://docs.datadoghq.com/api/latest/usage-metering/

---
# Disponibilidade

Disponível para planos:

- PRO
- ENTERPRISE

Alguns endpoints exigem recursos adicionais habilitados, como:

- Cost Attribution
- [[Unified Service Tagging]]
- [[Multi-Organization]] Billing

---
# Características gerais

| Característica | Detalhes |
|---|---|
| Retenção | Até 15 meses |
| Delay de processamento | Até 72 horas |
| Granularidade | Horária, diária e mensal |
| Escopo | Single-org e Multi-org |
| Autenticação | API Key + Application Key |

---
# Autenticação

As APIs utilizam:

- `DD-API-KEY`
- `DD-APPLICATION-KEY`

Exemplo:

```bash
curl -X GET "https://api.datadoghq.com/api/v1/usage/summary" \
-H "DD-API-KEY: <API_KEY>" \
-H "DD-APPLICATION-KEY: <APP_KEY>"
```

---

# Classificação dos endpoints

| Endpoint                                | Categoria        | Retorna                            |
| --------------------------------------- | ---------------- | ---------------------------------- |
| `/usage/hourly-attribution`             | Usage            | Métricas de uso por tags           |
| `/usage/monthly-attribution`            | Usage            | Métricas mensais de uso por tags   |
| `/usage/billable-summary`               | Billable Usage   | Quantidades faturáveis             |
| `/usage/summary`                        | Usage            | Resumo geral de utilização         |
| `/usage/estimated_cost`                 | Cost             | Estimativa de custo                |
| `/usage/historical_cost`                | Cost             | Custos históricos                  |
| `/usage/projected_cost`                 | Cost             | Projeção de custo                  |
| `/cost_by_tag/monthly_cost_attribution` | Cost Attribution | Custos mensais atribuídos por tags |

---
# Get Hourly Usage Attribution

Recupera métricas horárias de uso atribuídas por tags.

## Endpoint

```http
GET /api/v1/usage/hourly-attribution
```

## URL completa

```http
https://api.datadoghq.com/api/v1/usage/hourly-attribution
```

---
## O que essa API retorna

Essa API retorna métricas de consumo operacional, não custos monetários.

Exemplos:

- Infra Hosts
- Containers
- Indexed Logs
- APM Hosts
- Custom Metrics
- Indexed Spans

Os dados são agrupados por tags.

---
## Exemplos de uso

| Uso | Exemplo |
|---|---|
| Rateio interno | Uso por time |
| Governança | Uso por ambiente |
| Kubernetes | Uso por namespace |
| Observabilidade | Crescimento de consumo |

---
## Importante

Essa API:

- NÃO retorna valores monetários
- NÃO representa invoice
- NÃO retorna billing consolidado

Ela normalmente é usada como base para cálculo interno de chargeback/showback.

---
# Get Monthly Usage Attribution

Recupera métricas mensais de uso atribuídas por tags.

## Endpoint

```http
GET /api/v1/usage/monthly-attribution
```

## URL completa

```http
https://api.datadoghq.com/api/v1/usage/monthly-attribution
```

---
## O que essa API retorna

Retorna consumo consolidado mensal por produto e tags.

Exemplos:

- Quantidade de hosts
- Volume de logs
- Uso de containers
- Uso de custom metrics

---
## Importante

Essa API:

- NÃO retorna custo financeiro
- NÃO substitui invoice
- NÃO possui pricing aplicado

---
## Casos de uso

- Relatórios operacionais
- Tendência mensal
- Capacity planning
- Base para showback

---
# Get Billable Usage Summary

Retorna resumo de unidades faturáveis da conta.

## Endpoint

```http
GET /api/v1/usage/billable-summary
```

## URL completa

```http
https://api.datadoghq.com/api/v1/usage/billable-summary
```

---
## O que essa API retorna

Retorna quantidades consideradas faturáveis pelo Datadog.

Exemplos:

- Billable hosts
- Billable containers
- Indexed logs
- Indexed spans
- Custom metrics

---
## Importante

Essa API:

- NÃO retorna custo monetário
- Retorna quantidades utilizadas para billing
- É mais próxima do invoice do que as APIs de usage attribution

---
## Casos de uso

- Auditoria de invoice
- Conferência de billing
- Análise de crescimento faturável

---
# Get Usage Across Account

Retorna resumo geral de utilização da conta.

## Endpoint

```http
GET /api/v1/usage/summary
```

## URL completa

```http
https://api.datadoghq.com/api/v1/usage/summary
```

---
## O que essa API retorna

Retorna métricas gerais de utilização da organization.

Exemplos:

- Infra hosts
- Containers
- Logs
- Synthetics
- RUM
- APM

---
## Importante

Essa API:

- NÃO retorna custos
- NÃO retorna pricing
- NÃO retorna invoice

---

## Casos de uso

- Dashboards operacionais
- Capacity planning
- Tendência de crescimento

---
# Get Estimated Cost Across Account

Retorna estimativa de custo da conta.

## Endpoint

```http
GET /api/v2/usage/estimated_cost
```

## URL completa

```http
https://api.datadoghq.com/api/v2/usage/estimated_cost
```

---
## O que essa API retorna

Retorna estimativas monetárias de custo.

Exemplos:

- Estimated total cost
- Estimated product cost
- Estimated account cost

---
## Importante

Essa API:

- Retorna estimativas
- NÃO representa invoice fechado
- Pode sofrer alterações até o fechamento do billing

---
## Casos de uso

- Forecast
- Budget tracking
- Alertas financeiros

---
# Get Historical Cost Across Account

Retorna custos históricos processados.

## Endpoint

```http
GET /api/v2/usage/historical_cost
```

## URL completa

```http
https://api.datadoghq.com/api/v2/usage/historical_cost
```

---
## O que essa API retorna

Retorna custos monetários históricos consolidados.

Exemplos:

- Custos mensais
- Custos por produto
- Custos consolidados da organization

---
## Importante

Essa API:

- Retorna custo financeiro
- É baseada no billing processado
- É mais adequada para relatórios financeiros

---
## Casos de uso

- Fechamento mensal
- Relatórios FinOps
- Auditoria financeira

---
# Get Projected Cost Across Account

Retorna projeção de custo até o final do período atual.

## Endpoint

```http
GET /api/v2/usage/projected_cost
```

## URL completa

```http
https://api.datadoghq.com/api/v2/usage/projected_cost
```

---
## O que essa API retorna

Retorna projeções monetárias futuras baseadas no consumo atual.

Exemplos:

- Forecast mensal
- Estimativa de fechamento
- Tendência de crescimento financeiro

---
## Importante

Essa API:

- Trabalha com estimativas
- NÃO representa billing fechado
- Pode mudar conforme o consumo cresce

---
## Casos de uso

- Budget forecast
- Previsão financeira
- Alertas de estouro de orçamento

---
# Get Monthly Cost Attribution

Retorna custos mensais atribuídos por tags.

## Endpoint

```http
GET /api/v2/cost_by_tag/monthly_cost_attribution
```

## URL completa

```http
https://api.datadoghq.com/api/v2/cost_by_tag/monthly_cost_attribution
```

---
## O que essa API retorna

Retorna custos monetários distribuídos por tags.

Exemplos:

- Custo por ambiente
- Custo por aplicação
- Custo por equipe
- Custo por cliente

---
## Importante

Essa API:

- Retorna custo financeiro
- Depende de tagging adequada
- Exige Cost Attribution habilitado

---
## Casos de uso

- Chargeback
- Showback
- FinOps
- Rateio financeiro

---
# Recomendações FinOps

## Padronizar tags

Exemplos:

```text
env:prod
team:finops
service:payments
cost_center:123
```

---
## Separar APIs de usage e cost

| Tipo | Objetivo |
|---|---|
| Usage APIs | Operação e consumo |
| Cost APIs | Financeiro e billing |

---
## Não misturar “usage” com “invoice”

Métricas de uso:

- Não representam custo automaticamente
- Podem divergir do billing final
- Precisam de pricing/rate card para cálculo financeiro

---
# Referências

- https://docs.datadoghq.com/api/latest/usage-metering/
- https://docs.datadoghq.com/account_management/billing/cost_attribution/
- https://docs.datadoghq.com/account_management/billing/usage_attribution/