#cloud8 #aws 
## Introdução

Para que o Cloud8 se conecte aos provedores da AWS, você precisa fornecer as credenciais necessárias à plataforma. Atualmente, há duas maneiras de fazer isso:

- **[IAM Role](https://www.cloud8.com.br/ajuda/conectando-provedores-aws/#iam-role)** (_recomendado_) – cria-se um _Role_ com permissão explícita para a conta AWS usada pelo **Cloud8**.
- **[Access Key IAM](https://www.cloud8.com.br/ajuda/conectando-provedores-aws/#iam-key)** (alternativa) – Para tanto, basta criar um usuário IAM do tipo “_Programmatic Access_” e com um política de segurança customizada que atenda a necessidade de seu negócio e processos.

Recomendamos que a primeira _Role_ a ser configurada seja em uma conta do tipo “_Management account_”. O procedimento de configuração de _role_ descrito abaixo deverá ser repetido em todas as contas da _Organization_.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-1024x407.png)

Antes de iniciar as configurações, sugerimos alterar as configurações de idioma para **EN-US**, a fim de facilitar a identificação das propriedades que serão configuradas. Na barra superior, selecione o ícone de engrenagem (Configurações) e altere o idioma para _English_ (US).

![](https://cloud8.io/wp-content/uploads/2025/08/change-language-1024x363.webp)

## Integrar uma conta da AWS usando _IAM Role_

Neste artigo, descrevemos o passo a passo para gerar o _IAM Role_. Sugerimos que abra um bloco de notas para anotar as informações necessárias para conexão do provedor junto a **Cloud8**. Esteja pronto para anotar as seguintes informações:

- AWS ACCOUNT ID (management account)
- ROLE NAME
- ROLE ARN
- EXTERNAL ID 
- CUR Export Name
- CUR Bucket S3
- CUR Bucket S3 Path Prefix

### Passo 1 – Criar uma nova _Role_ no Console AWS

Clique em “_Create role_”.

![](https://cloud8.io/wp-content/uploads/2025/08/create-role-1024x466.webp)

O ideal é primeiro criar uma _Managed Policy_ com as permissões que precisa. Veja uma sugestão. Não se preocupe se não souber todas as permissões, é possível mudá-la a qualquer momento.

### Passo 2 – Selecionar entidade confiável

Na tela seguinte selecione AWS account como “Trusted entity type”.

![](https://cloud8.io/wp-content/uploads/2025/08/select-trusted-entity-1024x283.webp)

Na seção abaixo, informe que é outra conta da AWS que terá acesso a essa _Role_. Selecione a opção “**_Another AWS account_**” e informe o ID da Cloud8: **693155863762**. Marque a opção **“_Require external ID_”** e defina o valor para _External ID_. Anote o _“External ID”_ no bloco de notas para utilizar posteriormente. 

**Nota**: para o _External ID_ utilize somente caracteres alfanuméricos. Como o usaremos via API, apesar do AWS permitir outros caracteres, eles não funcionam quando usados programaticamente.

Em seguida, clique em “**Next**”.

![](https://cloud8.io/wp-content/uploads/2025/08/trusted-aws-account-1024x463.webp)

### Passo 3 – Adicionar permissões

Agora é o momento de adicionar permissões a essa _Role_, liberando o acesso às áreas específicas de sua conta AWS. A _Policy_ mínima que o Cloud8 precisa é a “**_ReadOnlyAccess_**”. 

Caso esteja difícil identificar a policy, ordene a coluna policy name por ordem decrescente alfabética e a _policy_ “_ReadOnlyAccess_” será uma das primeiras. Em seguida, clique em “**Next**”.

![](https://cloud8.io/wp-content/uploads/2025/08/add-permissions-1024x464.webp)

É possível, na seção logo abaixo, definir um limite aos _Roles_ selecionados acima. Você pode selecionar um _Role_ menos rígido e aumentar a segurança removendo acessos desnecessários.

### Passo 4 –  Nomear Role e revisar as permissões antes de publicar

Sugerimos adotar a seguinte nomenclatura: cloud8-role. Anote o _“Role Name”_ no bloco de notas. Em seguida, clique em “**_Create role_**”.

![](https://cloud8.io/wp-content/uploads/2025/08/name-review-create-1024x262.webp)

Pronto! Sua _Role_ foi criada e ele pode ser vista e editada direto no Console.

![](https://cloud8.io/wp-content/uploads/2025/08/roles-console-1024x463.webp)

Clique na _role_ criada para visualizar as informações. Anote o “_Role ARN_” no bloco de notas.

![](https://cloud8.io/wp-content/uploads/2025/08/cloud8-access-1024x269.webp)

### Passo 5 – Configurando o provedor no Cloud8

No menu lateral esquerdo, selecione “**Providers**”. Clique em “**New**” e preencha os campos obrigatórios com os dados gerados nas etapas anteriores.

- **Provider name**: O nome que será utilizando para identificar o provedor na Cloud8.
- **Timezone**: padrão de tempo local que será utilizado.
- **Language**: idioma padrão.
- **Default location**: Escolha a localização mais popular ou mais utilizada pela sua conta, vamos varrer todas regiões e zonas de qualquer forma.
- **IAM Role ARN**: _Role ARN_ criada no Passo 4.
- **External ID**: _External ID_ criado no Passo 2.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-1.png)

Clique em “Register” e aguarde a sincronização dos dados.

## Integrar uma conta AWS usando uma IAM User Key

Neste artigo, descrevemos o passo a passo para gerar o _IAM User Key_. Sugerimos que abra um bloco de notas para anotar as informações necessárias para conexão do provedor junto a Cloud8. Esteja pronto para anotar as seguintes informações:

- AWS ACCOUNT ID (management account)
- ACCESS KEY
- SECRET ACCESS KEY
- CUR Export Name
- CUR Bucket S3
- CUR Bucket S3 Path Prefix

### Passo 1 – Criar uma Chave de Acesso no Console AWS

Acesse o Console da AWS, clique no menu do usuário (canto superior direito) e selecione a opção “_Security credentials_”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-2-1024x468.png)

Na tela seguinte, procure a sessão de “Access keys” e clique em “Create access key”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-3-1024x463.png)

Com a criação da _Access Key_ e o respectivo _Secret access key_, anote essas informações no bloco de notas.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-4-1024x439.png)

Recomenda-se fazer o download desses dados clicando em “Download .csv file”. Em seguida, encerre essa etapa clicando em “Done”.

### Passo 2 –  Configurando o provedor na Cloud8

No menu lateral esquerdo, selecione “**Providers**”. Clique em “**New**” e preencha os campos obrigatórios com os dados gerados nas etapas anteriores.

- **Provider name**: O nome que será utilizando para identificar o provedor na Cloud8.
- **Timezone**: padrão de tempo local que será utilizado.
- **Language**: idioma padrão.
- **Default location**: Escolha a localização mais popular ou mais utilizada pela sua conta, vamos varrer todas regiões e zonas de qualquer forma.
- **Access Key**: _Access Key_ criada no Passo 1.
- **Secret Key**: _Secret access key_ criado no Passo 1.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-1.png)

Clique em “_Register_” e aguarde a sincronização dos dados.

## Próximos passos

### Habilitação do ECS e EKS Split Cost

No Portal da AWS, na barra de pesquisa busque por **_Billing and Cost Management_**. No menu lateral esquerdo, selecione **_Cost Management Preferences_**, na aba de **_Preferences and Settings_**. 

Marque as opções **_Amazon Elastic Container Service (ECS)_** e **_Amazon Elastic Kubernetes Services (EKS)_** em _Split cost allocation data_. Em _Rightsizing_ selecione **_Enable Rightsizing recommendations_**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-5-1024x470.png)

Essa configuração no **_Billing and Cost Management_** é fundamental para melhorar a visibilidade e o controle dos custos em ambientes que utilizam **ECS** e **EKS**. Ao habilitar a opção **_Split cost allocation data_** para esses serviços, os gastos passam a ser discriminados de forma mais granular, permitindo identificar com clareza quais recursos e _workloads_ estão consumindo mais orçamento dentro dos clusters. 

Ativar o **_Enable Rightsizing recommendations_** garante que a AWS forneça sugestões automáticas de ajuste de tamanho das instâncias, ajudando a identificar oportunidades de otimização e redução de custos sem comprometer a performance. Clique em “**_Save Preferences_**”.

### Backfill do Histórico de custos 

A criação do CUR irá carregar dados a partir do primeiro dia do mês em que ele foi criado, portanto, caso você tenha criado no mês atual não terá o histórico disponível de meses anteriores. Será necessário abrir um chamado junto à AWS solicitando o _Backfill_ dos meses anteriores. É necessário aguardar 24 horas após a criação do CUR, e passar os dados necessários como o _Account ID_, _Export Name_, _Bucket_ e _S3 Path Prefix_.

Informe no chamado:

- Nome do _bucket_ S3
- Prefixo utilizado
- Export name do CUR
- Período desejado para o _backfill_ (datas de início e fim)
- Explique que precisa do _backfill_ dos dados históricos para o novo CUR.

Segue um modelo de texto para abertura de chamado de _backfill_ na AWS, adaptado para o contexto de solicitação de histórico do _Cost and Usage Report_ (CUR):

_**Assunto**: Solicitação de Backfill de Dados Históricos no AWS Cost and Usage Report (CUR)_

_**Descrição**:_

_Prezados,_

_Solicito o backfill dos dados históricos para o Cost and Usage Report (CUR) recém-configurado em nossa conta AWS. O objetivo é garantir que todos os dados de uso e custos anteriores estejam disponíveis no novo bucket configurado._

_Detalhes da configuração:_

- _Bucket S3: [NOME_DO_BUCKET]_
- _Prefixo: [PREFIXO_UTILIZADO]_
- _Export Name do CUR: [EXPORT_NAME]_
- _Período desejado para backfill: [DATA_INICIAL] até [DATA_FINAL] (recomendamos solicitar histórico desde janeiro do ano anterior para ter pelo menos um ano calendário completo)_

_O CUR já está ativo e o primeiro arquivo foi publicado com sucesso. Gostaríamos de solicitar que a AWS publique os dados históricos referentes ao período acima neste novo CUR._

_Caso seja necessário algum ajuste adicional na configuração ou envio de informações complementares, por favor, nos informe._

_Agradeço desde já pelo suporte._

_Atenciosamente,_

_[Seu nome]_

_[Seu contato]_

## Configurando o Cloud8 FinOps Analytics para AWS

A configuração do FinOps Analytics é realizada através da conexão com um bucket S3 que recebe os dados de uso e custo através de CUR.

### Configurando Billing Export (CUR) na AWS

Um _Cost and Usage Reports_ (CUR) é um conjunto de dados de uso e custo detalhados. É utilizado para exportar dados de billing para um _bucket_ S3, permitindo integração completa com a ferramenta da Cloud8. É possível solicitar um _backfill_ de dados de períodos anteriores à criação do CUR, permitindo uma visão histórica do consumo dos provedores da AWS.

#### Pré-requisitos

Possuir acesso administrativo na _Management Account_ da _Organization_.

### Configurando um novo arquivo CUR

No Portal da AWS, na barra de pesquisa busque por **_Cost and Usage Reports_**. Em seguida, clique em **_Create_**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-6-1024x460.png)

Em seguida, selecione **_Legacy CUR export_**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-7-1024x290.png)

- **_Export name_:** Nomeie o relatório e anote no bloco de notas.
- Selecione a opção “**_Include resource IDs_**”
- Selecione a opção “**_Split cost allocation data_**”.
- Selecione a opção “**_Refresh automatically_**”

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-8-1024x465.png)

