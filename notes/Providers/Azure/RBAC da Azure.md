#azure #arquitetura_solucoes 
## Organização de Recursos

Na [[Azure]] a Organização de recursos é importante para uma melhor alocação de custos e projetos. Além disso, permite uma gestão mais granular de IAM e Policies e herança de Tags. 

![[Pasted image 20260330154742.png]]

## Role Based Access Control

O controle de acesso baseado em regras é utilizado para gerenciar acessos  e governança de recursos na Azure, inclusive ao painel do [[Cost Management Azure]].

- Subscriptions: containers de Recursos Azure.
- Resource Groups: agrupamentos lógicos de recursos que compõem uma mesma solução e partilham o mesmo ciclo de vida.
- Management Groups: organizam subscriptions em hierarquias e suportam até seis níveis de profundidade, sem incluir o root level.

## Roles

- Owner: acesso total aos dados de custo e configurações de custo.
- Contributor: acesso total aos dados de custo e configurações de custo, com exceção do controle de acesso.
- Reader: acesso somente leitura aos dados de custo.
- Cost Management Contributor: acesso total aos dados de custo, configurações e recomendações.
- Cost Management Viewer: acesso de leitura ao Cost Management e recomendações.

![[Pasted image 20260330174221.png]]

Conforme descrito nas [[Melhores Práticas de Azure]], Cost Management Contributor atende ao requisito do mínimo privilégio.  Cenários mais complexos podem demandar Roles adicionais como:

- Monitoring Reader:  se for necessário o uso de métricas detalhadas como logs e contadores de performance do Azure Monitor.
- Monitoring Contributor: : se for necessário reagir a Budgets excedidos seria necessário a role para criar e executar Action Groups usados para disparar alertas e automações.
- Storage Account Contributor: para exportar dados para uma Storage Account.

## Comportamento de cada Role

![[Pasted image 20260330175144.png]]
## Fontes

https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org

https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/view-all-accounts

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-work-scopes