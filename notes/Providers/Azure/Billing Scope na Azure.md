#azure #arquitetura_solucoes 
Uma Billing Account é criada no momento em que a empresa/usuário se cadastra na Azure. É usada para gerenciar invoices, pagamentos e monitorar custos. Um usuário pode ter acesso a múltiplas Billing Accounts.

Um usuário também pode acessar o billing através do Enterprise Agreement ou Microsoft Customer Agreement.

## Tipos de Billing Account

***Microsoft Online Services Program*** é criada através do [[Azure]] website nas modalidades:

- Azure Free Account
- Account Pay-as-you-go
- Visual Studio Subscriber

Nesse tipo de account só pode haver no máximo cinco subscriptions, e subscriptions transferidas para uma nova billing account não contam para esse limite.

A criação de contas desse tipo é um ato discricionário da Microsoft, baseado no histórico do usuário com a Azure.

![[Pasted image 20260330170149.png]]

***Enterprise Agreement*** é criada quando uma empresa assina um Enterprise Agreement para utilizar a Azure. Em RA enrollment pode conter um número ilimitado de EA Accounts.

O número máximo de Subscriptions por EA Account é 5.000. É interessante não usar subscriptions para implementar limites de acesso, conforme descrito no [[Melhores Práticas de Azure]] e no [[RBAC da Azure]].

![[Pasted image 20260330170204.png]]

Em EA é possível criar Departments, um agrupamento opcional de Accounts e Subscriptions para segmentar custos e estabelecer orçamentos.

Accounts representam Account Owners que tem permissão para criar e gerenciar Subscriptions.

Mais detalhes estão presentes no [[Billing Scope do Enterprise Agreement]]

Para configurar acessos, conferir [[Roles para Enterprise Agreement]]

***Microsoft Customer Agreement (MCA)*** é criado quando uma empresa trabalha com um representante da Microsoft para assinar MCAs. 

Nesse tipo de account só pode haver no máximo cinco subscriptions, e subscriptions transferidas para uma nova billing account não contam para esse limite.

A criação de contas desse tipo é um ato discricionário da Microsoft, baseado no histórico do usuário com a Azure.

Um MCA pode ter até 10.000 Subscriptions.

![[Pasted image 20260330170451.png]]

Um Billing Profille representa um invoice e suas informações como método de pagamentos. Um billing profile pode ter mais de um Invoice Section.

Invoice Section representa um agrupamento de custos no invoice.

Mais detalhes estão presentes no [[Billing Scope do Microsoft Customer Agreement]]

Para configurar acessos, conferir [[Roles para Microsoft Customer Agreement]]

***Microsoft Partner Agreement*** é criado para parceiros Cloud Solution Providers (CSP) gerenciarem seus clientes. 

Um Partner Billing Account pode ter até 10.000 Subscriptions.

![[Pasted image 20260330170722.png]]

Um Billing Profille representa um invoice e suas informações como Currency. Um billing profile pode ter mais de um Customer.

Customer representam os clientes de um CSP, e agrupam Subscriptions e custos de Azure Marketplace. 

Um Customer pode ter um Reseller associado, que é um revendedor da Microsoft, como um CSP Two-Tier.

Mais detalhes estão presentes no [[Billing Scope do Cloud Solution Provider]]

Para configurar acessos, conferir [[Roles para Cloud Solution Provider]]
## Fontes

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-work-scopes

https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/view-all-accounts