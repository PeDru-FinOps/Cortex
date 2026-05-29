#cloud8 #finops #data_analysis #governance #cloudcomputing #oci #aws #azure #gcp 

A ferramenta Cloud8 permite ao usuário unificar e simplificar a gestão de orçamentos empresariais através da unificação de diversos provedores em uma única view simplificada. Embora os provedores de serviço de nuvem ofereçam funcionalidades de Budget nativa, as mesmas podem se tornar ineficientes em contextos multicloud, considerando a necessidade de criar orçamentos distintos, em portais distintos, resultando em um número crescente de regras para serem administradas.

## Passo 1 – Acessando a Gestão de Budgets da Cloud8

No menu lateral esquerdo, selecione FinOps Reports, e em seguida Budgets. Clique em Novo, e um modelo de budget em branco será criado para edição. Cada campo representado por uma coluna precisa ser selecionado e preenchido.

## Passo 2 – Configurando o Budget

### Nome

O nome que será dado ao budget. Uma boa prática a ser adotada é dar nomes que deixem bem clara a função do budget que ele representa, os provedores configurados, unidades de negócio e método de agrupamento definido (Tags, Invoice ou Produto).

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-01.webp "Configurando Budgets no Cloud8")

### Budgets – Itens

Configuração dos provedores atribuídos ao budget. Ao clicar no campo, todos os provedores cadastrados serão exibidos.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-02.webp "Configurando Budgets no Cloud8")

Atualmente há 3 (três) métodos de Budget implementados na ferramenta Cloud8: Organização – Invoice; Organização – Produtos; Organização – Tags.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-03.webp "Configurando Budgets no Cloud8")

1. Organização – Invoice (BETA) – Essa configuração de budget realiza o monitoramento do orçamento através do Invoice gerado pelos provedores. Em cenários onde unidades de negócio, aplicações e produtos estão devidamente separados por Billing Profile (Azure), Billing Account (AWS), Payer Account (GCP e Huawei).

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-04.webp "Configurando Budgets no Cloud8")

2. Organização – Produtos (Técnico) – Essa configuração de budget realiza o monitoramento do orçamento através de categorias de serviço oferecidos no provedor. É possível especificar quais produtos você deseja monitorar dentro do orçamento definido, sendo recomendado para cenários como o de novas implementações e produtos (Ex: Uma PoC de utilização de recursos de Inteligência Artificial, onde você pode estipular um orçamento para evitar que os custos ultrapassem valores razoáveis).

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-05.webp "Configurando Budgets no Cloud8")

3. Organização – Tags (Negócios) – Essa configuração de budget realiza o monitoramento do orçamento através de metadados e seus respectivos valores, permitindo maior controle de budgets à nível de negócios.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-06.webp "Configurando Budgets no Cloud8")

### Moeda

Defina a moeda que será considerada no acionamento do trigger, impactando diretamente em cenários onde o provedor realiza o faturamento em moeda específica (como no caso da AWS, que fatura em USD), ou contratos que não possuem taxa de câmbio fixo.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-07.webp "Configurando Budgets no Cloud8")

### Método

A ferramenta Cloud8 possui diversos métodos de acionamento para monitorar estouro de orçamento.

**Estimativa mensal e Custo fixo mensal**: 

No caso de haver custos pré-definidos e/ou estimados, selecione **Estimativa Mensal** ou **Custo fixo mensal.** Em seguida, preencha cada mês do período do Budget com o valor do orçamento específico para aquele mês. O lançamento dos valores é feito manualmente, tendo em vista a possibilidade de se atribuir orçamentos diferentes para meses diversos.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-08.webp "Configurando Budgets no Cloud8")

**Custo fixo diário**: 

Para um nível de controle ainda maior, é possível atribuir um orçamento diário, selecionando **Custo fixo diário.** Em seguida, preencha cada mês do período do Budget com o valor do orçamento específico para aquele mês. O lançamento dos valores é feito manualmente, tendo em vista a possibilidade de se atribuir orçamentos diferentes para meses diversos.