Na configuração “_Data export delivery options_”, faça as seguintes configurações:

- **_Report data time granularity_**: o período necessário para agregação dos dados no relatório, podendo ser por hora, diariamente ou mensalmente (não recomendado). Recomenda-se a configuração “_Hourly_”.
- **_Report versioning_**: definir se as versões mais atuais do CUR substituam as versões anteriores ou sejam entregues juntamente com as versões anteriores. Recomenda-se “_Create new report version_”.
- **_Report data integration_**: pode deixar a configuração sem seleção, pois precisamos do formato CSV.
- **_Compression type_**: selecione ZIP ou GZIP.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-9-1024x414.png)

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-10-1024x465.png)

Em **_Data export storage settings_**, clique em **_Configure_**. Caso opte por criar um novo _bucket_ preencha os dados de “_S3 bucket name_” e selecione uma “_Region_”. Sugerimos adotar o nome “**cloud8-bucket**”. Em seguida, clique em “**_Create bucket_**”. Anote o nome do _bucket_ S3 no bloco de notas.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-11.png)

Caso tenha decidido utilizar um _bucket_ já existente, clique em **_Select existing bucket_**, e selecione o bucket desejado. Tendo em vista a possibilidade das políticas serem incompatíveis com o bucket selecionado, será necessário marcar o campo **“_I agree to overwrite my S3 bucket policy_”**. Clique em **_Select bucket_**. Anote o nome do bucket S3 no bloco de notas.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-12.png)

