#azure #arquitetura_solucoes 

### Billing Account

Representa um Customer Agreement para múltiplos produtos e serviços.
### Billing Profile

Agrupa todas as Subscriptions incluídas numa invoice. São o equivalente ao EA Enrollment, e são o escopo onde os invoices são gerados. Compras que não são baseadas em uso (Marketplace, Reservas, etc) estão disponíveis apenas nesse escopo.

### Invoice Section

Permite agrupar as Subscriptions  com um Billing Profile dentro de sessões individuais dentro da mesma invoice. 

### Customer

Representa um grupo de Subscriptions associadas a um cliente específico de MCA de um Partner. É um escopo específico para CSPs.
## Roles utilizadas no Cost Management - MCA

### Owner

Gerencia configurações e acessos, visualiza custos e gerencia configurações de custo, budgets e exports.
### Contributor

Gerencia configurações, exceto acessos, visualiza custos e gerencia configurações de custo, budgets e exports.

### Reader

Pode visualizar configurações e dados de custo. Além de gerenciar budgets e exports.

### Invoice Manager

Pode visualizar e pagar invoices, pode visualizar dados de custo e configuração. Pode gerenciar budgets e exports.

### Azure Subscription Creator

Pode criar Subscriptions, ver custos e gerenciar configurações de custos. Também pode gerenciar budgets e alertas.
## Fonte

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-work-scopes