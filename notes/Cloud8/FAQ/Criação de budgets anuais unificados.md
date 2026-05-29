#cloud8 #finops #data_analysis #governance #cloudcomputing #oci #aws #azure #gcp 

A criação de orçamentos anuais facilita muito a gestão financeira de qualquer empresa, oferecendo visibilidade de médio e longo prazo para as despesas previstas e, possibilitando assim, o planejamento de custos dentro do período. Quando se trata de custos com infraestrutura de computação em nuvem, os provedores de serviço atualmente oferecem funcionalidades com essa finalidade, organizando um dos maiores custos de tecnologia para alguns tipos de negócio.

Porém, quando as empresas utilizam ambientes multicloud híbridos e distribuídos, baseados em mais de uma empresa provedora, esse processo pode se tornar pouco eficiente, dadas as diferenças entre as plataformas e tecnologias, resultando em um número sempre crescente de regras a serem criadas e administradas.

A Plataforma Cloud8 permite ao usuário simplificar a **gestão de orçamentos empresariais** através do agrupamento de diversos provedores em uma **única visualização**, reunindo de forma simples e direta todos os dados necessários para montagem do budget, independente do provedor utilizado. Confira abaixo como fazer.

## Passo 1 – Acessando a Gestão de Budgets da Cloud8

No menu lateral esquerdo, selecione **FinOps Reports**, e em seguida **Budgets**. Clique em **Novo**, e um modelo de budget em branco será criado para edição. Cada campo representado por uma coluna precisa ser selecionado e preenchido.

## Passo 2 – Configurando o Budget

### Nome

O nome que será dado ao Budget. Uma boa prática a ser adotada é dar nomes que deixem bem clara a função do orçamento que ele representa, os provedores configurados, unidades de negócio e método de agrupamento definido (Tags, Invoice ou Produto).

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step01.webp)

### Budgets – Itens

Configuração dos provedores atribuídos ao budget. Ao clicar no campo, todos os provedores cadastrados serão exibidos.

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step02.webp)

Atualmente há 3 (três) formatos de Budget implementados na ferramenta Cloud8:

- Organização – Invoice
- Organização – Produtos
- Organização – Tags

**Organização – Invoice (BETA)** – Essa configuração de budget realiza o monitoramento do orçamento através do Invoice gerado pelos provedores. Em cenários onde unidades de negócio, aplicações e produtos estão devidamente separados por Billing Profile (Azure), Billing Account (AWS), Payer Account (GCP e Huawei).

**Organização – Produtos (Técnico)** – Essa configuração de budget realiza o monitoramento do orçamento através de categorias de serviço oferecidos no provedor. É possível especificar quais produtos você deseja monitorar dentro do orçamento definido, sendo recomendado para cenários como o de novas implementações e produtos (Ex: Uma PoC de utilização de recursos de Inteligência Artificial, onde você pode estipular um orçamento para evitar que os custos ultrapassem valores razoáveis).

**Organização – Tags (Negócios)** – Essa configuração de budget realiza o monitoramento do orçamento através de metadados e seus respectivos valores, permitindo maior controle de budgets à nível de negócios.

### Moeda

Defina a moeda que será considerada no acionamento do trigger, impactando diretamente em cenários onde o provedor realiza o faturamento em moeda específica (como no caso da AWS, que fatura em USD), ou contratos que não possuem taxa de câmbio fixo.

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step07.webp)

### Método

A ferramenta Cloud8 possui diversos métodos de acionamento para monitorar estouro de orçamento. No caso de orçamentos anuais, selecione **Custo fixo anual BETA**. Em seguida, preencha o Budget com o custo total do período, data de início do orçamento, vigência em anos e método de preenchimento, que poderá ser:

1. **Completar com valores mensais consumidos e dividir sobra**: para cenários onde os custos mensais poderão variar, porém o orçamento de todo o período está definido, e o escopo do projeto deverá ser ajustado ao saldo remanescente.
2. **Proporcional – dividir pelo número de meses**: para cenários onde há um custo médio definido, e as variações mensais permitem a identificação de anomalias de consumo e insights sobre crescimento de custos e ambiente.

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step08.webp)

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step09.webp)

### Integrações

Ao configurar um budget, é possível integrar com sistema de mensageria ou disparo de e-mail para os responsáveis por gerenciar o orçamento.

### Quando

Define a granularidade com a qual os alertas são disparados.

- Diário
- Semanal
- Último dia do mês
- Única vez no mês quando ultrapassar o valor
- Sempre que ultrapassar o valor

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step10.webp)

## Passo 3 – Gravar as alterações

Ao concluir a configuração de todos os campos, lembre-se de clicar em **Gravar**, ou todas as configurações serão perdidas. 

![](https://www.cloud8.com.br/wp-content/uploads/2025/08/budget-step11.webp)

## Considerações finais

A configuração de Budgets deve ser configurada individualmente para cada provedor. Caso se dejse criar um Budget que englobe mais de um provedor, é necessário criar uma Unidade de Negócios.

## Conexões aprovadas

- [[Cloud8/SOPs/Configurando Budgets no Cloud8]]