Independente de qual das opções de configuração for adotada, preencha “**_S3 path prefix_**” com o valor desejado para prefixo do seu _data export_. Sugerimos utilizar “**cloud8-prefix**”. Anote o S3 path prefix no bloco de notas.

Valide as informações e clique em **_Create Report_**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-13-1024x465.png)

### Editar arquivo CUR pré-existente

É possível que já exista um arquivo CUR anteriormente configurado. Neste caso o usuário terá a opção de editar as configurações da configuração existente.

**Atenção**! Essa ação não é recomendada caso o CUR existente esteja sendo utilizado por outras aplicações ou serviços, o que poderá desconfigurar sistemas que façam utilização do mesmo.

No Portal da AWS, na barra de pesquisa busque por **_Cost and Usage Reports_**. Em **_Exports and Dashboards_** selecione o relatório desejado.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-14-1024x460.png)

Em seguida, clique em **Edit**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-15-1024x430.png)

Altere os campos necessários, em seguida clique em **Edit Report**.

**OBS:** As alterações efetuadas no CUR não terão efeitos retroativos, e passarão a funcionar a partir do mês em que a alteração foi realizada.

### Cadastrando o CUR na Cloud8

No menu lateral da Cloud8 selecione FinOps Analytics. Selecione o provedor AWS anteriormente configurado no menu superior. Será exibida uma imagem na tela com a mensagem “**Habilite os detalhes de custos para ter acesso a análise! Clique aqui!**”. 

