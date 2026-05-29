#arquitetura_solucoes #azure #cloudcomputing #finops 

Nossa última newsletter trouxe um guia técnico de utilização de tags na alocação de recursos. Nessa mesma edição eu abordei a boa prática de se utilizar um modelo de governança híbrido, onde a alocação de custos não depende exclusivamente de tags e utiliza de maneira estratégica a hierarquia de conta que os provedores de nuvem oferecem. No caso da Azure, a hierarquia de contas segue a seguinte estrutura:

- Tenancy
- Management Groups
- Subscriptions
- Resource Groups
- Resources

O artigo de hoje abordará a utilização de Management Groups como estratégia de alocação de custos.

## O que é um Management Group?

Um Management Group é um agrupamento de Subscriptions que pertencem a um mesmo locatário do Microsoft Entra. Esse agrupamento vai além da identificação de custos, e tem como objetivo principal garantir conformidade e propagação de políticas e condições de acesso, que são herdadas em todas as Subscriptions que compõem o grupo.

Além da herança de Políticas de Acesso, os Management Groups também são utilizados para conceder a um determinado usuário permissões de acesso a um grupo de Subscriptions, sem precisar fazê-lo de forma individualizada em cada Subscription. O RBAC através de IAM pode ser configurado diretamente no Management Group, facilitando não apenas a concessão de acessos, mas também a exclusão, o que é uma boa prática de segurança.

Na prática, recursos filhos herdam as permissões de RBAC atribuídas em seus recursos pais. Se um usuário receber função de Contributor em um determinado Management Group, essa permissão será replicada em cada Subscription, Resource Group e Resource dentro deste Management Group.

![[Pasted image 20260414154522.png]]

Conforme imagem acima, é possível criar Management Groups dentro de Management Groups, gerando assim divisões cada vez mais precisas de Unidades de Negócio, até que por fim sejam atribuídas as Subscriptions aos Management Groups de último nível na hierarquia da unidade de negócios.

O uso de Management Groups também permite a gestão de logs no Azure Monitor, possibilitando pesquisar e gerenciar eventos ocorridos no grupo de gerenciamento selecionado.

![[Pasted image 20260414154545.png]]

Por fim, é importante ressaltar que a criação de Management Groups não gera qualquer custo adicional ou altera critérios de cobrança na Billing Account, uma vez que se trata apenas de um container lógico para agrupamento de Subscriptions.

## Limitações

Em primeiro lugar, **o uso de Management Groups não tem suporte para gerenciamento de custos para Subscriptions de MCA (Microsoft Customer Agreement).** Ou seja, os recursos Azure de gerenciamento de custos como o Cost Analysis, Budget e Exports do portal Azure não funcionam em nível de Management Group.

Além disso, **cada grupo de gerenciamento e Subscription pode ter suporte a apenas um pai**, ou seja, uma vez que um Management Group ou Subscription esteja atribuído à um Mangament Group dentro da Unidade de Negócios, não pode ser incluído em outro.

Quanto as outras limitações técnicas da funcionalidade, podemos listar:

- Um único diretório pode dar suporte a 10.000 Management Groups.
- Cada hierarquia no Management Group pode ter até seis níveis de profundidade.
- Todas as Subscriptions e Management Groups estão dentro de uma hierarquia principal, única, que é um Root Management Group.

Cada diretório do Microsft Entra ID possui apenas um Root Management Group, no qual toda a Hierarquia de Contas Azure será definida. É possível, inclusive, aplicar políticas globais e atribuição de funções no nível deste diretório.

## Utilizando Management Groups para Alocação de Custos

Em um modelo híbrido, Management Groups formam a primeira camada estratégica de alocação de custos, complementando as tags que fornecem granularidade adicional. **Assim, uma boa estratégia seria utilizar Management Groups para categorias de alto nível, enquanto tags agregam mais granularidade e detalhamento.**

Assim, em sede de Management Groups, creio que os dois melhores agrupamentos sejam:

- Business Unit / Department (Marketing, Finance, Sales, etc): facilita a alocação de custos relacionando todas as Subscriptions que pertençam a uma mesma unidade de negócios.
- Environment (Development, Production, Homologation, QA): uma vez que cada ambiente costuma ter regras diferentes de acesso, compliance e monitoramento.

Por outro lado, há tags que não são boas para se tornarem Management Groups:

- Owner: considerando que o responsável poderá ser alterado, ou o projeto transferido para outro time.
- Compliance: tag de auditoria, com valores variáveis.
- Application: com o crescimento do negócio e produtos lançados, poderá ensejar na criação de diversos Management Groups diferentes.

## Configurando um Management Group

No Portal Azure, pesquise por Management Group. Em seguida, clique em "**Create".**

![[Pasted image 20260414154608.png]]

Após a criação do Management Group você poderá transferir as Subscriptions necessárias. O processo é feito manualmente, clicando em **"Move"**.

![[Pasted image 20260414154619.png]]

Selecione o Management Group e clique em **"Save"**.

![[Pasted image 20260414154639.png]]

Depois de algum tempo as alterações serão realizadas com sucesso, e você já poderá ver a estrutura dos Management Groups.

![[Pasted image 20260414154651.png]]

## Bibliografia utilizada

[Organizar seus recursos com grupos de gerenciamento – Governança do Azure - Azure governance | Microsoft Learn](https://learn.microsoft.com/pt-br/azure/governance/management-groups/overview)

[Criar um grupo de gerenciamento com o portal - Azure governance | Microsoft Learn](https://learn.microsoft.com/pt-br/azure/governance/management-groups/create-management-group-portal)

[Proteger sua hierarquia de recursos – Governança do Azure - Azure governance | Microsoft Learn](https://learn.microsoft.com/pt-br/azure/governance/management-groups/how-to/protect-resource-hierarchy)