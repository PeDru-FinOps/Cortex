#arquitetura_solucoes #cloud8 #aws #azure #cloudcomputing #finops #oci #gcp #governance 

A automação de tarefas em ambientes de computação em nuvem é um recurso essencial para otimizar a execução de atividades repetitivas, melhorar a produtividade e reduzir custos. Com ferramentas modernas, é possível agendar diversas ações em servidores na nuvem, como backups, alterações de configurações e escalabilidade, garantindo maior controle e eficiência na gestão da infraestrutura.

A funcionalidade de automações da Cloud8 funciona através de agendamentos únicos ou recorrentes, e não possui suporte para automações reativas, como execução com base em métricas.

## Tarefas que podem ser automatizadas no Cloud8

### Automações para Instâncias

1. **_Start_**: iniciar instância desligada.
2. **_Stop_**: parar uma instância ativa.
3. **_Upgrade / Downgrade_**
4. **_Change Volume Type_**: alterar o tipo do volume de dados atachado ao servidor. 
5. **_Backup_**: realiza um backup da instância.
6. **_Copy backup to region_**: efetua uma cópia assíncrona do backup para outra região.
7. **_Security copy (Vault) to another AWS provider_**: cria uma cópia de segurança de uma instância de um provider AWS para outro provider AWS. 
8. **_Interval_**: funcionalidade interna do Automações que permite configurar um intervalo de tempo entre a execução de automações configuradas no mesmo _Workflow_.
9. **_Connect to Load Balancer_**
10. **_Disconnect from Load Balancer_** 
11. **_Associate security group_**
12. **_Dessassociate security group_**
13. **_Scale t*.unlimited_**: caso tenha criado sua Conta da AWS antes de 15 de julho de 2025 e use uma instância t2.micro ou t3.micro da oferta do [Nível gratuito da AWS](https://aws.amazon.com/free/) no modo unlimited, poderão ser aplicadas cobranças se o consumo médio durante um período contínuo de 24 horas exceder o [uso de linha de base](https://docs.aws.amazon.com/pt_br/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html#baseline_performance) da instância.
14. **_Script – Command_**: executa um comando determinado na instância.
15. **_Script – HTTP Webservice_**
16. **Connect elastic IP**: conectar um _Elastic IP_.
17. **_Reboot_**: reiniciar a instância.
18. **_Terminate_**: deletar a instância.

### Automações para Bancos de Dados

1. **_Start_**: iniciar instância desligada.
2. **_Stop_**: parar uma instância ativa.
3. **_Upgrade / Downgrade_**: alterar o SKU da instância.
4. **_Change Volume Type_**: alterar o tipo do volume de dados atachado ao servidor.  
5. **_Backup_**: realiza um backup da instância.
6. **_Copy backup to region_**: efetua uma cópia assíncrona do backup para outra região.
7. **_Security copy (Vault) to another AWS provider_**: cria uma cópia de segurança de uma instância de um provider AWS para outro provider AWS.
8. **_Export databases_**:
9. **_Connect to a pool_**:
10. **_Disconnect from pool_**:
11. **_Scale capacity_**:
12. **_Change size/capacity_**
13. **_Change OCPUs (Core count)_**
14. **_Reboot_**: reiniciar a instância.
15. **_Cache Reboot_**: reiniciar o cache da instância.

### Automações para Apps (Auto Scalling)

1. **_Scale instance number_**
2. **_Stop / Deallocate_**
3. **_Start_**
4. **_Scale Service Plan_**

### Automações para Containeres

1. **_Scale / Turn off cluster service_**
2. **_Change capacity providers_**
3. **_Change task definition_**

### Automações para DNS Zones

1. **_DNS Backup_**

### Automações para Volumes de Dados

1. **_Backup / Snapshot_**
2. **_Copy snapshot to region_**
3. **_Security copy (Vault) to another AWS provider_**
4. **_Change type (Scale)_**

### Automações de Reports

1. **_Backup Coverage_**
2. **_Backup List_**
3. **_Billing estimate summary_**
4. **_Stopped instances_**
5. **_Unttaged Resources with ID_**
6. **_Completed Workflows_**
7. **_CSV costs per product_**
8. **_New instances_**
9. **_AWS Security Groups_**
10. **_AWS VPC and Subnets_**

## Configurando Workflows de Automações

Um **_Workflow_ de Automação** é um conjunto de uma ou mais ações que podem ser configuradas e executadas em um dos recursos que possuem suporte para automação. Assim, não é necessário criar diversas automações individualmente para executar uma sequência de tarefas, e as mesmas podem ser programadas como um fluxo de trabalho inteligente.

Em **_Automations_**, selecione o servidor e clique em “**_New Workflow_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-01.png "Cloud8 Automations")