Em Habilitar gestão de custos, informe:

- **_Bucket with billing data_**: Informe o Bucket name.
- **_Report path prefix/Export name_**: Informe a combinação do S3 path prefix + Export name no formato **<_S3 path prefix_>/<_Export name_>**. 

Em seguida, clique em “Habilitar”.

**Observação:** Caso o CUR tenha acabado de ser criado, será necessário aguardar ao menos 24 horas para poder adicioná-lo no Cloud8.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-16-1024x471.png)

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-17.png)

Após a configuração levará algumas horas para que os dados sejam processados e publicações na aplicação da Cloud8.

## Habilitando Melhores Práticas na Cloud8

Após a configuração do _FinOps Analytics_ ser concluída e os dados já estiverem sincronizados na Cloud8, será possível habilitar a função de **Melhores Práticas** na Cloud8.

O **_Best Practices_** é um consultor avançado que combina mais de 1.000 regras exclusivas de segurança, backup, conformidade e redução de custos para AWS, Azure, GCP e OCI com alertas flexíveis via Teams, Slack ou e-mail.

No menu lateral da Cloud8 selecione **_Providers_**. Selecione o provedor desejado e clique em “**_Best Practices_**”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-18-1024x490.png)

Você deverá selecionar os provedores nos quais deseja habilitar a funcionalidade, e para isso, desmarque a checkbox “**_Disabled on this provider_**” e selecione a opção “**_Same as main credentials_**”.

Em seguida clique em “**Configure**”.

**Observação:** Caso o FinOps Analytics tenha acabado de ser habilitado, será necessário aguardar ao menos 24 horas para poder habilitar a funcionalidade do Melhores Práticas.

### Habilitando o Cost Optimization Hub

No Portal da AWS, em _Billing and Cost Management_ / _Cost Management Preferences_ selecione a aba **_Cost Optimization Hub_.** Esta funcionalidade é necessária para habilitar recomendações de otimização de custos de diversos serviços AWS através de ações como _rightsizing_ ou adoção de descontos baseados em compromisso, como o _Savings Plans_. 

Selecione a opção **_Enable Cost Optimization Hub for this account  and all member accounts_**, e em seguida clique em **_Enable_**.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-19-1024x462.png)

### Habilitando o AWS Compute Optimizer

