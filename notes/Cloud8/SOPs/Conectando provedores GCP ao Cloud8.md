#cloud8 #gcp 
Para utilizar sua conta _Google Cloud_ (GCP) integrada à Plataforma Cloud8, você vai precisar fornecer uma credencial de acesso. Abaixo segue o passo a passo para criação de uma credencial para integrar a sua nuvem GCP ao Cloud8.

## Pré-requisitos

O usuário precisa ter as seguintes permissões para acessar o painel de gerenciamento de recursos da Organization:

- Resourcemanager.organizations.get
- resourcemanager.organizations.getIamPolicy

## Coletar ID da Organização

A primeira informação necessária para configuração é o ID da Organization. No topo da tela, clique no ícone à esquerda da bara de pesquisa e anote o ID da Organização em um bloco de notas.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-01.webp "Conectando provedores GCP ao Cloud8")

Caso o tipo de conta do usuário não possua Organization, mas apenas Projects, siga para o passo seguinte utilizando o projeto onde há BigQuery configurado para coletar os dados de billing export.

## Coletar Billing Account ID

No topo da tela, pesquise por Billing. No menu lateral esquerdo clique em “Account management”. Anote o Billing Account ID. A configuração do FinOps Analytics é realizada através de uma Table do BigQuery e mediante as permissões BigQuery Data Viewer e BigQuery Job User. 

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-02.webp "Conectando provedores GCP ao Cloud8")

Caso a sua conta possua diversos projetos e não possua uma Organization, pesquise por “Billing accounts” na barra de pesquisa superior. Na lateral esquerda haverá um expander chamado “Billing account”, clique nele e selecione a billing account desejada.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-03.webp "Conectando provedores GCP ao Cloud8")

No menu lateral esquerdo selecione “Billing export”. Caso “Detailed usage cost” esteja desabilitado, será necessário configurar a exportação. Para isso, clique em “Edit settings”.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-04.webp "Conectando provedores GCP ao Cloud8")

Selecione um Project no qual realizar a criação do export. Lembre-se de selecionar aquele no qual haja a maior parte dos dados de faturamento. Na opção de Dataset cliquem em ”Create new dataset”.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-05.webp "Conectando provedores GCP ao Cloud8")

Após a criação, clique e “Save” e prossiga para próxima etapa.

## Habilitar APIs

É importante habilitar as seguintes APIs em [https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/dashboard)

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-06.webp "Conectando provedores GCP ao Cloud8")

Clique em **Enable APIs and services**, e busque por:

- Cloud Resource Manager API
- Compute Engine API
- Cloud SQL
- Cloud Billing para utilizar o FinOps Analytics
- KMS API
- Recommender API

### **Passo 1 – Criar Service Account**

No menu de IAM & Admin, selecione Service Accounts. Clique em **Create Service Account**: [https://console.developers.google.com/iam-admin/serviceaccounts](https://console.developers.google.com/iam-admin/serviceaccounts/project)

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-07.webp "Conectando provedores GCP ao Cloud8")

Em regra essa configuração é feita na Organization.

**OBS:** Em alguns casos é necessário criar a Service Account dentro de um projeto e depois atribuir permissões dentro da Organization, quando não for possível criar diretamente na mesma.

Para isso, clique em IAM dentro da Organization e selecione “Grant access”. 

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-08.webp "Conectando provedores GCP ao Cloud8")

Preencha os campos de Service account name, Service account ID. 

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-09.webp "Conectando provedores GCP ao Cloud8")

### **Passo 2 – Garantir as permissões de acesso necessárias**

Na aba **Permissions**, clique em **Manage access**, e em seguida em **Add role**

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-10.webp "Conectando provedores GCP ao Cloud8")

As **Roles** dependem do tipo de ação que o usuário deseja que a Cloud8 possa executar em seu ambiente, tais quais visualização de informações, backups, agendamentos para redução de custos, etc. Entre as roles disponíveis, sugerimos:

