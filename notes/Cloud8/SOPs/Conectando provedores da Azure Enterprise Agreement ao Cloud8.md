#cloud8 #azure 
## Introdução

Em uma [[Azure]] _Account_ que faça parte de um _Enterprise Agreement_ (EA), será necessário configurar a integração com o [[Cloud8]] em cada _Subscription ID_ que faça parte do _Tenant ID_ (_Directory_) e também no nível de _Enterprise Administrator_ do EA.

Para conectar uma conta Azure com contrato Enterprise Agreement (EA) ao Cloud8 é necessário:

- Criar um Service Principal (App Registration)
- Atribuir a role de Reader em cada Subscription
- Atribuir ao Service Principal a role Enrollment Reader no nível da Billing Account (EA)

Para começar, pesquise por **_Microsoft Entra ID_**, e acesse a aba _Overview_. Anote o _Tenant ID_.

Sugerimos que deixe o bloco de notas aberto para registrar as seguintes informações:

- **_SUBSCRIPTION ID_** (Passo 1)
- **_SECRET VALUE_** (Passo 2)
- **_APPLICATION ID_** (Passo 2)
- **_TENANT ID_** (Passo 2) 
- **_ENTERPRISE APPLICATION ID_** (Passo 4)
- **_ENTERPRISE APPLICATION OBJECT ID_** (Passo 4)
- **_BILLING ACCOUNT ID_** (Passo 5)
- **_GUID_** (Passo 5)

### Pré-requisitos

- Mude o idioma para _English_ no menu superior, clicando no ícone de _Settings_. Em seguida, selecione _Language + Region_ e escolha _**English**_ em _Language_.
- O usuário precisa ser _**Global Administrator**_ no _Tenant_ onde a configuração será realizada.. 
- O usuário precisa ser _**Enterprise Administrator**_ na conta de _Enterprise Agreement_.

### Como verificar se o usuário possui a _role_ _Enterprise Administrator_ 

No **Portal Azure**, pesquise por “_**Cost Management + Billing**_”. Na aba _Billing Scopes_ verifique se o usuário possui acesso a **_Billing Account_** ou se o usuário é _**Enterprise Administrator**_ em _My role_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-01.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Para configurar o acesso de _Enterprise Administrator_, outro usuário com acesso de _Enterprise Administrator_ precisa conceder acesso. Para isto, selecione _**Billing Account**_ e clique em _**Access Control**_ (IAM).

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-02.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Clique em **_Add_** e selecione a _role_ _**Billing Account Administator**_. Em **_User, groups, or apps_** selecione o usário que receberá a _role_ e clique em **_Add_**.

### Como verificar se o usuário possui a role Global Administrator 

Na barra de pesquisa superior, busque por “_**Microsoft Entra ID**_”. Em _Overview_ verifique se o usuário possui a _role_ **_Global Administrator_** na sessão de _My Feed_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-03.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Para configurar o acesso de _Global Administrator_, outro usuário com acesso de _Global Administrator_ precisa conceder a _role_ usando o **_Microsoft Entra ID_**. Ao clicar em _**Users**_ você será direcionado para lista de usuários da conta.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-04.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Selecione o usuário que receberá a nova _role_ e clique em **_Assigned roles_**. Em seguida, clique em **_Add assignments_**, busque por **_Global Administrator_** e conclua clicando em _Add_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-05.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

### Passo 1 – Selecionando a Subscription

Na barra de pesquisa superior, procure por “**_Subscription_**”. Selecione a _Subscription_ e anote o _**Subscription ID**_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-06.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

### Passo 2 – Configurar o App Registration

Na barra de pesquisa superior, procure por **_App Registrations_**. Clique em _App Registration_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-07.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Clique em “**_New registration_**” e defina um nome.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-08.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Selecione o _App Registration_ criado e clique em _**Certificates & Secrets**_ no menu lateral esquerdo. Em seguida, clique em **_New Client Secret_**. Escolha um nome para a chave e selecione a data de expiração para 24 meses.

Após a criação, o provedor será configurado usando o **_Secret Value_**. Anote-o imediatamente após a criação, pois ele não estará mais visível.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-09.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Ainda em _App Registration_, anote o _**Application ID**_ e o _**Tenant ID**_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-10.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

### Passo 3 – Conceda as permissões necessárias ao _App Registration_

Busque novamente por **_Subscription_** e clique em _**Access control**_ (IAM) no menu lateral esquerdo da _Subscription_, em seguida clique em **_Add_** > _**Add role assignment**_.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-11.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Selecione as roles **_Reader_**, **_Billing_** **_Reader_** e **_Reservation Reader_**, em seguida clique _**Next**_:

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-12.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Na aba **_Members_**, clique em _**Select members**_, em seguida procure pelo _App Registration_ que foi criado. Em seguida clique em **_Review + assign_**:

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-13.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

