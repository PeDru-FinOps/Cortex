#cloud8 #data_analysis #finops #cloudcomputing #data_governance 

## Visão Geral

A capacidade de visualizar dados de custos precisos e gerar relatórios é um dos pilares de uma prática de FinOps de sucesso. Ambientes multicloud se tornam difíceis de administrar em decorrência dos dados virem de múltiplas fontes, com nomes de coluna heterogêneas para tratar da mesma informação. Muitas vezes a análise de dados de custo demanda um trabalho complexo de normalização de dados para geração de um relatório minimamente funcional.

Na Cloud8 permitimos que o usuário tenha total controle dos filtros e exibição dos seus dados de custo através da funcionalidade “_**Dashboards**_”. Através dela é possível filtrar, exibir e exportar informações utilizando tabela dinâmica com dados exportados diretamente no provedor de serviços de nuvem. Assim, o usuário final fica responsável exclusivamente por determinar quais informações serão exibidas.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-01.webp "FinOps Dashboards Cloud8")

Ao clicar em “**FinOps – Reports**” no menu lateral esquerdo um expander irá exibir diversas funcionalidades, entre elas a “**Dashboards**”. Ao clicar, o usuário terá acesso à uma tabela dinâmica diretamente integrada com os providers cadastrados no sistema da Cloud8.

## Compreendendo a interface do Dashboards

O Dashboards foi desenvolvido para permitir ao usuário manipular dados através de um sistema _Drag-and-Drop_, dispensando a memorização e utilização de qualquer sistema de querys, tais quais o SQL, KQL e afins. Os blocos podem ser selecionados e reorganizados de acordo com as necessidades do usuário.

Esse sistema permite que os dados sejam manipulados tanto por usuários técnicos quanto por outros perfis de usuários, como executivo e financeiro, para dar visibilidade de custos atrelados à regras e unidades de negócio previamente definidas sem a necessidade de conhecimento de linguagens de consulta. O sistema utiliza as seguintes opções:

### All Fields

Exibe todos os widgets que podem ser utilizados para gerar as tabelas dinâmicas.

- **Cost**: informação de custo;
- **Provider**: provedores cadastrados no sistema da Cloud8;
- **Product**: o tipo de produto (Virtual Machines, EKS, Redis, etc)
- **Product details**: o tipo de cobrança vinculada a um recurso (Storage, Data Tansfer, etc)
- **Usage type group**: informações como a SKU dos recursos;
- **Region**: região do recurso;
- **Component ID**: ID do recurso;
- **Component name**: nome do recurso.

### Row labels e Column labels

Através do sistema de _Drag-and-Drop_, os widgets arrastados do _All Fields_ para _Row_ e _Column_ serão exibidos respectivamente como linha ou coluna da tabela dinâmica. A ordem de exibição das informações segue a ordem dos blocos, da esquerda para direita. No exemplo abaixo uma visualização foi gerada com base no tipo de produto, exibindo os custos de cada _provider_.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-02.webp "FinOps Dashboards Cloud8")

Caso o usuário deseje organizar os custos por _provider_ e exibir os custos por cada tipo de produto, basta arrastar o bloco “**Provider**” para frente do bloco “**Product**”.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-03.webp "FinOps Dashboards Cloud8")

### Values

Através do sistema de _Drag-and-Drop_, os widgets arrastados do _All Fields_ para _Values_ serão exibidos em uma coluna de valor, que pode ser configurada para exibir a soma ou a contagem. Para alterar a configuração, clique em cima do widget e selecione “**Field settings**”

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-04.webp "FinOps Dashboards Cloud8")

Em “**Summarize by**” selecione “**Count**” ou “**Sum**”. Em seguida, clique em “OK”.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-05.webp "FinOps Dashboards Cloud8")

### Chart

Os dados selecionados no Dashboards podem ser visualizados no formato de gráfico, clicando em “**Chart**” na parte inferior da tela.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-06.webp "FinOps Dashboards Cloud8")

Os gráficos podem ser configurados clicando em “**Series Type**”, sendo possível selecionar entre as opções abaixo:

- **Column**
- **Stacked Column**
- **Bar**
- **Stacked Bar**
- **Line**
- **Area**
- **Bubble**
- **Scatter**
- **Pie**

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-07.webp "FinOps Dashboards Cloud8")

Também é possível exportar o gráfico clicando na opção _Export_; e imprimi-lo clicando em “**Print**”. Por fim, é possível expandir o gráfico para analisá-lo de forma mais detalhada, clicando em “**Fullscreen**”.

### Filtros e opções adicionais

No topo da tela existem diversos filtros e opções adicionais que permitem melhorar o desempenho na utilização do painel do _Dashboards_. Essas opções permitem selecionar escopos de carregamento de dados com base nos _Providers_ cadastrados, e mesmo em _Tags_ que estejam configuradas no ambiente.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-08.webp "FinOps Dashboards Cloud8")

**1 – Seletor de Provider:** permite selecionar um _Provider_ ou _Business Unit_ para carregar os dados no _Dashboards_.