No Portal da AWS, na barra de pesquisa busque por **_AWS Compute Optimizer_**. Este recurso usará _machine learning_ para analisar métricas relevantes do _CloudWatch_ e dados de configuração de recursos (como identificadores de recursos e tags de metadados) referentes a serviços específicos para as recomendações feitas. Clique em “**_Get started_**”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-20-1024x440.png)

Você pode ativar o **_Cost Optimization Hub_ diretamente pela organização (_management account_)** e habilitar para **todas as contas membro de uma vez**, ou optar por ativar **conta a conta** de forma individual.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-21-1024x463.png)

Em Preferências de _opt-in_ selecione **Todas as contas-membro desta organização**, e em seguida clique em **Fazer _opt-in_**.

## Adicionando credenciais de administração na AWS para Cloud8

O Cloud8 suporta o uso de IAM para o AWS com uma credencial customizada de segurança. Isso permite garantir privilégio mínimo ao integrar o Cloud8 com sua conta AWS. Essas credenciais normalmente incluem:

- Access Key
- Permissões mínimas necessárias
- Suporte para login com MFA
- Registro de logs de auditoria

Em IAM, acesse _Policies_. Em seguida, clique em “**_Create policy_**”. Na aba JSON é possível selecionar quais operações serão autorizadas, com base no Tipo de Recurso. Além disso, também é possível selecionar quais recursos serão impactados.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-22-1024x433.png)

Ao selecionar uma ação, a ferramenta automaticamente altera o JSON para incluir as permissões selecionadas. Em “**_Add resource_**”, selecione “_All resources_” em _Resource Type_. Após configurar todo o JSON, clique em “**_Next_**”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-23-1024x413.png)

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-24.png)

Na aba “**_Review & Create_”** adicione um “_Policy Name_” para identificar a política criada e atribuí-la posteriormente. Em seguida, clique em **“_Create policy_**”.

