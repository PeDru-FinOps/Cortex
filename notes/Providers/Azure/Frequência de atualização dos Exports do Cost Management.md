#azure #cloudcomputing #finops #data_governance 

Arquivo vinculado: [[Criar Cost Management Exports]]

Considerando um dos [[Princípios de FinOps]], que diz que os relatórios precisam ser acessíveis e estar disponíveis o mais rápido possível, devemos sempre considerar a qualidade e frequência da atualização dos dados, e na Azure não é diferente.

Resumindo:

- Quando você agenda uma exportação, ela sempre roda na mesma frequência definida (por exemplo, diariamente).
- Em exportações diárias, os dados incluem os custos acumulados desde o início do mês até a data atual.
- O horário exato da execução pode variar ao longo do dia, pois depende da carga do Azure — não dá para confiar em um horário fixo.
- Depois que a exportação começa, os dados ficam disponíveis em até 4 horas.
- Todo o agendamento é baseado em UTC (tempo universal coordenado).

Sobre a configuração:

- Pela API, você deve informar o horário já em UTC — não há conversão automática.
- Pelo portal do Azure, o horário local é automaticamente convertido para UTC.

Exemplo:

- Se você agenda via API às 14:00 UTC, esse horário é usado diretamente.
- Se agenda pelo portal às 02:00 no horário da Índia (UTC+5:30), o sistema converte para 20:30 UTC do dia anterior.

![[Pasted image 20260415144814.png]]

## Disponibilidade da Informação mais recente

Em Subscriptions EA e MCA os dados ficam disponíveis no Cost Management no período de 8 a 24 horas.

Em Subscriptions Pay-as-you-Go leva até 72 horas para informação ficar disponível.

- Os custos estimados são atualizados **6 vezes por dia** e podem mudar conforme o uso aumenta.
- Cada atualização é **cumulativa** (inclui dados anteriores).
- O período de faturamento é fechado até **72 horas após o fim**.
- Durante o mês em aberto, os valores são **estimativas** e podem ter atrasos.

**Exemplos de fechamento**

- EA: mês termina em 31/03 → fechado até **04/04 (UTC)**.
- Pay-as-you-go: mês termina em 15/05 → fechado até **19/05 (UTC)**.
- Custos podem continuar sendo ajustados até **5 dias após o fim** do período.
- A fatura é o valor **final**.

**Retenção de dados**

- Dados ficam armazenados por **pelo menos 7 anos**.
- No portal: acesso aos últimos **13 meses**.
- Para dados mais antigos: usar a **API de Exports**.

**Reprocessamento (rerated data)**

Os custos do período atual podem ser **recalculados** até o fechamento da fatura.

**Arredondamento de custos**

- No portal: valores são **arredondados** (regra padrão).
- API e arquivos: **sem arredondamento** (até 8 casas decimais).
- Arredondamento só ocorre na **exibição**, não no cálculo interno.

**Desconto Azure Commitment (ACD)**

- Arredondamento ocorre na taxa unitária conforme a moeda.
- Exemplo: desconto aplicado → valor arredondado → custo total = quantidade × valor arredondado.
- Em casos com unidades (ex: 10 horas), o arredondamento ocorre no total e depois é redistribuído.

**Diferença entre dados históricos e fatura**

Dados históricos mostram **custos estimados**, sem créditos ou pagamentos antecipados. A fatura pode ter valores diferentes devido a:

- Créditos/descontos
- Mudanças de preço

Exemplo: consumo em dezembro com preço antigo, mas estimativa usa preço novo.
## Referência

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-improved-exports#create-exports

https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data