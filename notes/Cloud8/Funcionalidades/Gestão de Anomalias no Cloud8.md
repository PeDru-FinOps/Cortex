#cloud8 #finops 

Este tutorial orienta você a configurar uma regra para detecção de anomalias de custos em sua plataforma Cloud8. Com essa funcionalidade, você pode identificar desvios significativos nos gastos de forma automática, evitando surpresas financeiras e mantendo o controle sobre o orçamento. Além de criar uma regra personalizada, você verá como acessar os relatórios e gráficos gerados, que fornecem uma visão detalhada do uso e dos custos em toda a sua infraestrutura.

## O que é gestão de anomalias?

Compreender uso e custo da infraestrutura de uma aplicação ou produto é extremamente importante em uma estratégia de FinOps que visa manter os custos efetivos para a manutenção das operações, minimizando os impactos no negócio.

Assim, torna-se extremamente importante detectar, alertar e gerenciar custos inesperados e irregularidades de uso que comprometam o orçamento das operações. Chamamos esta capacidade de Gestão de Anomalias.

As anomalias são níveis de gastos que são considerados diferentes da média histórica ou variação esperada. Assim, é possível que uma empresa adote uma regra orçamentária que preveja uma variação mensal de até 10% em comparação ao período anterior, que decorra de fatores externos ou variações de consumo de recursos.

Através da funcionalidade de gestão de anomalias da Cloud8 é possível detectar gastos irregulares à nível de Provedor, Unidade de Negócios ou Produto, permitindo que o usuário reaja imediatamente quando uma anomalia ocorrer.

## Configurando uma nova detecção de anomalias

Para configurar uma nova detecção de anomalias, clique em “Rules”no topo da página, e em seguida clique em “New”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-01.webp "Gestão de anomalias Cloud8")

Em “View cost as” defina a visão de Markup que será utilizada, e em “Currency” se a anomalia será baseada nos custos em dólar ou real.

Em “Name” defina um nome para regra de anomalia. Sugerimos que o nome adotado seja o mais claro possível quanto à regra que está sendo implementada.

Em “Context” selecione o provider ou unidade de negócio. Marque a checkbox de Total caso deseje que a anomalia considere os custos totais, ou a checkbox de “Products” caso deseje criar uma regra de anomalia específica para um produto. Exemplo de uso: criar uma regra de anomalia para monitorar os custos com recursos de IA no ambiente de desenvolvimento. 

No painel de “Settings” selecione o percentual mínimo a ser considerado como anomalia. Portanto, se a regra de negócio leva em consideração uma variação de custos de até 10%, configure o percentual mínimo como 11%. 

É possível também validar um valor mínimo de custo a ser considerado como anomalia, com vista a evitar falsos positivos em hipóteses onde o aumento percentual é alto, ainda que o custo seja baixo. Podemos utilizar como exemplo a configuração de uma regra de anomalias de 11%, onde ocorre o aumento nos custos com IP. Na hipótese, o recurso custava R$ 5,00 e ocorre o aumento de R$1,00. Neste caso haveria um alerta de anomalias, já que esse aumento, embora irrisório, alcança o percentual de 20%, ultrapassando a regra de tolerância de variação.

Para evitar ser alertado de anomalias de valor irrisório defina um valor real em “Min value”, que atuará em conjunto ao percentual definido. O “Min value” só será considerado anomalia se o valor definido representar o percentual mínimo configurado. Exemplo: Se o “Min value” for configurado como R$10.000,00; em um cenário onde o custo anterior foi R$120.000,00 e o custo atual for R$130.000,00, a variação percentual será de 8,33%. Logo, não será considerada uma anomalia de custos.

Em “Pattern Checkings” selecione a granularidade de análise de anomalias, podendo ser: Diária, 7 dias (Semanal) e Mensal. A mesma regra de anomalias pode levar em consideração mais de um período, sendo possível definir um percentual de anomalia diária, semanal e mensal na mesma regra, trazendo níveis cada vez maiores de controle de gastos.

Em “Exceptions” é possível definir exceções levando em consideração diferenças de consumo que ocorrem durante finais de semana. É possível que um determinado job de backup integral seja realizado semanalmente aos sábados, representando um evidente aumento nos custos de backup, o que já é esperado na regra de negócio. Da mesma forma, o custo de um ambiente ao domingo, quando parte das aplicações de produção podem não tem o mesmo nível de consumo e acesso, ao serem utilizadas na segunda-feira geram um aumento esperado no custo diário. Nestas hipóteses, é viável configurar regras de exceção no trigger da anomalia.

Caso deseje uma visão imediata das anomalias que possam ser identificadas após a configuração, selecione o checkbox “Run now” para realizar a primeira execução da busca de anomalias logo após a criação da regra.

Feita a configuração, clique em “Save”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-02.webp "Gestão de anomalias Cloud8")

## Video passo a passo

## Deletando uma regra de anomalia

Para deletar uma regra de anomalia criada, clique em “Rules”. Selecione a regra e clique em “Delete”. Para deletar as anomalias que tenham sido detectadas de acordo com a regra que será deletada, selecione o checkbox de “Remove anomalies linked to this rule”. Para concluir, clique em “Remove”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-03.webp "Gestão de anomalias Cloud8")

## Avaliando Anomalias

Após configurar uma anomalia, ela ficará disponível para visualização no painel da Cloud8, ao clicar em “Rules”. Ao selecionar uma regra de anomalia configurada é possível executá-la manualmente clicando em “Run now”; ou editá-la clicando em “Edit”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-04.webp "Gestão de anomalias Cloud8")

Ao selecionar “FinOps – Anomalies” no menu lateral esquerdo, todas as anomalias identificadas serão listadas na tela. Para analisar uma anomalia, clique no ícone de “Graph” e o usuário será direcionado para a funcionalidade do FinOps – Analytics, onde poderá identificar o fato gerador da anomalia.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-05.webp "Gestão de anomalias Cloud8")

Também é possível exportar a listagem de anomalias identificadas em um determinado período clicando no ícone da opção “Download data in CSV format” no canto superior direito.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-06.webp "Gestão de anomalias Cloud8")

## Documentando anomalias

É possível documentar anomalias clicando no ícone de “Document”. Essa funcionalidade permite gerar um documento de report da anomalia, categorizando-a e acompanhando-a .

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-07.webp "Gestão de anomalias Cloud8")

Após a configuração da documentação da anomalia, é possível fazer registros do incidente, selecionando a anomalia e clicando novamente no ícone de “Document”, alterando as informações conforme o incidente seja avaliado pelo usuário.

Essa funcionalidade permite identificar rapidamente as anomalias que não foram validadas, pois todo registro documentado é apresentado com um ícone na listagem.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-08.webp "Gestão de anomalias Cloud8")

Por fim, é possível exportar os incidentes documentados, facilitando a auditoria e criação de KPIs de resolução de incidentes. Basta clicar no ícone no canto superior direito da tela, selecionar o período que deseja exportar e clicar em “Download data in CSV format”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-09.webp "Gestão de anomalias Cloud8")

## Deletando registros de anomalia

É possível deletar uma registro de anomalia selecionando-a e clicando em “Delete”, no topo da tela. Em seguida, confirme clicando em “Destroy”.

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-10.webp "Gestão de anomalias Cloud8")

Para deletar todos os registros, basta clicar em “Delete all” no topo da tela. Em seguida, confirme clicando em “Delete all”.  

![Gestão de anomalias Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/12/anomalias-11.webp "Gestão de anomalias Cloud8")