![](https://www.cloud8.com.br/wp-content/uploads/2021/06/image-25-1024x461.png)

Abaixo estão alguns modelos de permissão adotados na Cloud8:

```
{
  "Version": "2012-10-17",
  "Statement": [
  {
    "Effect": "Allow",
    "Action": [
       "ec2:Describe*",
       "ec2:CreateImage",
       "ec2:CreateSnapshot",
       "ec2:ModifyInstanceAttribute",
       "ec2:AssociateAddress",
       "ec2:RebootInstances",
       "ec2:StartInstances",
       "ec2:StopInstances",
       "ec2:CreateTags",
       "ec2:DeleteTags",
       "rds:Describe*",
       "rds:StartDBInstance",
       "rds:StopDBInstance",
       "rds:StartDBCluster",
       "rds:StopDBCluster",
       "rds:Download*",
       "rds:ListTagsForResource",
       "rds:ModifyDBInstance*",
       "rds:CreateDBSnapshot*",
       "ssm:Describe*",
       "savingsplans:Describe*",
       "elasticache:Describe*",
       "elasticloadbalancing:Describe*",
       "elasticbeanstalk:Describe*",
       "autoscaling:Describe*",
       "ecs:Describe*",
       "ecs:List*",
       "eks:Describe*",
       "eks:List*",
       "cloudtrail:DescribeTrails",
       "cloudtrail:GetTrailStatus",
       "cloudtrail:Look*",
       "cloudfront:Describe*",
       "cloudfront:Get*",
       "cloudfront:List*",
       "storagegateway:Describe*",
       "storagegateway:List*",
       "es:Describe*",
       "es:List*",
       "elasticache:Describe*",
       "elasticache:List*",
       "redshift:Describe*",
       "workspaces:Describe*",
       "lightsail:Get*",
       "lambda:Get*",
       "lambda:List*",
       "tag:get*",
       "trustedadvisor:Describe*",
       "support:Describe*",
       "iam:Get*",
       "iam:List*",
       "iam:Generate*",
       "organizations:Describe*",
       "organizations:List*",
       "route53:Get*",
       "route53:List*",
       "cloudwatch:Get*",
       "cloudwatch:List*",
       "kms:List*",
       "kms:Describe*",
       "sns:ListSubscriptions*",
       "sns:CreateTopic",
       "sns:Subscribe",
       "sns:ConfirmSubscription",
       "rds:CreateEventSubscription"
    ],
       "Resource": "*"
  },
  {
    "Action": [
       "s3:ListAllMyBuckets"
    ],
    "Effect": "Allow",
    "Resource": "arn:aws:s3:::*"
  },
  {
    "Action": [
       "s3:ListBucket",
       "s3:GetBucketLocation"
    ],
    "Effect": "Allow",
    "Resource": "arn:aws:s3:::___bucket_name___"
  },
  {
    "Action": [
       "s3:GetObject"
    ],
    "Effect": "Allow",
    "Resource": "arn:aws:s3:::___bucket_name___/*"
  }
  ]
}
```

**Restringir Start/Stop a um conjunto específico de recursos agrupados por _tags_:**

```
{
   "Effect": "Allow",
   "Action": [
       "ec2:RebootInstances",
       "ec2:StartInstances",
       "ec2:StopInstances"
   ],
   "Resource": "arn:aws:ec2:*:*:instance/*",
   "Condition": {
       "StringEquals": {
             "ec2:ResourceTag/Cloud8": "Enable"
       }
   }
},
```

**Limpeza de backup/Política de Retenção que apaga AMI/Snapshots segundo regras (insira no primeiro bloco com as permissões gerais):**

```
…ec2:DeregisterImageec2:DeleteSnapshotrds:DeleteDBSnapshotrds:DeleteDBClusterSnapshotlightsail:DeleteInstanceSnapshot…
```

**Copiar para outra região:**

```
…ec2:CopyImagerds:CopyDBSnapshotrds:CopyDBClusterSnapshot…
```

**Economia e backup do RDS:**

```
…rds:ModifyDBInstance*rds:CreateDBSnapshot*rds:CreateDBClusterSnapshot*…
```

**Monitoramento e eventos RDS:**

```
…sns:Describe*sns:ListSubscriptions*sns:CreateTopicsns:Subscribesns:ConfirmSubscriptionrds:CreateEventSubscription…
```

**Executando scripts via EC2 Commands:**

```
…ssm:List*ssm:Get*ssm:SendCommand…
```

**Cópia de segurança (cofre) para outra conta origem:**

```
…ec2:ModifyImageAttributeec2:ModifySnapshotAttributerds:ModifyDBSnapshotAttributerds:ModifyDBClusterSnapshotAttribute…
```

**Conta de destino:**

```
…ec2:CopyImageec2:CopySnapshotrds:CopyDBSnapshotrds:CopyDBClusterSnapshot…
```

**Redução de custos em Auto Scaling e Beanstalk:**

```
…elasticbeanstalk:Update*autoscaling:Update*…
```

**Redução de custos em ECS e Fargate:**

```
…ecs:Describe*ecs:Update*…
```

**Redução de custos no OpenSearch / ElasticSearch:**

```
…ess:Update*…
```

**Load Balancer:**

```
…elasticloadbalancing:RegisterInstancesWithLoadBalancerelasticloadbalancing:DeregisterInstancesFromLoadBalancerelasticloadbalancing:RegisterTargetselasticloadbalancing:DeregisterTargets…
```

**Edição de tags:**

```
…tag:*ec2:CreateTagsec2:DeleteTagsrds:AddTagsToResourcerds:RemoveTagsFromResourceelasticloadbalancing:RemoveTagselasticloadbalancing:AddTagsroute53:ChangeTags*dynamodb:Tag*dynamodb:Untag*logs:Tag*logs:Untag*eks:Tag*eks:Untag*elasticache:RemoveTagsFromResourceelasticache:AddTagsToResources3:DeleteObjectTaggings3:DeleteJobTaggings3:PutBucketTaggings3:DeleteStorageLensConfigurationTaggings3:ReplicateTagss3:PutStorageLensConfigurationTaggings3:PutObjectVersionTaggings3:PutObjectTaggings3:PutJobTaggings3:DeleteObjectVersionTaggingdms:RemoveTagsFromResourcedms:AddTagsToResource…
```

**Alteração do tipo de disco:**

```
…ec2:ModifyVolume*…
```

**Redução de custos com Redshift:**

```
…redshift:Pause*redshift:Resume*…
```

**Redução de custos com Workspaces:**

```
…workspaces:Stop*workspaces:Start*…
```

**Suporte ao Lightsail:**

```
…lightsail:Describe*lightsail:Get*lightsail:Stop*lightsail:Start*lightsail:Reboot*lightsail:Create*lightsail:Copy*…
```

Agora basta atribuir a política criada à Função (Role) configurada para acesso do Cloud8.