- _Browser_
- _Viewer_
- Billing Account Viewer
- _View Service Accounts_
- _Compute Viewer_;
- Cloud SQL Viewer;
- _Monitoring Viewer_;
- _BigQuery Data Viewer;_
- _BigQuery Job User_;
- _Kubernetes Engine Cluster Viewer_;
- _Cloud Asset Viewer_
- _Compute Recommender Viewer_
- _Cloud Functions Viewer_

No caso de um acesso mais avançado e com automatizações, serão necessárias as seguintes roles:

- _Browser_
- _Viewer_
- Billing Account Viewer
- _View Service Accounts_
- _Compute Engine_: _Compute Admin_ ou _Compute Viewer_;
- _Cloud SQL_: Cloud SQL Admin ou Cloud SQL Viewer;
- _Monitoring_: _Monitoring Viewer_;
- _BigQuery_: _BigQuery Data Viewer_ e _BigQuery Job User_;
- _Kubernetes_: _Kubernetes Engine Cluster Viewer_;
- _Cloud Asset Viewer_
- _Compute Recommender Viewer_
- _Cloud Functions Viewer_

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-11.webp "Conectando provedores GCP ao Cloud8")

Você pode pesquisar a Role desejada clicando em **Select a Role**, em seguida em **Filter by role or permission**

**Nota**: se o projeto for membro de um “_Organization_”, ele deverá ter os mesmos roles que o _Service Account_, caso contrário receberá a mensagem “_User is not Authorized_”.

### **Passo 3 – Criar JSON**

Precisamos de um arquivo JSON que contenha a _service account_. Para isso, na aba **Keys**, clique em **Add Key**, e em seguida **Create new key.**

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-12.webp "Conectando provedores GCP ao Cloud8")

Selecione **JSON**, logo após clique em **Create**. Uma Private Key será gerada automaticamente.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-13.webp "Conectando provedores GCP ao Cloud8")

### **Passo 4 – Habilitar JSON no cadastro de novo provedor.**

Copie o conteúdo do JSON no Portal Cloud8, e em seguida Cadastrar.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-14.webp "Conectando provedores GCP ao Cloud8")

## Configurando o FinOps Analytics na Cloud8

A configuração do FinOps Analytics é realizada através de uma Table do BigQuery e mediante as permissões BigQuery Data Viewer e BigQuery Job User. 

Pesquise Billing, e no menu lateral esquerdo selecione “Billing export”. Verifique se há um Detailed Billing Export. Caso não haja, será necessário criar um.

Busque por “Dataset name” do Detailed Usage Cost e anote. 

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-15.webp "Conectando provedores GCP ao Cloud8")

Clique no Dataset name para abrir a visualização de Tables. Copie e anote o nome da BigQueyTable ao expandir a visão do Dataset na esquerda.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-16.webp "Conectando provedores GCP ao Cloud8")

Na Plataforma da Cloud8, clique em FinOps Analytics, selecione o provider da GCP e configure informando o “Dataset Name” e o “BigQuery Table”.

## Habilitando Boas Práticas na Cloud8

Após a configuração do FinOps Analytics ser concluída e os dados já estiverem sincronizados na Cloud8, será possível habilitar a função de Boas Práticas na Cloud8.

O Best Practices é um consultor avançado que combina mais de 1.000 regras exclusivas de segurança, backup, conformidade e redução de custos para AWS, Azure, GCP e OCI com alertas flexíveis via Teams, Slack ou e-mail.

Antes de continuar valide se as APIs abaixo estão habilitadas:

- KMS API
- Recommender API

No menu lateral da Cloud8 selecione Providers. Selecione o provedor desejado e clique em “Best Practices”.

![Conectando provedores GCP ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/gcp-17.webp "Conectando provedores GCP ao Cloud8")

Você deverá selecionar os provedores nos quais deseja habilitar a funcionalidade, e para isso, desmarque a checkbox “**Disabled on this provider**” e selecione a opção “**Same as main credentials**”.

Em seguida clique em “**Configure**”.  
**Observação:** Caso o FinOps Analytics tenha acabado de ser habilitado, será necessário aguardar ao menos 24 horas para poder habilitar a funcionalidade do Melhores Práticas.