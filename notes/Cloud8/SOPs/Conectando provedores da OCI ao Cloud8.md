#cloud8 #oci 

Para integrar uma conta **Oracle Cloud (OCI)** na Plataforma Cloud8, você precisa fornecer uma credencial de acesso nas configurações de sua conta conosco. Faça essa configuração do início ao fim através do tutorial abaixo.

## Configurando as credenciais de acesso OCI

 Sugerimos que abra um bloco de notas e esteja pronto para anotar os seguintes dados:

- CONFIGURATION FILE PREVIEW (**PASSO 1**)
- GROUP NAME (**PASSO 2**)
- PEM (**PASSO 2**)

Inicialmente, sugerimos verificar a estrutura da **_Organization_** da OCI. Na barra de pesquisa superior, busque por **_Tenancies_**. A configuração deverá ser realizada primeiro na **_Parent tenancy_ da _Organization_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-01.webp "Integrando OCI com Cloud8")

Em seguida, valide a existência de **CUR** (**Cost and Usage Report**), pesquisando por “_Cost and Usage Reports_” na barra superior de pesquisa.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-02.webp "Integrando OCI com Cloud8")

### Passo 1 – Criando um usuário 

Em seguida, na barra de pesquisa superior, busque por _Domains_ e selecione o _Default domain_. Na aba **_User management_**, encontre _Users_ e clique em **_Create_**. Sugerimos adotar o nome de usuário Cloud8.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-03.webp "Integrando OCI com Cloud8")

Defina **_First name_**, **_Last name_** e _**Username/Email.**_ Sugerimos utilizar um email através do qual você consiga resetar informações, se necessário. Em seguida, clique em **_Create_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-04.webp "Integrando OCI com Cloud8")

Em seguida, crie uma **_API Key_** para o usuário criado, clicando na aba _API Key_ e em seguida em _**Add API key**_.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-05.webp "Integrando OCI com Cloud8")

Selecione a opção **_Generate API key pair_**, e faça o download da _private key_ e da _public key_.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-06.webp "Integrando OCI com Cloud8")

Sugerirmos armazenar as _API keys_ baixadas em um repositório seguro ou cofre, caso seja necessário utilizá-las posteriormente. Por fim, clique em **_Add_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-07.webp "Integrando OCI com Cloud8")

Copie o conteúdo do _Configuration file preview_ e salve em um bloco de notas.

### Passo 2 – Crie um Grupo de Acesso

Retorne para **_Domains_**, selecione novamente o _Default domain_, e na aba de _User Management_, role para baixo até encontrar **_Groups_**. Clique em **_Create group_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-08.webp "Integrando OCI com Cloud8")

Selecione um nome para o grupo e o usuário criado na etapa anterior. Em seguida, clique em **_Create_**. Anote o _Name_ do grupo no bloco de notas para uso posterior.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-09-1024x476.webp)

### Passo 3 – Criar um Policy de acesso

No menu lateral esquerdo, selecione **_Policies_**, e clique em **_Create Policy_** no _root compartment_.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-10-1024x475.webp)

Defina um nome para a _policy_ e selecione o _Root Compartment_.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-11-1024x242.webp)

Na sessão de **_Policy Builder_**, clique em **_Show manual editor_**. Em seguida, copie a definição de _policies_ abaixo:

```
define tenancy usage-report as ocid1.tenancy.oc1..aaaaaaaaned4fkpkisbwjlr56u7cj63lf3wffbilvqknstgtvzub7vhqkggq
Allow group __MEUGROUP__ to read all-resources in tenancy
endorse group __MEUGROUP__ to read objects in tenancy usage-report
```

**IMPORTANTE:** Não altere o código de _tenancy_ acima, pois ele é padrão da Oracle.

Troque **==__MEUGROUP__==** pelo nome do _Group_ que foi criado na etapa anterior, em seguida clique em **_Create_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-12.webp "Integrando OCI com Cloud8")

### Passo 4 – Configurando as credenciais de acesso na Cloud8

No menu lateral esquerdo, selecione “**_Providers_**”. Clique em “**_New_**” e preencha os campos obrigatórios com os dados gerados nas etapas anteriores.

- **_Provider name_**: O nome que será utilizando para identificar o provedor na Cloud8.
- _**Timezone**_: padrão de tempo local que será utilizado.
- **_Language_**: idioma padrão.
- **_Default location_**: Escolha a localização mais popular ou mais utilizada pela sua conta, vamos varrer todas regiões e zonas de qualquer forma.
- **_User_**: Disponível no _CONFIGURATION FILE PREVIEW_ (**Passo 1**)
- **_Tenancy_**: Disponível no _CONFIGURATION FILE PREVIEW_ (**Passo 1**)
- **_Fingerprint_**: Disponível no _CONFIGURATION FILE PREVIEW_ (**Passo 1**)
- **_PEM_**: a _private key_ do usuário criada no **Passo 1**

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-13.webp "Integrando OCI com Cloud8")

Clique em **_Register_**, e aguarde a Sincronização concluir.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-14.webp "Integrando OCI com Cloud8")

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-15-1024x479.webp)

