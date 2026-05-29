#cloud8 #finops #data_analysis 

## FinOps Analytics – Products

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-01.webp "Análise de Custos com FinOps Analytics")

O Painel do [FinOps](https://www.cloud8.com.br/ajuda/tag/finops/) Analytics por Products consolida diversos dados para gerar uma visão executiva de custos consolidados em um único painel de análise. A partir dele é possível acompanhar o custo total consolidado, média diária, projeções mensais, variações em relação ao período anterior e a distribuição de gastos por serviço. Essa abordagem transforma dados brutos de faturamento em insights acionáveis, apoiando decisões e aumentando a eficiência e governança financeira.

## FinOps Analytics – Tags / RGs / Labels

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-02.webp "Análise de Custos com FinOps Analytics")

O Painel do FinOps Analytics por [[Playbook - Tags]] / RGs / Labels consolida diversos dados para gerar uma visão executiva de custos consolidados em um único painel de análise. A diferença decorre da opção de filtrar custos não por categoria de produto, e sim por Tags. É possível filtrar tags tanto por chave, quanto por valor, trazendo níveis de detalhamento cada vez maiores. A filtragem é realizada através do menu lateral direito.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-03.webp "Análise de Custos com FinOps Analytics")

Para saber mais sobre gestão de Tags:

[[Tagged]]
[[Untagged]]
[[Criação de Tag Sintética]]
## Compreendendo os painéis do FinOps Analytics

### Painel Consolidado

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-04.webp "Análise de Custos com FinOps Analytics")

O painel consolidado traz um panorama geral de custos, com uma visão anual e de comparativo mensal. No menu lateral direito é possível aplicar diversos filtros, entre os quais a amortização dos custos, créditos e custo de marketplace, caso adote a visão de Analytics. Ao selecionar “Invoice”, os custos serão exibidos conforme demonstrados no invoice enviado pelo provedor de nuvem ao cliente.

### Painel Sumário

Traz uma visão consolidada do período dos últimos 12 meses, além de uma visão de custos diário. Além do comparativo de custos  do período atual com o anterior, esse painel também nos apresenta o Top Details, os serviços com maior custo no ambiente, seu valor atual e o valor do período anterior.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-05.webp "Análise de Custos com FinOps Analytics")

### Daily – Painel Diário

Visão detalhada de custos diários por categoria de serviço.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-06.webp "Análise de Custos com FinOps Analytics")

### Details – Painel Detalhado

Este painel apresenta a **visão detalhada dos custos**, permitindo analisar cada componente de consumo individualmente, bem como sua **variação absoluta e percentual** entre períodos. A estrutura hierárquica por serviço (como EC2, RDS, Redshift, S3 e Marketplace) possibilita identificar rapidamente os principais **drivers de custo**, distinguir modelos de cobrança (On-Demand, Spot, Savings Plans, Storage, Backup, Data Transfer) e entender o impacto de cada métrica no total consolidado. 

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-07.webp "Análise de Custos com FinOps Analytics")

É possível configurar uma série de filtros através dos quais as variações de custos possam ser avaliadas:

- Min $: filtrar apenas as linhas de consumo cuja variação em comparação ao período anterior seja maior ou igual ao valor informado. 
- Percentage variation (+/-): filtrar apenas as linhas de consumo cuja variação em comparação ao período anterior seja maior ou igual ao percentual informado.
- Show only variations: caso marcado o painel exibirá apenas as linhas onde tenha ocorrido variação de custos. Caso não seja selecionado, todas as linhas de consumo, inclusive as que não possuem variação, serão exibidas.
- Show % : caso marcado será exibida a variação percentual ao lado do valor.
- View diff.: caso marcado será exibida a diferença em valores a diferença entre os períodos.
- Levels: o nível de detalhamento das informações. Quanto maior o level, mas níveis de detalhamento de custos são exibidos.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-08.webp "Análise de Custos com FinOps Analytics")

Também é possível exportar os dados gerados clicando em “HTML/Export”. Em seguida, clique no botão “CSV”.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-09.webp "Análise de Custos com FinOps Analytics")

### Top 10 / Anomalies (veja [Gestão de Anomalias](https://www.cloud8.com.br/ajuda/relatorios-e-graficos-de-anomalias-de-custos/))

#### Top 10 Most Expensive – Estimativa

Esse painel exibe o top 10 das categorias de serviço mais caras previstas para o período. Quando referente à um mês ainda não fechado, a informação apresentada é apenas uma estimativa baseada no Forecast para o período.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-10.webp "Análise de Custos com FinOps Analytics")

#### Data (var %)

Esse painel apresenta os 10 maiores ofensores com base na variação percentual de custos. Trata-se de uma visão resumida que permite uma identificação rápida dos ofensores. 

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-11.webp "Análise de Custos com FinOps Analytics")

#### Heatmap

O **heatmap** (mapa de calor) é uma visualização analítica que facilita a identificação rápida de **variações de custo ao longo do tempo**, destacando **tendências, picos e comportamentos anômalos** sem a necessidade de analisar números linha a linha.

![Análise de Custos com FinOps Analytics](https://www.cloud8.com.br/wp-content/uploads/2026/01/finops-analytics-12.webp "Análise de Custos com FinOps Analytics")

Como ler este heatmap do painel:

- **Linhas**: representam os serviços ou agrupamentos de custo.
- **Colunas**: representam os períodos, organizados cronologicamente.
- **Cores**: indicam a **variação percentual do custo** em relação ao período anterior:

- ==**Tons de vermelho** → aumento de custo (quanto mais intenso, maior o aumento).==
- ==**Tons de azul** → redução de custo.==
- **Tons claros / brancos** → estabilidade ou variação próxima de zero.
- ==**Preto** → ausência de custo ou dado não aplicável naquele período.==

O que esse heatmap permite identificar:

- **Serviços com crescimento recorrente de custo**, quando aparecem com vários blocos vermelhos consecutivos.
- **Efeitos de otimizações ou mudanças arquiteturais**, visíveis como transições de vermelho para azul.
- **Anomalias financeiras**, quando há um vermelho intenso isolado em um mês específico.
- **Sazonalidade**, ao observar padrões que se repetem em determinados períodos.
- **Impacto no custo total**, comparando a linha “Total” com os serviços individuais.

## Conclusão

Os painéis do **[FinOps](https://www.cloud8.com.br/ajuda/tag/finops/) Analytics** consolidam dados complexos de faturamento em visões claras para apoiar a tomada de decisão, permitindo que áreas técnicas, financeiras e de negócio compartilhem uma mesma leitura sobre os custos em nuvem. Ao combinar análises por **Products** e por **Tags / RGs / Labels**, a plataforma viabiliza tanto uma visão macro do consumo quanto um detalhamento granular por responsabilidade, aplicação ou centro de custo.

Dessa forma, o FinOps Analytics deixa de ser apenas uma ferramenta de reporte e passa a atuar como um **instrumento estratégico de governança financeira**, sustentando práticas de controle de custos, previsibilidade orçamentária, accountability e melhoria contínua da eficiência em nuvem.