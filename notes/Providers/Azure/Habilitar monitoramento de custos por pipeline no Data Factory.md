#azure #cloudcomputing #data_analysis #data_governance #finops 

Essa configuração permite exibir o custo por pipeline ou factory no billing report gerado pela Azure. 

1. Acesse o portal do Azure Data Factory
2. Na guia "Gerenciar", selecione "Factory settings" na seção "General"
3. Selecione "Show billing report (preview)" na modalidade "by pipeline"
4. Publicar a alteração

![[Pasted image 20260520154549.png]]

## Limitações

A seguir estão as limitações conhecidas dos recursos de cobrança por pipeline. Esses medidores de faturamento não serão arquivados no pipeline que o gira, mas serão arquivados em um item de linha alternativo para sua fábrica.

- Cobranças de operações do Azure Data Factory, incluindo leitura/gravação e monitoramento
- Cobranças para [nós do SSIS (SQL Server Integration Services) do Azure Data Factory](https://learn.microsoft.com/pt-br/azure/data-factory/tutorial-deploy-ssis-packages-azure)
- Se você tiver [Time to Live (TTL)](https://learn.microsoft.com/pt-br/azure/data-factory/concepts-integration-runtime-performance#time-to-live) configurado para Azure Integration Runtime (Azure IR), atividades do Data Flow executadas nestes IR não serão registradas sob pipelines individuais.
## Referência

https://learn.microsoft.com/pt-br/azure/data-factory/plan-manage-costs