Selecione quais recursos serão impactados pela automação, e defina um nome para mesma. Defina a data e horário nos quais ocorrerá o primeiro disparo da automação.

A tela exibida apresentará a configuração de uma automação. No exemplo abaixo, realizamos a configuração de um fluxo de trabalho onde um servidor é desligado, recebe um downgrade e é iniciado novamente. Entre cada tarefa, foi definido um intervalo de tempo de 10 minutos, a fim de garantir a conclusão de todos os jobs da automação.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-02.png "Cloud8 Automations")

Para incluir uma task no _Workflow_, selecione-a em “**_Type_**”, e após configurar os seus parâmetros, clique na seta para direta para que ela entre no painel do “_**Run in the order**_”. As setas definem as seguintes ações:

- **Direita**: inclui no _Workflow_
- **Esquerda**: remove do _Workflow_
- **Para cima**: sobe o item selecionado na ordem de execução
- **Para baixo**: desce o item selecionado na ordem de execução

Após a configuração, caso clique em “**_Save_**”, o _workflow_ será configurado e executado exclusivamente na data e hora informada na configuração. Para que a automação seja recorrente, é necessário clicar na aba “_**Repetitions**_” e configurar a recorrência selecionando a opção “_**This workflow repeats**_”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-03.png "Cloud8 Automations")

No exemplo acima foi configurada uma automação semanal, que será executada todas as sextas-feiras, sem prazo de expiração.

## Configurando Workflows por Tags

Tendo em vista que as automações do **Cloud8** não são reativas, ou seja, não disparam com base em métricas de utilização de recursos, é possível utilizar tags para definir cenários onde dinamicamente um recurso deverá executar a automação. Um exemplo seria quando a organização possui bancos de dados com uma determinada regra de granularidade; mas também possui bancos de dados críticos que precisam de backup de hora em hora durante períodos específicos. Neste caso, uma tag de frequência de backup pode ser configurada e utilizada em um _Workflow_ da **Cloud8**.

Em outros casos, o usuário pode simplesmente deseja criar uma automação que seja aplicada a todos os recursos que atendem à uma determinada regra de negócio, por exemplo, quando é definido que todos os recursos de desenvolvimento deverão ser desligados no final de semana.

### 1º Passo – Criar um Workflow de Automação

Clique em “**_Template / Tags_**” e selecione “_**New Workflow Template**_”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-05.png "Cloud8 Automations")

Na aba “**_Template_**” defina um nome para o template e prossiga para aba “_**Workflow**_”. Defina um recurso em “_**Resources**_”, porém não se preocupe com o servidor selecionado, pois ele serve apenas para permitir a configuração do workflow, e não será considerado para fins de automação caso não possua a tag definida.

Defina um nome para o _Workflow_ e defina a data e horário nos quais ocorrerá o primeiro disparo da automação. Em “_**Task**_” configure todo o fluxo de tasks da automação. No exemplo abaixo foi definido um _workflow_ que apenas desligará os servidores na sexta-feira a noite.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-06.png "Cloud8 Automations")

Clique na aba “**_Repetitions_**” e configure a recorrência selecionando a opção “**_This workflow repeats_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-03.png "Cloud8 Automations")