**OBS**: Esse procedimento deverá ser realizado em cada _Subscription_.

### Passo 4 – Configurar a Enterprise Application (Somente em Enterprise Agreement)

Em seguida, busque por _**Enterprise Applications**_ na barra de pesquisa superior. Selecione a _Enterprise Application_ definida no **Passo 2**. Sempre que um _App Registration_ é criado, automaticamente gera um _Enterprise Application_.

Anote no bloco de notas o **_Name_, _Enterprise Application ID_ e o _Enterprise Object ID_.**

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-14.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

### Passo 5 – Atribua permissões de _Enrollment Reader_ ao _Service Principal_ somente em _Enterprise Agreement_

Na barra de pesquisa superior busque por **_Cost Management + Billing_**. Em **_Overview_**, anote o **_Billing Account ID_**.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-15.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Com os dados coletados, o próximo passo é atribuir as permissões de API necessárias para a ferramenta. O primeiro passo é gerar em **GUID**, usando o comando **_New-Guid_** no _PowerShell_ ou através do website [Online GUID/ UUID Generator](https://guidgenerator.com/). Usando o website, clique em **_Generate some GUIDs_!**

**Anote o GUID gerado. Vamos chamá-lo de GUID-NOVAPERMISSAO**

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-16.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

O GUID servirá como um identificador único e imutável para garantir unicidade dentro da Azure, sendo vital para controle de acessos, automações, logs e governança.

Em seguida, use o  [Role Assignments Put REST API do EnrollmentReader](https://learn.microsoft.com/en-us/rest/api/billing/role-assignments/put?view=rest-billing-2019-10-01-preview&tabs=HTTP). Clique em **_Try it_**.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-17.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Preencha os campos com as seguintes informações:

- **billingAccountName**: _BILLING ACCOUNT ID_ (Passo 5)
- **billingRoleAssignmentName**: _GUID_NOVAPERMISSAO_
- **Body**: preencha conforme o modelo abaixo.

```
{
  "properties": {
    "principalId": "<ENTERPRISE APPLICATION OBJECT ID>",
    "principalTenantId": "<TENANT ID>",
    "roleDefinitionId": "/providers/Microsoft.Billing/billingAccounts/<BILLING ACCOUNT ID>/billingRoleDefinitions/24f8edb6-1668-4659-b5e2-40bb5f3a7d7e"
  }
}
```

Para o body:

- **<ENTERPRISE APPLICATION OBJECT ID> =>** Obtido no Passo 4
- **<TENANT ID> =>** Obtido no Passo 2
- **<BILLING ACCOUNT ID> =>** Obtido no Passo 5

Em seguida clique em **_Run_** para executar a atribuição. Valide o resultado através do **_Response Code 200_**.

Feito! Você configurou o **_Service Principal_** e está pronto para associá-lo a **Cloud8**. Preencha com os dados coletados nas etapas anteriores:

- **Subscription ID** = _SUBSCRIPTION ID_
- **Tenant ID** = _TENANT ID_
- **Application ID** = _APPLICATION ID_
- **Senha** = _SECRET VALUE_

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-18.webp)

# Configurando o FinOps Analytics no Cloud8

Essa etapa é manual e feita por nossa equipe. Envie um email para [suporte@cloud8.com.br](mailto:suporte@cloud8.com.br) informando que os processos de configuração do EA _Enrollment Reader_ foram completados com sucesso (**200 code**).

# Habilitando o _Best Practices_ no Cloud8

Após a configuração do _FinOps Analytics_ ser concluída e os dados já estiverem sincronizados na Cloud8, será possível habilitar a função de **Melhores Práticas** na Cloud8.

O **_Best Practices_** é um consultor avançado que combina mais de 1.000 regras exclusivas de segurança, backup, conformidade e redução de custos para AWS, Azure, GCP e OCI com alertas flexíveis via Teams, Slack ou e-mail.

No menu lateral da Cloud8 selecione **_Providers_**. Selecione o provedor desejado e clique em “_**Best Practices**_”.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-19.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Você deverá selecionar os provedores nos quais deseja habilitar a funcionalidade, e para isso, desmarque a checkbox “**_Disabled on this provider_**” e selecione a opção “**_Same as main credential_s**”.

![Conectando provedores da Azure Enterprise Agreement ao Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/10/azure-20.webp "Conectando provedores da Azure Enterprise Agreement ao Cloud8")

Em seguida clique em “**_Configure_**”.

**OBS:** Caso o _FinOps Analytics_ tenha acabado de ser habilitado, será necessário aguardar ao menos 24 horas para poder habilitar a funcionalidade do **Melhores Práticas**.