## Permissões específicas para automações

Alguns módulos da Cloud8 dependem da concessão de permissões específicas. Adicione-as editando os _Statements_ da _Policy_ criada, clicando em **_Edit Policy_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-16.webp "Integrando OCI com Cloud8")

Clique em **_Aditional rule_**, adicione as permissões necessárias e clique em **_Save changes_**.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-17.webp "Integrando OCI com Cloud8")

### Ligar / Desligar / Upgrade / Downgrade de Instâncias

```
Allow group __MEUGROUP__ to manage instance-family in tenancy where any {request.permission='INSTANCE_POWER_ACTIONS', request.permission='INSTANCE_UPDATE'}
```

### Backup

```
Allow group __MEUGROUP__ to manage volume-family in tenancy where any {request.permission='VOLUME_BACKUP_CREATE', request.permission='VOLUME_WRITE', request.permission='VOLUME_UPDATE', request.permission='VOLUME_BACKUP_DELETE', request.permission='BOOT_VOLUME_BACKUP_CREATE', request.permission='BOOT_VOLUME_BACKUP_DELETE', request.permission='VOLUME_GROUP_BACKUP_CREATE', request.permission='VOLUME_GROUP_BACKUP_DELETE'}
```

### MySQL – Ligar / Desligar

```
Allow group __MEUGROUP__ to manage mysql-family in tenancy where any {request.permission='MYSQL_INSTANCE_USE', requesAllow group __MEUGROUP__ to manage database-family in tenancy where any {request.permission='DB_NODE_POWER_ACTIONS', request.permission='DB_BACKUP_DELETE', request.permission='DB_BACKUP_CREATE'}
```

### DbSystems – Ligar / Desligar

```
Allow group __MEUGROUP__ to manage database-family in tenancy where any {request.permission='DB_NODE_POWER_ACTIONS', request.permission='DB_BACKUP_DELETE', request.permission='DB_BACKUP_CREATE'}
```

### Gerenciar Tags

```
Allow group __MEUGROUP__ to use tag-namespaces in tenancy
```

### OKE Cluster NodePools – Ligar / Desligar

```
Allow group __MEUGROUP__ to use subnets in tenancy
Allow group __MEUGROUP__ to use vnics in tenancy
Allow group __MEUGROUP__ to manage instance-family in tenancy
```

**IMPORTANTE:**

1 – A permissão ‘manage instance-family’ é necessária para _NodePools_.

2 – Para evitar misturar com instâncias que não sejam _Kubernetes_, recomendamos usar ‘in compartment <compartment-name>’ no lugar do tenancy inteiro.

### Instance Pools – Ligar / Desligar / Escalar (zero / +1)

```
Allow group __MEUGROUP__ to use instance-pools in tenancy
Allow group __MEUGROUP__ to manage compute-management-family in tenancy
```

**OBS:** A permissão ‘compute-management-family’ é necessária para escalar _Instance Pools_.

### Auto Scaling Groups Policy

```
Allow group __MEUGROUP__ to use auto-scaling-configurations in tenancy
Allow group __MEUGROUP__ to manage auto-scaling-configurations in tenancy
```

### Exadata –  Escalar número de OCPUs

```
Allow group __MEUGROUP__ to manage cloud-vmcluster in compartment <your_compartment_name> where any {request.permission='CLOUD_VM_CLUSTER_UPDATE', request.permission='CLOUD_EXADATA_INFRASTRUCTURE_UPDATE'}
```

### Autonomous DB – Ligar/Desligar

```
Allow group __MEUGROUP__ to use autonomous-databases in compartment <your_compartment_name> where any {request.permission='AUTONOMOUS_DATABASE_UPDATE'}
```

## Configurando o FinOps Analytics na Cloud8

A configuração do **_FinOps Analytics_** é realizada através um **_Cost and Usage Report_** configurado no provedor da Oracle. Essa configuração **é realizada automaticamente** na etapa anterior, através da _Policy_ de acesso configurada.

## Habilitando Boas Práticas na Cloud8

Após a configuração do **_FinOps Analytics_** ser concluída e os dados já estiverem sincronizados na Cloud8, será possível habilitar a função de **Boas Práticas na Cloud8**.

O _**Best Practices**_ é um consultor avançado que combina mais de 1.000 regras exclusivas de segurança, backup, conformidade e redução de custos para AWS, Azure, GCP e OCI com alertas flexíveis via Teams, Slack ou e-mail.

No menu lateral da Cloud8 selecione **_Providers_**. Selecione o provedor desejado e clique em “**_Best Practices_**”.

![Integrando OCI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/oci-cloud8-18.webp "Integrando OCI com Cloud8")

Você deverá selecionar os provedores nos quais deseja habilitar a funcionalidade, e para isso, desmarque a checkbox “**_Disabled on this provider_**” e selecione a opção “**_Same as main credentials_**”.

Em seguida clique em “**_Configure_**”.

**IMPORTANTE:** Após a habilitação do **_FinOps Analytics_**, será necessário aguardar ao menos 24 horas para habilitar a funcionalidade do **Melhores Práticas**.