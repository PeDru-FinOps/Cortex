#cloud8 #ia #finops 

**Disclaimer**: Esta integração está em período de testes (Beta). Qualquer inconsistência que você encontrar, agradecemos se puder nos relatar. Se tiver qualquer sugestão, estamos abertos a te ouvir :-).

## Credencial de acesso ao OpenAI

### Passo 1 – Gerar uma API Key de acesso

A configuração dos custos da **OpenAI** é realizada através de uma _API Key_ de permissão restrita. Para criá-la, acesse o link a seguir: [https://platform.openai.com/settings/organization/admin-keys](https://platform.openai.com/settings/organization/admin-keys)

Após isso, em **_Admin Keys_**, clique em _**Create new Admin Key**_.

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-01.webp "Integrando OpenAI com Cloud8")

Nomeie a _Admin Key_ (sugerimos Cloud8) e em **_Permissions_** selecione “**_Restricted_**”. Em _**Resources**_, selecione “_Read_” para **_Usage API Scope_**. 

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-02.webp "Integrando OpenAI com Cloud8")

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-03.webp "Integrando OpenAI com Cloud8")

Em seguida, clique em **_Create admin key_**. Salve a _Admin Key_ em um lugar seguro. É importante ressaltar que não será possível visualizá-la novamente após clicar em Done.

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-04.webp "Integrando OpenAI com Cloud8")

### Passo 2 – Configurar o provedor na Cloud8

Em posse da _API Key_ criada, acesse a plataforma da Cloud8. No menu lateral esquerdo, selecione “**_Providers_**”. Clique em “**_New_**” e preencha os campos obrigatórios com os dados gerados nas etapas anteriores.

- **_Provider name_**: O nome que será utilizando para identificar o provedor na Cloud8.
- **_Timezone_**: padrão de tempo local que será utilizado.
- **_Language_**: idioma padrão.
- **_Secret_**: _secret key_ gerada no **Passo 1**.

Finalize clicando em **_Register_**.

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-05.webp)

**OBS:** Caso não haja dados de faturamento na _account_ a configuração irá gerar um alerta de erro.

![Integrando OpenAI com Cloud8](https://www.cloud8.com.br/wp-content/uploads/2025/09/openai-cloud-06.webp)

## Configurando o FinOps Analytics na Cloud8

A configuração do **FinOps Analytics** é realizada automaticamente através da conexão via _API Key_ que recebe os dados de uso e custo via chamadas de API.