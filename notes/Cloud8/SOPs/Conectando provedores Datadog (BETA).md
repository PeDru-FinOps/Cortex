#cloud8 #cloudcomputing #datadog 

## **Importante para o Beta:**
  
Atualmente, a maioria dos ambientes Datadog não expõe custos detalhados diretamente pelas APIs de billing no nível necessário para cálculo financeiro completo. Por isso, nesta fase Beta, parte dos custos pode ser estimada utilizando os preços públicos da Datadog.

Caso necessário, os valores podem ser ajustados manualmente por cliente dentro da plataforma Cloud8.

## Observações sobre Tags e Atributos

Durante os testes iniciais da integração, o ambiente utilizado não possuía [[Tags]] configuradas.

Na documentação da Datadog, existem recursos relacionados a:

- tags
- attributes
- service metadata
- usage attribution

Caso o cliente utilize essas informações, a Cloud8 poderá tentar processá-las para melhorar agrupamentos, classificação e atribuição de custos.

## **Credenciais necessárias :**

Para realizar a integração com a Datadog, precisamos de:

- API Key
- Application Key

Importante: a Datadog normalmente exige o uso combinado das duas chaves para APIs de leitura.

### Recomendação de Conta para Integração:  

Recomendamos que a integração seja criada utilizando uma das opções abaixo:

- uma service account dedicada  
- um usuário administrador da Datadog

Isso facilita governança, auditoria e futuras rotações de credenciais.
### Criar a API Key:

No menu do Datadog:  Organization Settings > API Keys

Depois:

- clicar em “New Key”
- informar um nome para a chave, por exemplo: Cloud8 Billing Integration
- criar a chave
- copiar e guardar o valor gerado
### Criar a Application Key  

No menu do Datadog:  Organization Settings > Application Keys

Depois:

- clicar em “New Key”
- informar um nome para a chave, por exemplo: Cloud8 Billing Integration App Key
- criar a chave
- copiar e guardar o valor gerado imediatamente

**Importante**: em muitos ambientes Datadog, o segredo da Application Key pode ser exibido apenas no momento da criação. Se a chave não for salva nessa hora, pode ser necessário revogá-la e criar outra.
### Garantir as permissões necessárias  

A conta usada para criar a Application Key deve ter permissão para leitura de billing e usage no Datadog, para permitir o consumo dos dados de custos e uso.    

Como referência, validar se a conta/chave possui acesso de leitura equivalente a:

- billing_read
- usage_read
- cloud_cost_management_read

Se vocês utilizarem RBAC com escopos mais restritos, o ideal é conceder somente os acessos mínimos necessários para leitura dessas informações.

### Identificar o site/região do Datadog  

A Cloud8 também precisa saber em qual site/região a conta Datadog está hospedada, pois isso altera a URL-base da API.

Exemplos:

|Região|Endpoint|
|---|---|
|US1|`https://api.datadoghq.com`|
|EU|`https://api.datadoghq.eu`|
|US3|`https://api.us3.datadoghq.com`|
|US5|`https://api.us5.datadoghq.com`|
|AP1|`https://api.ap1.datadoghq.com`|
|AP2|`https://api.ap2.datadoghq.com`|

## Validar as Credenciais

Antes de concluir a integração, é recomendável validar as credenciais.

### Validação simples da API Key:  

`` GET /api/v1/validate

`` curl -X GET "https://api.datadoghq.com/api/v1/validate" \
 `` -H "DD-API-KEY: <your_api_key>"

### Validação do API Key + Application Key 

`` GET /api/v2/validate_keys

`` curl -X GET "https://api.datadoghq.com/api/v2/validate_keys" \
``  -H "DD-API-KEY: <your_api_key>" \
``  -H "DD-APPLICATION-KEY: <your_app_key>"

## Obtendo o Org ID

### Via API

A Cloud8 pode utilizar o identificador organizacional da Datadog (`public_id`) para identificação da conta integrada.

`` curl -X GET "https://api.datadoghq.com/api/v1/org" \
 `` -H "DD-API-KEY: <your_api_key>" \
 `` -H "DD-APPLICATION-KEY: <your_app_key>"

No retorno JSON localizar:

`` "public_id": "abc123xyz"

### Via Navegador (necessário acesso à interface Datadog)

Crie um favorito/bookmark no navegador contendo:

`` javascript:(function() {var orgId = JSON.parse(document.querySelector('#_current_user_json').value).org.id; alert("OrgId is " + orgId);})();

Ao executar dentro da interface Datadog, será exibido o Org ID da organização.
### Informações que devem ser enviadas para a Cloud8  

Precisaremos receber:

- API Key
- Application Key
- site/região da Datadog
- Org ID / public_id
- confirmação de acesso de leitura a:
    - usage
    - billing
    - cost attribution
- confirmação se Cloud Cost Management / Cost Attribution está habilitado
### Observações sobre os dados  

Alguns dados de uso podem ser consumidos pelas APIs de Usage Metering.  

Já os dados de cost attribution mensal dependem do modelo de billing do Datadog e, para contas com direct billing, costumam ficar disponíveis após o fechamento do ciclo, normalmente até o dia 19 do mês corrente para o mês anterior.

## Utilizando os dados do Datadog na Cloud8

Após a integração dos dados, os custos de Datadog ficarão disponíveis nas seguintes funcionalidades:

### FinOps Analytics

![[Pasted image 20260522101147.png]]

![[Pasted image 20260522101352.png]]
### Dashboards

![[Pasted image 20260522101229.png]]

# Referências Oficiais

API Datadog: [Documentação Oficial da API Datadog](https://docs.datadoghq.com/api/latest/?utm_source=chatgpt.com)
Usage Metering: [Datadog Usage Metering API](https://docs.datadoghq.com/api/latest/usage-metering/?utm_source=chatgpt.com)
Organizations API: [Datadog Organizations API](https://docs.datadoghq.com/api/latest/organizations/?utm_source=chatgpt.com)
APM API: [Datadog APM API](https://docs.datadoghq.com/api/latest/apm/?utm_source=chatgpt.com)
## Referências Internas

[[APIs utilizadas pelo Cloud8 na Datadog]]

