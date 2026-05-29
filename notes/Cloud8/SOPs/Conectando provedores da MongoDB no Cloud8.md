#cloud8 #sop 

O **MongoDB** é um banco de dados _NoSQL_ orientado a documentos, amplamente utilizado em aplicações modernas que exigem escalabilidade, alta performance e flexibilidade na modelagem de dados. Diferente de bancos relacionais tradicionais, ele armazena informações em documentos no formato JSON / BSON, facilitando a evolução do _schema_ e a integração com arquiteturas distribuídas e ambientes _cloud-native_.

A seguir, você encontrará o passo a passo completo para realizar a **integração de uma conta MongoDB à Plataforma Cloud8** de forma segura e estruturada.

## Passo 1: Acesse o Portal do MongoDB

Para coletar os dados necessários, acesse o [**MongoDB Atlas**](https://cloud.mongodb.com/). No menu lateral esquerdo, clique em **Organization Settings**. Anote o **Organization ID**.

![Conectando MongoDB](https://www.cloud8.com.br/wp-content/uploads/2026/02/conectando-mongo-01.webp "Conectando MongoDB")

## Passo 2: Gere uma API Key de acesso

A configuração dos custos da MongoDB é realizada através de uma _API Key_ de permissão restrita. No menu lateral esquerdo, clique em **Applications**, e na aba **API Keys** clique em **Create API Key**.

![Conectando MongoDB](https://www.cloud8.com.br/wp-content/uploads/2026/02/conectando-mongo-02.webp "Conectando MongoDB")

Nomeie a _API Key_ (sugerimos **Cloud8**) e em **Organization Permissions** selecione **Organization Member** e **Organization Billing Viewer**. 

![Conectando MongoDB](https://www.cloud8.com.br/wp-content/uploads/2026/02/conectando-mongo-03.webp "Conectando MongoDB")

Na tela seguinte anote a _public key_ e a _private key_ geradas. **Salve-as em um lugar seguro**. É importante ressaltar que não será possível visualizá-la novamente após clicar em **Done**.

## Passo 3: Configure o provedor na Cloud8

Em posse das _API Keys_ criadas, acesse a plataforma da Cloud8. No menu lateral esquerdo, selecione “**Providers**”. Clique em “**New**” e preencha os campos obrigatórios com os dados gerados nas etapas anteriores.

- **Provider name**: O nome que será utilizando para identificar o provedor na Cloud8.
- **Timezone**: padrão de tempo local que será utilizado.
- **Language**: idioma padrão.
- **Public Key**
- **Private Key**

Finalize clicando em **Cadastrar**.

![Conectando MongoDB](https://www.cloud8.com.br/wp-content/uploads/2026/02/conectando-mongo-04.webp "Conectando MongoDB")

**INFO:** A configuração do **FinOps Analytics** é realizada através da conexão via _API Key_ que recebe os dados de uso e custo via chamadas de API.