#cloud8 

A funcionalidade de Inventário permite ao usuário consultar o catálogo de recursos que compõem a sua infraestrutura de cloud. No menu lateral esquerdo, clique em **FinOps - Reports**, e em seguida **Inventory**. 

Importante informar que apenas recursos que tenham gerado algum tipo de custo serão listados nesta funcionalidade.

## Definindo o período de avaliação

O usuário poderá selecionar o período para que a listagem de recursos seja exibida. Esta configuração permite identificar todos os recursos que compuseram o ambiente cloud dentro de uma janela de tempo específica. Caso o usuário selecione os últimos meses, terá uma visão de todos os seus recursos atuais; porém se selecionar uma janela de tempo anterior, terá uma visão histórica da infraestrutura, permitindo identificar recursos excluídos e alterações na infraestrutura.

## Definindo os produtos da avaliação

O usuário poderá selecionar todos os recursos de um Provider específico, Unidade de Negócios ou Tier II configurado, selecionando-o em **Product**.

![[Pasted image 20260504153323.png]]

Também é possível selecionar Produtos específicos, clicando no Checkbox daqueles que deseja catalogar. Essa configuração permite selecionar mais de um tipo de Produto.

![[Pasted image 20260504153441.png]]

É possível especificar ainda mais, selecionando um tipo específico dentro de uma categoria de Produto.

![[Pasted image 20260504153558.png]]

Em seguida, clique em **Load** para gerar a listagem.
## Tipos de Relatório

### Detalhado

Exibirá um painel com as informações completas de Produto, Tipo de Produto, nome do componente, Detalhes, entre outras informações.

![[Pasted image 20260504153809.png]]

É possível configurar essa visualização de acordo com o opção **Group**, agrupando por:

- Provider
- Product
- SKU/Type
- Component
- Region
- Resource Group
- Compartment 
### Grouped by ID + history

Exibirá um painel focado em apresentar a variação de custos de um determinado recurso dentro do Período definido pelo usuário. Esse painel permite que o usuário foque em listar recursos que tiveram variação de custos, configurando um valor definido e/ou um determinado percentual de variação.

![[Pasted image 20260504154405.png]]

- Min $: Define um valor numérico de variação, listando todos os recursos que tenham variado X ou mais dentro do Período.
- Percentage variation (+/-): o percentual de aumento ou redução a ser considerado dentro do Período.
- Show only variations: ao selecionar, exibirá apenas os níveis de recurso onde a variação tiver ocorrido.
- Show %: exibe o percentual de variação na visualização.
- View diff.: exibe a diferença a maior ou menor entre os meses do período definido, ou entre o período atual e o mês anterior.

Esse tipo de visualização permite a configuração de **Levels** de visualização. **All levels** apresentará as informações com o maior nível de detalhamento, descendo até o Resource ID do recurso responsável pela variação de custos. Cada nível tem um escopo diferente:

- Level 1: exibe apenas o Provider
- Level 2: exibe a Subscription (Azure) ou Region (AWS e GCP)
- Level 3: exibe o tipo de Produto
- Level 4: exibe o nome do componente
- Level 5: exibe detalhes do tipo de uso do componente

### Summarized and consolidated (only itens)

Exibirá um painel com a quantidade de recursos de um determinado Produto dentro do Período especificado. Esse tipo de visualização permite inventariar a quantidade total de recursos de forma simples.

![[Pasted image 20260504155742.png]]
