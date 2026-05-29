#datadog #data_analysis #management #cloudcomputing 

A funcionalidade de **Usage Attribution** do [Datadog](https://www.datadoghq.com?utm_source=chatgpt.com) serve para quebrar o consumo da plataforma por tags, permitindo identificar quais times, projetos, ambientes ou aplicações estão gerando uso — e potencialmente custo.
## O que ela faz

Ela permite:

- Definir até **3 tags principais** para rateio
- Visualizar consumo agrupado por essas tags
- Gerar relatórios horários e mensais
- Exportar CSV/TSV para chargeback/showback
- Acompanhar tendências de uso ao longo do tempo

A feature trabalha principalmente com:

- métricas de uso
- volume ingerido
- hosts
- spans
- logs
- sessões RUM
- containers
- custom metrics

Ou seja:

Ela mostra **quem consumiu o quê**, mas não necessariamente o valor financeiro exato da invoice.
## Limitações importantes

Nem todo produto suporta Usage Attribution, porque são consumos não tagueáveis na instrumentação.

- Incident Management Users
- CI Pipeline Users
- Parallel Testing Slots
- Audit Trail
## API

Usage Attribution utiliza a [[API - Usage Metering]]
## Referências

https://docs.datadoghq.com/account_management/billing/usage_attribution/?utm_source=chatgpt.com

https://docs.datadoghq.com/api/latest/usage-metering/?utm_source=chatgpt.com
