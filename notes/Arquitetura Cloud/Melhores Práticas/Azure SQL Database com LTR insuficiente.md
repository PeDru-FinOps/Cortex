#azure #cloudcomputing #data_governance #bestpractices

Essa boa prática recomenda verificar se há bancos de dados no Azure SQL com retenção de backups de longo prazo (LTR – _Long-Term Retention_) insuficiente.

Por padrão, o alerta foca em bancos que estão com a retenção semanal configurada como 0 dias — ou seja, não estão armazenando backups de longo prazo.

A recomendação é configurar a retenção de backups completos (full backups) do Azure SQL Database ou Azure SQL Managed Instance para armazenamento em Blob Storage, com redundância adequada, permitindo guardar esses backups por até 10 anos.

**Resumo curto:**  
Garanta que o LTR esteja configurado (especialmente retenção semanal > 0) para manter backups de longo prazo e atender requisitos de recuperação e conformidade.
## Referências

https://learn.microsoft.com/en-us/azure/azure-sql/database/long-term-retention-overview?view=azuresql
## Conexões aprovadas pela Hunnigan
- [[Azure]]
## Tags aprovadas pela Hunnigan
- #governance
