#azure #governance #data_analysis #data_engineering #finops #cloudcomputing 

O Fabric reside numa capacidade, que é um pool de recursos alocados na plataforma. Cada capacidade tem um número de Capacity Units (CUs). É possível monitorar as capacidades do Microsoft Fabric utilizando o Microsoft Fabric Capacity Metrics.
## Instalar o aplicativo de monitoramento

- Precisa ser Capacity Admin
- Precisa de uma licença de Power BI (Pro, Premium Per User ou trial)

1ª opção - Vá em [AppSource > Microsoft Fabric Capacity Metrics](https://go.microsoft.com/fwlink/?linkid=2219875) e clique em **Get it now**.

2ª opção - Em Power BI service:
1. Select **Apps**.
2. Select **Get apps**.
3. Search for **Microsoft Fabric**.
4. Select the **Microsoft Fabric Capacity Metrics** app.
5. Select **Get it now**.

Entre no AppSource usando a conta Microsoft e conclua a tela de registro. O aplicativo levará ao Microsoft Fabric para concluir o processo. Selecione **Instalar** para continuar.
## Executar pela primeira vez

Para concluir a instalação, configure o aplicativo Métricas de Capacidade do Microsoft Fabric executando-o pela primeira vez.

1. No Microsoft Fabric, na experiência do Power BI, selecione **Aplicativos**. Se você estiver executando o aplicativo logo após instalá-lo, será redirecionado para o painel **Aplicativos** e poderá pular para a etapa 2. Caso contrário, para ver o painel **Aplicativos** , altere o seletor de experiência da parte inferior esquerda para o Power BI em vez do Fabric.
2. Selecione o aplicativo **Métricas de Capacidade do Microsoft Fabric**.
3. Quando aparecer a mensagem _Você precisa se conectar aos seus dados para ver este relatório_, selecione **Conectar**.
4. Na primeira janela **Conectar-se às Métricas de Capacidade do Microsoft Fabric**, preencha os campos de acordo com a tabela:

| Campo | Obrigatório | Valor | Observações |
|---|---|---|---|
| UTC_offset | Sim | Valores numéricos de 14 a -12. Para indicar um fuso horário de meia hora, use `.5`. Exemplo: `5.5` para o horário padrão da Índia. | Insira o horário padrão da sua organização em UTC (Tempo Universal Coordenado). |
| RegionName | Aplicável à versão 2.0 e abaixo | **Administrador de capacidade:** defina o parâmetro de região como `"Padrão"`.<br><br>**Administrador de Locatários:**<br>• Se você for administrador de locatários e tiver permissões de administrador em uma capacidade na região inicial ou não houver capacidades na região inicial para todo o locatário, defina o parâmetro como `"Padrão"`.<br>• Caso contrário, defina-o como uma das regiões em que você possui permissão de administrador em uma capacidade (exemplo: `"Europa Ocidental"`). | 1. Capacidades pausadas e de avaliação também são consideradas ao determinar as regiões disponíveis.<br><br>2. Após a configuração, a criação ou exclusão de capacidades pode impactar o relatório. Reavalie o valor do parâmetro `RegionName`. Caso o valor precise mudar, atualize as configurações do modelo semântico e realize uma atualização do modelo.<br><br>3. O `RegionName` pode ser encontrado nas configurações de capacidade no portal de administração. No Microsoft Fabric, acesse:<br>`Configurações > Governança e insights > Configurações de capacidade do portal de administração` e verifique o valor da região exibido ao lado do nome da capacidade. |
| DefaultCapacityID | Aplicável às versões 1.9.2 a 2.0 | ID de uma capacidade da qual você é administrador. | A ID da capacidade pode ser encontrada na URL da página de gerenciamento de capacidade.<br><br>No Microsoft Fabric, acesse a administração de capacidades e selecione uma capacidade. A ID estará presente na URL após `/capacities/`.<br><br>Exemplo:<br>`https://app.powerbi.com/admin-portal/capacities/00001111-aaaa-2222-bbbb-3333cccc4444`<br><br>Nesse caso, a ID é:<br>`00001111-aaaa-2222-bbbb-3333cccc4444`.<br><br>Após a instalação, o aplicativo permite visualizar todas as capacidades às quais você possui acesso. |
| CapacityID | Aplicável à versão 1.8 e abaixo | ID de uma capacidade da qual você é administrador. | A ID da capacidade pode ser encontrada na URL da página de gerenciamento de capacidade.<br><br>No Microsoft Fabric, acesse a administração de capacidades e selecione uma capacidade. A ID estará presente na URL após `/capacities/`.<br><br>Exemplo:<br>`https://app.powerbi.com/admin-portal/capacities/00001111-aaaa-2222-bbbb-3333cccc4444`<br><br>Nesse caso, a ID é:<br>`00001111-aaaa-2222-bbbb-3333cccc4444`.<br><br>Após a instalação, o aplicativo permite visualizar todas as capacidades às quais você possui acesso. |
| Avançado | Opcional | `Ligado` ou `Desligado` | O aplicativo atualiza os dados automaticamente à meia-noite. Essa funcionalidade pode ser desabilitada expandindo a opção avançada e selecionando `Off`. |

5. Selecione **Avançar**.
6. Na segunda janela **Conectar-se às Métricas de Capacidade do Microsoft Fabric**, preencha os seguintes campos:
    
    - **Método de autenticação** – Selecione o método de autenticação. O único método de autenticação com suporte é _OAuth2_.
    - **Configuração de nível de privacidade desta fonte de dados** – Selecione _Organizacional_ para habilitar o acesso do aplicativo a todas as fontes de dados da organização.

Observação

_ExtensionDataSourceKind_ e _ExtensionDataSourcePath_ são campos internos relacionados ao conector do aplicativo. Não altere os valores desses campos.

7. Selecione **Entrar e continuar**.
8. Selecione uma capacidade na lista suspensa **Nome da capacidade**.
9. Após você configurar o aplicativo, pode levar alguns minutos para que ele obtenha seus dados. Se você executar o aplicativo e ele não estiver exibindo nenhum dado, atualize o aplicativo. Esse comportamento só acontece quando você abre o aplicativo pela primeira vez.

## Funcionalidades

O aplicativo Microsoft Fabric Métricas de Capacidade fornece vários recursos e funcionalidades para ajudá-lo a monitorar e gerenciar suas capacidades de forma eficaz. O aplicativo inclui as seguintes páginas:

- **Página de Saúde**: obtenha uma visão geral de alto nível para todas as capacidades de que você é administrador e identifique aquelas que consomem mais recursos computacionais ou enfrentam problemas, como restrições ou rejeições de consultas. Para obter mais informações, consulte [Compreender a página Saúde do aplicativo de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-health-page).
    
- **Página de Compute**: obtenha uma visualização de 14 dias do desempenho de computação da sua capacidade. Os visuais incluem gráficos de fita, tendências de utilização e uma matriz de operações, ajudando você a analisar padrões de uso, cargas de pico e eventos de restrição. "AI Functions aparece como uma categoria de operação distinta em gráficos de fita, tendências de utilização e na matriz de operações, controlada separadamente do Spark e do Dataflows Gen2." Para obter mais informações, consulte [Noções básicas sobre a página de computação do aplicativo de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-compute-page).
    
- **Página de armazenamento** : monitore o uso do armazenamento nos últimos 30 dias. Exiba o armazenamento atual e faturável por área de trabalho, acompanhe os dados excluídos temporariamente e explore tendências por meio de gráficos de barras e tabelas detalhadas. Para obter mais informações, consulte [Noções básicas sobre a página de armazenamento de aplicativos de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-storage-page).
    
- **Ponto de Tempo**: aprofunde-se em um intervalo de tempo específico de 30 segundos para ver quais operações (interativas ou em segundo plano) consumiram mais recursos computacionais. A divisão da operação inclui um grupo dedicado às Funções de IA, para que você possa ver o uso das Funções de IA num intervalo de tempo de 30 segundos. Use esta página para diagnosticar sobrecargas e entender o comportamento de dimensionamento automático ou limitação. Para obter mais informações, consulte [Entenda a página de ponto de tempo do aplicativo de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page).
    
- **Página de Resumo do Momento no Tempo**: resume os tipos de operação (não as operações individuais) que contribuíram para o uso da capacidade em um momento no tempo selecionado. Os visuais de resumo incluem o AI Functions como um tipo de operação, ajudando a identificar quando ele contribui significativamente para o uso da capacidade e os limiares de escalonamento automático. Para obter mais informações, consulte [Entenda a página de resumo do marcador de tempo do aplicativo de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-summary-page).
    
- **Página de detalhes do item no marco temporal**: fornece detalhes granulares sobre operações dentro de um item específico em um momento. Inclui filtros para ID de operação, usuário e limites de CU que são úteis para análise de causa raiz e ajuste de desempenho. Para obter mais informações, consulte [a página de detalhes do item de ponto temporal do aplicativo de métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-item-detail-page).
    
- **Computação de dimensionamento automático para Spark** Página: Esta página fornece insights sobre o comportamento de dimensionamento automático de cargas de trabalho do Spark, ajudando você a otimizar o desempenho e a alocação de recursos. Para obter mais informações, consulte [Entenda o aplicativo de métricas Autoscale compute para a página Spark](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-feature-autoscale-page).
    
- **Página de detalhes de dimensionamento automático para Spark: aprofunde-se** nas operações de dimensionamento automático para entender quais cargas de trabalho dispararam o dimensionamento e como elas contribuíram para o uso geral da capacidade. Para obter mais informações, consulte [a página de detalhes do Understand Autoscale compute for Spark](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-feature-autoscale-detail-page).
    
- **Planejar capacidade**: Aprenda como estimar a SKU de capacidade correta para suas cargas de trabalho usando o aplicativo de métricas e o Avaliador de SKU Fabric. Ajuda a evitar excesso ou subprovisionamento. Para obter mais informações, consulte [Planejar o tamanho da capacidade](https://learn.microsoft.com/pt-br/fabric/enterprise/plan-capacity).
    
- **Monitorar a capacidade pausada**: acompanhe quando uma capacidade foi pausada ou retomada e entenda por que picos de utilização podem aparecer durante pausas. Inclui diretrizes sobre como interpretar a operação `carryforward`. Para saber mais, confira [Monitorar uma capacidade pausada](https://learn.microsoft.com/pt-br/fabric/enterprise/monitor-paused-capacity).
    
- **Cálculos**: entenda como o aplicativo calcula as principais métricas, como uso de UC, restrição e impacto no escalonamento automático. Os cálculos de taxonomia de operação e de CU incluem funções de IA como um tipo de operação separado. O uso de CU é atribuído de forma independente do Spark e do Dataflows Gen2 em todos os visuais. Útil para interpretar visuais e validar relatórios internos. Para obter mais informações, consulte [cálculos do aplicativo Métricas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-calculations).
## Latência de dados

Os dados no aplicativo Microsoft Fabric Capacity Metrics estão sujeitos ao processamento e à latência de atualização. Em geral, os dados de uso ficam disponíveis dentro de 10 a 15 minutos após a atividade. Por exemplo, às 17h15 (hora local), gráficos como o gráfico de utilização podem exibir dados até aproximadamente 17h.

Algumas dimensões, incluindo **capacidades**, **workspaces** e itens, são **atualizadas** como parte de uma atualização de modelo semântico agendada à meia-noite (hora local). Como resultado, alterações, como a criação de uma nova capacidade, de um workspace ou de um item, ou a movimentação de um workspace entre capacidades, aparecem no aplicativo após a próxima atualização.
## Considerações e limitações

Ao usar o aplicativo Microsoft Fabric Métricas de Capacidade, considere as seguintes considerações e limitações:

- Atualize os parâmetros e atualize o modelo semântico sempre que suas capacidades disponíveis forem alteradas. Por exemplo, se você obter acesso de administrador de locatário JIT, atualize o parâmetro _RegionName_ nas configurações de modelo semântico (conforme descrito nas diretrizes de instalação) e atualize o modelo após a concessão do acesso.
    
- O aplicativo de Métricas de Capacidade do Microsoft Fabric não dá suporte a alertas ou notificações. Para alertas em tempo real, consulte [o que é Real-Time hub?](https://learn.microsoft.com/pt-br/fabric/real-time-hub/real-time-hub-overview)
    
- Os dados para novas capacidades não ficam visíveis no aplicativo Métricas até a próxima atualização agendada. Os dados de novos itens e espaços de trabalho não ficam visíveis até a próxima atualização agendada após a primeira operação que consuma CUs realizada nos últimos 14 dias. Para exibir os dados antes da próxima atualização agendada, inicie uma atualização manual do modelo semântico.
    
- Para ocultar os emails de usuários no aplicativo, desabilite a configuração [Show user data in the Fabric Capacity Metrics app and reports](https://learn.microsoft.com/pt-br/fabric/admin/service-admin-portal-audit-usage#show-user-data-in-the-fabric-capacity-metrics-app-and-reports) no portal do Admin.
    
- Itens e operações faturáveis consomem unidades de capacidade da sua capacidade e são pagos pela sua organização. Itens e operações não faturáveis refletem funcionalidades de pré-visualização que não contam para o limite de capacidade e não são pagos. Eles fornecem uma indicação do possível impacto futuro em sua capacidade. Quando os recursos de visualização se tornam geralmente disponíveis, sua organização começa a pagar por eles e seu impacto na sua capacidade é levado em conta.
    
- Na exibição logarítmica do visual [Utilização e limitação da capacidade](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-compute-page#capacity-utilization-and-throttling), o eixo primário visto à esquerda do visual não está alinhado com o eixo secundário visto à direita do visual.
    
- Nas tabelas de operações [interativas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page#interactive-operations-for-timerange) e [em segundo plano](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page#background-operations-for-timerange), a coluna _Aceleramento(s)_ exibe zero quando o aceleramento está desabilitado, mesmo quando a capacidade está sobrecarregada.
    
- Há uma diferença de 0,01 a 0,05% entre o valor _% de unidade de capacidade_ nos [Visuais da primeira linha](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page#top-row-visuals)_Gráfico de linhas de pulsação_ e os valores [Total de unidade de capacidade](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page#interactive-operations-for-timerange) das tabelas de operações [interativas](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-timepoint-page#background-operations-for-timerange) e em _segundo plano_.
    
- Quando o estado de capacidade permanece inalterado durante as datas selecionadas ou nos últimos 14 dias, ele não aparece na tabela Evento do Sistema.
    
- A amostragem pode ocorrer durante a exportação de dados da página Exportar Dados. Consulte o segundo e o terceiro marcadores em [Considerações e limitações](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-export-data?tabs=powerbi-desktop#considerations-and-limitations).
    
- O modelo semântico usado pelo aplicativo Microsoft Fabric Capacity Metrics só tem suporte para uso pelos relatórios fornecidos no aplicativo. Não há suporte para qualquer consumo, uso ou modificação do modelo semântico.
    
- A coluna _CU (s)_ da [tabela de matriz por item e operação](https://learn.microsoft.com/pt-br/fabric/enterprise/metrics-app-compute-page#matrix-by-item-and-operation) exibe o consumo cumulativo de segundos de CU para um item específico nos últimos 14 dias. Se você mover o item de outro espaço de trabalho para o espaço de trabalho atual nos últimos 14 dias, a coluna _CU (s)_ incluirá o consumo cumulativo de segundos de CU para o item no espaço de trabalho anterior.
    
- O aplicativo de Métricas de Capacidade do Fabric oferece suporte a ambientes que usam links privados em nível de locatário [](https://learn.microsoft.com/pt-br/fabric/security/security-private-links-overview), mas não há suporte para links privados em nível de espaço de trabalho nos workspaces onde o aplicativo está instalado.
    
- Os valores de limite em visuais de limitação não refletem as configurações de proteção contra sobretensão aplicadas. Para exibir os limites reais de [surge protection](https://learn.microsoft.com/pt-br/fabric/enterprise/surge-protection), consulte o Portal Administrativo no Power BI Service.
## Compartilhar o relatório de métricas de capacidade do Fabric

Quando você instala o aplicativo de Métricas de Capacidade do Microsoft Fabric, ele cria um espaço de trabalho em seu locatário Microsoft Fabric. Para compartilhar o relatório, você deve ser um administrador de capacidade.

Para compartilhar o relatório de Métricas de Capacidade do Fabric, siga estas etapas:

1. Abra o aplicativo de Métricas de Capacidade do Microsoft Fabric.
2. Vá para o workspace onde você instalou o aplicativo.
3. Selecione **Compartilhar**.

Você pode optar por compartilhar com _usuários em sua organização_ ou com _usuários business-to-business (B2B) de uma organização externa que são convidados para o seu tenant como visitantes (por meio da Colaboração B2B do Azure)_. Essa opção é útil quando você deseja que alguém de fora da sua organização, como um consultor ou parceiro, veja as Métricas de Capacidade do Fabric sem movê-las para seu tenant interno.

## APIs de Acesso

## Integração com Billing Export

## Referências

https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app?utm

https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app-install?tabs=1st
## Conteúdo relacionado

[[Automação de Start e Stop para Fabric]]