**2 – Currency:** permite selecionar a Moeda no qual os valores serão apresentados no painel.

**3 – +Tags / RGs:** permite selecionar _Tags_ e _Resource Groups_ como filtros na geração do _Dashboard_.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-09.webp "FinOps Dashboards Cloud8")

Conferir em:

[[Utilizando Tags na Cloud8]]
[[FinOps Tags]]

**4 – Dynamic:** selecionar essa opções faz com que os dados sejam carregados automaticamente, logo que um widget é arrastado para uma determinada posição, sem a necessidade de clicar em “**Refresh**”. Além disso, essa opção habilita as seguintes opções de filtro:

- **Day**: visão de custos diária.
- **Component ID**: ID do recurso.
- **Component Name**: nome do recurso.
- **Week**: visão de custos semanais.
- **Quantity**: quantidade de elementos catalogados de acordo com um filtro aplicado.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-10.webp "FinOps Dashboards Cloud8")

**5 – Filter:** essa opção permanece bloqueada fora do modo “**Dynamic**”. Permite selecionar um período de tempo específico.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-11.webp "FinOps Dashboards Cloud8")

**6 – Refresh:** recarregar os dados manualmente para aplicar alguma alteração de campos e filtros. Embora o modo Dynamic execute o carregamento automaticamente, o usuário também poderá realizar essa ação.

**7 – Export:** Permite exportar os dados em diversos formatos, para utilização em ferramenta de terceiros.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-12.webp "FinOps Dashboards Cloud8")

**8 – Settings:** Permite configurar algumas opções de exibição de dados, como formato da tabela dinâmica, posição de linhas e colunas.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-13.webp "FinOps Dashboards Cloud8")

**9 – Expand All:** em regra, as informações da tabela dinâmica do _Dashboards_ são exibidas de forma compactada.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-14.webp "FinOps Dashboards Cloud8")

Caso o usuário deseje expandir um campo para ver mais detalhes, deverá clicar no ícone do “+” ao lado do nome do campo, como no exemplo acima. Caso o usuário deseje ver os custos dos produtos de um _Provider_ específico, deverá expandir a visualização de linhas.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-15.webp "FinOps Dashboards Cloud8")

A opção “**Expand All**” permite que o usuário expanda a visualização de todas as linhas de uma única vez.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-16.webp "FinOps Dashboards Cloud8")

**10 – Tabular View:** permite a visualização dos dados no formato de tabela. Na prática,os valores exibidos serão apenas o do último filtro aplicado.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-17.webp "FinOps Dashboards Cloud8")

Compare o resultado acima com o gerado pela opção “**Expand All**”. Em “**Tabular View**” apenas a soma do último filtro “**Product**” é exibido, mantendo o foco no custo por produto. Já em “**Expand All**” são exibidos tanto o custo total por _Provider_, quanto o custo total por _Product_, em linhas separadas.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-16.webp "FinOps Dashboards Cloud8")

**11 – Reset:** utilizado para limpar todos os filtros e configurações aplicados, retornando os dados para sua visualização original.

## Configurando Dashboards para consultas posteriores

A Cloud8 permite que uma visualização de _Dashboard_ criada seja salva para consultas posteriores. Em cenários com diversas unidades de negócios, times, ou mesmo para garantir que usuários com perfis diferentes (Financeiro, Técnico, Executivo, etc) vejam apenas os dados que lhe sejam pertinentes, os Dashboards gerados podem ser salvos para consulta posterior, sem a necessidade de reconfigurar todos os campos e filtros aplicados.

Após configurar a exibição de dados desejada, clique em “**My Dashboards**”, no canto superior esquerdo do painel. Selecione “**Save New**”.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-18.webp "FinOps Dashboards Cloud8")

Na tela seguinte, defina um nome para o _Dashboard_ criado, e clique no checkbox “**Share with all users**” caso deseje que o painel salvo também possa ser visualizado por outros usuários do Cloud8.

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-19.webp "FinOps Dashboards Cloud8")

O usuário poderá exportar o resultado do _Dashboards_ no formato CSV para um _storage_, como **Blob Storage** (Azure), **Bucket S3** (Azure) e **BigQuery** (GCP). Basta selecionar a opção “**Export as CSV**”. Fonte: [[Como integrar e exportar dados da Cloud8 para Storages Cloud]]

![FinOps Dashboards Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-dashboards-20.webp "FinOps Dashboards Cloud8")

Você poderá selecionar as opções de incluir uma coluna para frequência diária, e uma para número da semana, clicando nas suas respectivas checkboxes. Defina um nome para o arquivo exportado, e selecione o _Storage_ onde o arquivo será salvo.

**OBS:** A configuração do Storage é realizada em Integrations, no menu lateral esquerdo.

Selecione o formato das casas decimais, o separador do CSV e em seguida clique em “**Save**”. Após essa configuração os dashboards salvos passarão a ser exportados automaticamente para o Storage selecionado, permitindo que o usuário possa integrar esses dados com ferramentas de BI e afins.