No exemplo acima foi configurada uma automação semanal, que será executada todas as sextas-feiras, sem prazo de expiração. Ao concluir, clique em “**_Save_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-07.png "Cloud8 Automations")

### 2º Passo – Configurar a execução por Tags

Agora que já possuímos um template do workflow, podemos definir que o mesmo seja atribuído e executado automaticamente em todos os recursos que possuem determinado valor de tag. Para isso, clique em “**_Templates / Tags_**” e em seguida selecione “**_Tags <-> Templates_**”.

Perceba que o template criado passa a ser listado abaixo das opções de configuração.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-05.png "Cloud8 Automations")

Em “**Tag**” selecione “**_New association_**” e informe o “_**Tag name**_” e o “**_Tag value_**”. No exemplo abaixo, a automação deverá ser executada em todos os recursos que possuam a tag “**automation**” com o valor “**true**”.

Como a funcionalidade é _case sensitive_, é possível verificar ocorrências diversas tags diferentes separando-as por vírgula.

![](https://www.cloud8.com.br/wp-content/uploads/2025/11/image-9.png)

Em “**_Linked Templates_**” selecione o template criado. Em “**_Providers_**” selecione quais provedores cadastrados serão verificados para execução da automação. Ao final, clique em “**Save**”.

**NOTA:** Esta funcionalidade ainda não está disponível para provedores **OCI** e **Huawei**.

## Configurando Workflows por Provider

A configuração de _Workflows_ por _Provider_ permite todos os recursos de um determinado provedor cadastrado no **Cloud8** recebam as mesmas automações, sem necessidade de configurar manualmente em cada um deles. 

### 1º Passo – Criar um Workflow de Automação

Clique em “**_Template / Tags_**” e selecione “**_New Workflow Template_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-05.png "Cloud8 Automations")

Na aba “**_Template_**” defina um nome para o template e prossiga para aba “**_Workflow_**”. Defina um recurso em “**_Resources_**”, porém não se preocupe com o servidor selecionado, pois ele serve apenas para permitir a configuração do _workflow_, e não será considerado para fins de automação caso não possua a tag definida.

Defina um nome para o _Workflow_ e defina a data e horário nos quais ocorrerá o primeiro disparo da automação. Em “**_Task_**” configure todo o fluxo de _tasks_ da automação. No exemplo abaixo foi definido um _workflow_ que apenas desligará os servidores na sexta-feira a noite.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-06.png "Cloud8 Automations")

Clique na aba “**_Repetitions_**” e configure a recorrência selecionando a opção “**_This workflow repeats_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-03.png "Cloud8 Automations")

No exemplo acima foi configurada uma automação semanal, que será executada todas as sextas-feiras, sem prazo de expiração. Ao concluir, clique em “**_Save_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-07.png "Cloud8 Automations")

### 2º Passo – Configurar a execução por Provider

Agora que já possuímos um template do workflow, podemos definir que o mesmo seja atribuído e executado automaticamente em todos os recursos que possuem determinado valor de tag. Para isso, clique em “**_Templates / Tags_**” e em seguida selecione “**_Tags <-> Providers_**”.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-05.png "Cloud8 Automations")

Em “**_Link name_**”, clique “**_New association_**” e defina um “**_Name_**” para configuração. Em “**_Linked Templates_**” selecione o template criado. Em “**_Providers_**” defina em quais provedores a automação será executada. Ao final, clique em “**_Save_**”.

![](https://www.cloud8.com.br/wp-content/uploads/2025/11/image-9.png "Cloud8 Automations")

**NOTA:** Esta funcionalidade ainda não está disponível para provedores **OCI** e **Huawei**.

![Cloud8 Automations](https://www.cloud8.com.br/wp-content/uploads/2025/11/cloud8-automations-011.png "Cloud8 Automations")

Perceba que o painel exibirá um bloco identificando a automação no horário e provedores configurados.