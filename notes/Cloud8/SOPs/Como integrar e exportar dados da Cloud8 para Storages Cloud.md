#finops #azure #aws #data_governance #data_analysis #gcp #cloud8 #finops 

A Cloud8 é uma plataforma que centraliza e enriquece dados provenientes de múltiplas contas e múltiplos provedores de nuvem, facilitando a análise e visualização de dados  tanto de forma isolada, quanto unificada. Para auxiliar nossos clientes a integrarem esses dados aos seus próprios sistemas de BI, relatórios personalizados ou painéis, oferecemos a possibilidade de exportação dos dados para contas de armazenamento dos principais provedores de nuvem.

Abaixo você vai encontrar os passos necessários para criar essa integração com **Amazon AWS**, **Google GCP** e **Microsoft Azure**. Pule diretamente para:

|   |   |   |
|---|---|---|
|![](https://www.cloud8.com.br/wp-content/uploads/2020/10/logo_aws-color.png)  <br>[Integração Cloud8 com AWS S3 Bucket](https://www.cloud8.com.br/ajuda/integracao-com-storages-cloud/#aws-bucket)|![](https://www.cloud8.com.br/wp-content/uploads/2020/10/logo_azure-color.png)  <br>[Integração Cloud8 com Azure Storage Account](https://www.cloud8.com.br/ajuda/integracao-com-storages-cloud/#azure-storage)|![](https://www.cloud8.com.br/wp-content/uploads/2020/10/logo_googlecloud-color.png)  <br>[Integração Cloud8 com GCP Cloud Storage](https://www.cloud8.com.br/ajuda/integracao-com-storages-cloud/#gcp-storage)|

[Exportando dados da Cloud8 para um Cloud Storage Account (todos os provedores suportados)](https://www.cloud8.com.br/ajuda/integracao-com-storages-cloud/#exportar-bucket)

---

## Como fazer uma integração com AWS S3 Bucket?

Abaixo está o passo-a-passo para integrar um S3 Bucket à sua conta Cloud8.

- Encontre no menu lateral a opção “**Integrações**“;
- Crie uma nova integração do Tipo “**_Bucket S3_**“;
- Indique o **nome do _Bucket S3_** definido na AWS no campo “**Bucket”**;
- Configure o par de acesso, IAM Role ARN e External ID, fornecidos pela AWS. Essa credencial deve possuir permissões de **criar e atualizar** arquivos em seu Bucket;
- Preencha as demais informações e finalize em **Gravar**
- Essa integração funciona também no **Melhores Práticas** e em “**Reports**” – pode-se criar o relatório para ser exportado

![Integração com AWS S3 (Bucket)](https://www.cloud8.com.br/wp-content/uploads/2024/07/blog-storage-s3.png "Cloud8 Integração com AWS S3 (Bucket)")

### IAM Role

Uma **IAM Role** é uma entidade no AWS IAM que define um conjunto de permissões para fazer solicitações aos serviços da AWS. Ao contrário de um usuário IAM, que é associado a uma pessoa, uma função IAM é destinada a ser assumida por qualquer entidade confiável, como um serviço AWS, um aplicativo, ou um usuário IAM. As funções são úteis para conceder permissões temporárias e podem ser assumidas por diferentes entidades conforme necessário.

### ARN (Amazon Resource Name)

O **ARN** é um identificador que segue um formato padrão e único para identificar recursos dentro da AWS. Ele é usado para especificar a função de maneira única em políticas e permissões.

#### Exemplo de Role ARN

```
arn:aws:iam::ID-NUMERICO-AWS:role/NOME-DO-ROLE
```

#### Uso de IAM Role ARN em S3

Quando você usa uma IAM Role com o S3, pode **conceder permissões específicas para acessar buckets e objetos S3**. Por exemplo, você pode criar uma função IAM com permissões para acessar um bucket S3 específico e depois configurar um serviço AWS (como EC2) ou um usuário IAM para assumir essa função. Isso é útil para gerenciar e controlar o acesso aos recursos S3 de forma segura e escalável.

#### Por que usar IAM Role ARN?

- **Segurança:** Permite conceder permissões temporárias, minimizando riscos.
- **Flexibilidade:** Pode ser assumida por várias entidades, facilitando a gestão de permissões.
- **Escalabilidade:** Ideal para grandes ambientes onde diferentes serviços e usuários precisam de acesso controlado.

---

## Como fazer uma integração com Azure Storage Account?

Caso você ainda não o tenha feito, o primeiro passo é criar uma _Storage Account_ na **Azure**. Para isso, na barra de pesquisa do painel Azure, busque por “_Storage accounts_”. Clique em “_**Create**_”. Na aba **_Basics_**, preencha as informações, defina a _Subscription_ e _Resource Group_ onde a conta de armazenamento será criada.

Defina um nome e região para criação do recurso, e em “_**Preferred storage type**_” escolha “**_Azure Blob Storage or Azure Data Lake Storage Gen 2_**”.

Em _Performance_, selecione “**_Standard_**”, e em _Redundancy_ selecione “_**Locally-redundant storage (LRS)**_”. Entretanto, trata-se de uma sugestão, e a definição da redundância deverá sempre acompanhar as regras de negócio do usuário.

![Integrando Azure Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-azure-storage-01.webp "Integrando GCP Storage")

Conclua clicando em “**_Review + create_**”. Valide os dados e clique em “_**Create**_”.

![Integrando Azure Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-azure-storage-02.webp "Integrando GCP Storage")

Pesquise pelo storage account criado. No menu lateral esquerdo, pesquise por “_**Containers**_”. Clique em “_**Add container**_”, defina um nome e clique em “**_Create_**”. **Anote o nome do container criado.**

![Integrando Azure Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-azure-storage-03.webp "Integrando GCP Storage")

No menu lateral esquerdo localize “_**Access keys**_”. Copie para um bloco de notas as seguintes informações:

- _Storage account name_
- _Key_

![Integrando Azure Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-azure-storage-04.webp "Integrando GCP Storage")

### Integrando o Storage Account com a Plataforma Cloud8

Siga os passos abaixo para criar uma integração dentro de nosso Painel MultiCloud com o Azure Storage Account.

- Encontre no menu lateral a opção “**Integrações**“
- Selecione “**Nova Integração**” na primeira opção
- Clique em “**Tipo**” e selecione a opção “**Azure Storage Account**“
- Dê um nome para essa integração
- Preencha os dados necessários: _**Storage Account Name**_, _**Storage Account Key**_ e _**Container**_

![Cloud8 new integration](https://www.cloud8.com.br/wp-content/uploads/2025/04/cloud8-integration.webp "Integrando Azure Storage")

---

## Como fazer uma integração com GCP Cloud Storage?

Caso ainda não tenha feito, primeiro você precisa criar o **GCP JSON** no _Service Account_. Para isso, acesse o Console da GCP e pesquise por **_IAM & Admin_**. Selecione **_Service Accounts_** no menu lateral esquerdo.

![Integrando GCP Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-gcp-storage-01.webp "Integrando GCP Storage")

Na aba **_Permissions_**, selecione **_Manage access | Add another role_** e escolha **_Storage Object Admin_**.

![Integrando GCP Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-gcp-storage-02.webp "Integrando GCP Storage")

Retorne para Service Accounts, e clique no ícone de três pontos para selecionar a opção **Manage Keys**. Clique em **Add key | Create new key** para criar uma nova chave de acesso, caso não a tenha criado ainda. Do contrário, basta a concessão dos acessos necessários na etapa anterior.

![Integrando GCP Storage](https://www.cloud8.com.br/wp-content/uploads/2025/11/integrando-gcp-storage-03.webp "Integrando GCP Storage")

Veja abaixo como integrar um GCP Cloud Storage à sua conta Cloud8.

- Encontre no menu lateral a opção “**Integrações**“;
- Crie uma nova integração do Tipo “**_GCP Cloud Storage_**“
- Adicione uma [credencial (arquivo _JSON_ de um _Service Account_)](https://www.cloud8.com.br/ajuda/conectando-provedores-gcp/) gerada na Access Key;
- Clique em “**Gravar**” e está pronto.

![Cloud8 integração com Storage GCP](https://www.cloud8.com.br/wp-content/uploads/2024/07/blog-storage-gcp.png "Cloud8 integração com Storage GCP")

---

## Como exportar dados da Cloud8 para um Storage Cloud

Os clientes Cloud8 muitas vezes possuem relatórios em diferentes formatos que precisam ser alimentados com os dados disponíveis em nossos reports. A forma mais simples de fazer isso é através de uma integração com um Storage Cloud. Veja abaixo como fazer essa extração em passos rápidos.

**NOTA**: No exemplo foi utilizado bucket S3 da AWS, mas o processo é igual para todos os providers suportados.

![Cloud8 pivot table](https://www.cloud8.com.br/wp-content/uploads/2025/04/cloud8-pivot-table-1.webp "Cloud8 pivot table")

- Clique em “**_FinOps – Reports_**“, em seguida em “**_Pivot Table_**” 
- Selecione o “**Provedor**“, “**Tags**“, **moeda** e **_markup_**
- Clique em “**_Refresh_**” para carregar o relatório com os filtros selecionados
- Utilize o botão “**Meus Dashboards**” e selecione “**Salvar Novo**”
- Dentro das opções exibidas, selecione a integração criada no passo anterior, para o provider escolhido
- **Não esqueça de salvar**

![Cloud8 Save new dashboard](https://www.cloud8.com.br/wp-content/uploads/2025/04/cloud8-pivot-table-dashboards.webp "Cloud8 Save new dashboard")

Após esses dois passos simples, o cliente receberá um arquivo completo e consistente em formato CSV, com o markup definido por ele, de 2 a 3 vezes por dia contendo todos os dados. 

Dessa forma não é necessária nenhuma integração por API, geração de credenciais, scripts, tratativas de erro, etc.

### Melhores Práticas

Em “**Relatórios**” você pode exportar todos os dados em formato JSON. Se escolher “**Imediatamente**“, iremos exportar sempre que um novo item entrar ou sair na regra. Dentro do JSON, encontra-se um “**_identifier_**” que pode ser usado na conciliação de um item que abriu e depois foi fechado (seja por que mudou a regra ou o cliente / parceiro consertou e assim pode usado para fechar automaticamente).

### Inventário

Para exportação de dados de **Inventário**, contate o Suporte para configurarmos internamente.