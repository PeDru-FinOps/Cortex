#datadog #management #cloudcomputing 

É possível gerenciar várias organizações filhas a partir de uma única conta da organização principal. Isso geralmente é usado por provedores de serviços gerenciados que possuem clientes que não devem ter acesso aos dados uns dos outros.

O recurso de conta multi-organização não está habilitado por padrão. Entre em contato com o suporte da Datadog para habilitá-lo.
## Capacidades

- Os usuários podem ser adicionados à organização principal e a várias organizações filhas. Os usuários podem alternar entre organizações no menu de configurações da conta do usuário.
- Organizações dentro de uma organização principal não têm acesso aos dados umas das outras. Para habilitar consultas de métricas entre organizações, consulte a seção sobre visibilidade entre organizações.
- A organização principal pode visualizar o uso de cada organização filha individualmente, permitindo que a organização principal acompanhe as tendências de uso.
- As configurações da conta, como endereços IP permitidos, não são herdadas pelas organizações filhas da organização principal.
## Multi-Org usage

A organização matriz pode visualizar o uso total e faturável de todas as suas organizações (filiais e matriz) passando o cursor sobre o nome de usuário no canto inferior esquerdo e navegando até [**Plan & Usage** > **Usage & Cost**](https://app.datadoghq.com/billing/usage?cost_summary).

A página Usage mostra o uso agregado da organização matriz e de todas as suas filiais. Há duas abas na página Uso:

- Geral
- Organizações Individuais
## Usage attribution

A organização principal pode visualizar o uso das organizações filhas por meio de chaves de tags existentes na página **Usage Attribution**. Os administradores podem passar o cursor sobre o nome de usuário no canto inferior esquerdo e navegar até: [**Plan & Usage** > **Usage & Cost**](https://app.datadoghq.com/billing/usage?cost_summary).

Quando habilitada no nível da organização principal, a atribuição de uso mostra o uso agregado em todas as organizações. Isso pode ser útil se você quiser atribuir o uso de suas organizações filhas a determinados projetos, equipes ou outros agrupamentos.

As funcionalidades incluem:

- Alterar e adicionar novas chaves de tags (até três).
- Acessar o uso mensal tanto na interface do usuário quanto em um arquivo .tsv (valores separados por tabulação) baixado.
- Acessar o uso diário em um arquivo .tsv para a maioria dos tipos de uso.
## Referências

https://docs.datadoghq.com/account_management/multi_organization/
https://docs.datadoghq.com/account_management/org_settings/cross_org_visibility/
https://docs.datadoghq.com/account_management/org_settings/cross_org_visibility/#configure-connections
https://docs.datadoghq.com/account_management/plan_and_usage/cost_details/