**Custo fixo anual BETA**: 

No caso de orçamentos anuais, selecione **Custo fixo anual BETA**. Em seguida, preencha o Budget com o custo total do período, data de início do orçamento, vigência em anos e método de preenchimento, que poderá ser:

1. **Completar com valores mensais consumidos e dividir sobra**: para cenários onde os custos mensais poderão variar, porém o orçamento de todo o período está definido, e o escopo do projeto deverá ser ajustado ao saldo remanescente.

2. **Proporcional – dividir pelo número de meses**: para cenários onde há um custo médio definido, e as variações mensais permitem a identificação de anomalias de consumo e insights sobre crescimento de custos e ambiente.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-09.webp "Configurando Budgets no Cloud8")

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-10.webp "Configurando Budgets no Cloud8")

**% Custo fixo do mês anterior**

No caso de haver uma margem de tolerância de variação de custos em relação ao período mensal anterior, selecione **% Custo fixo do mês anterior**.  Em seguida, preencha o percentual de variação de custo válido, ou seja, se o _Cost Variance_ for 12%, defina a porcentagem de notificação em 13%.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-11.webp "Configurando Budgets no Cloud8")

Esse tipo de Budget não demanda a definição de valores, pois utiliza os custos do mês anterior como parâmetro de comparação, gerando um cenário ideal de crescimento planejado e monitoramento automatizado.

**Aumentou % Estimativa do mês anterior e Aumentou % Custo fixo do mês anterior**

No caso de haver uma margem de tolerância de aumento de custos em relação ao período mensal anterior, selecione **Aumentou % Estimativa do mês anterior** ou **Aumentou % Custo fixo do mês anterior**.  Em seguida, preencha o percentual de variação de custo válido, ou seja, se o _Cost Variance_ for 12%, defina a porcentagem de notificação em 13%.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-12.webp "Configurando Budgets no Cloud8")

**Diminuiu % Estimativa do mês anterior**

A Cloud8 permite a configuração de um budget de redução de custos em relação ao período mensal anterior, bastando slecionar **Diminuiu % Estimativa do mês anterior**.  Em seguida, preencha o percentual de variação de custo válido, ou seja, se o _Cost Variance_ for 12%, defina a porcentagem de notificação em 13%.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-13.webp "Configurando Budgets no Cloud8")

Esse tipo de Budget não demanda a definição de valores, pois utiliza os custos do mês anterior como parâmetro de comparação, gerando um cenário ideal para identificação de períodos de sazonalidade e avaliação de impacto de desativação de features e sistemas.

### Integrações

Ao configurar um budget, é possível integrar com sistema de mensageria ou disparo de e-mail para os responsáveis por gerenciar o orçamento.

**Quando**: Define a granularidade com a qual os alertas são disparados.

- Diário
- Semanal
- Último dia do mês
- Única vez no mês quando ultrapassar o valor
- Sempre que ultrapassar o valor

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-14.webp "Configurando Budgets no Cloud8")

## Passo 3 – Gravar as alterações

Ao concluir a configuração de todos os campos, lembre-se de clicar em **Gravar**, ou todas as configurações serão perdidas. 

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-15.webp "Configurando Budgets no Cloud8")

## Visualização dos dados do budget

Após a configuração do Budget, é possível monitorar o orçamento clicando no ícone azul e vermelho representando um gráfico. Esta funcionalidade permite a avaliação comparativa entre o custo efetivo e o custo projetado para o período selecionado.

![Configurando Budgets no Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/03/budgets-16.webp "Configurando Budgets no Cloud8")

## Considerações finais

A configuração de Budgets deve ser configurada individualmente para cada provedor. Caso se dejse criar um Budget que englobe mais de um provedor, é necessário criar uma Unidade de Negócios.