#azure #arquitetura_solucoes 

### Billing Account

Representa um EA Enrollment, e é o escopo onde as invoices são geradas. Todas as compras e cobranças de uso ficam disponíveis na modalidade Actual e Amortized. 

- Actual inclui todas as cobranças de Azure, Marketplace e Microsoft 365. Nesta view os custos cobertos por um commitment aparecem zerados e cada commitment adquirido é exibido.
- Amortized inclui todas as cobranças de Azure, Marketplace e Microsoft 365, porém commitments não aparecem diretamente se tiverem sido utilizados. A própria Microsoft informa que Amortized não vai bater com o invoice, pois é calculado com base na alocação e não no montante billado.

### Department

Agrupamento opcional que permite acompanhar cobranças de uso. Marketplace e Commitments não estão disponíveis nesse nível de visualização.

### Enrollment Account

Representa uma simples conta, e possui um Account Owner. Marketplace e Commitments não estão disponíveis nesse nível de visualização.

## Roles utilizadas no Cost Management - Billing Account

### Enterprise Admin

Pode visualizar todos os dados de custos. Pode gerenciar configurações de billing account e controlar quem visualiza detalhes de custos, habilitando Account Owners e Department Admins para ver as cobranças. 

### Enterprise Admin Read-Only

Pode visualizar billing account settings, dados de custo, configurações, porém não pode modificar nada. Pode gerenciar budgets e exports.

## Roles utilizadas no Cost Management - Billing Account

### Department Admin 

Pode visualizar todos os custos quando "DA view charges" estiver habilitado na billing account. Pode gerenciar configurações de Department, gerenciar budgets e exports.

### Department Admin Read-Only

Pode visualizar configurações de Department, dados de custo e configurações de custo. Pode gerenciar budgets e exports.
## Fonte

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-work-scopes