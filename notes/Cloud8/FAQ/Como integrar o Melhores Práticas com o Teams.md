#cloud8 #sop 

## 1 - Dentro da aplicação do Teams, acessar “Workflows”:

https://teams.microsoft.com/v2/

![[Pasted image 20260513105029.png]]

OBS: Na versão free do Teams, essa opção de apps -> workflows não está disponível.

## 2 - Criar novo workflow para integração:

2.1 - Acessar “Manage Workflows”:

![[Pasted image 20260513105108.png]]

2.2 - Clicar em “Build from scratch”

![[Pasted image 20260513105242.png]]

2.3 - Clique em “/select a trigger” e depois em “Build with Power Automate to see more
triggers”

![[Pasted image 20260513105303.png]]

2.4 - Clique em “Go to Power Automate”

![[Pasted image 20260513105322.png]]

Com isso, podemos configurar os passos para esse novo fluxo de integração, que está
detalhado no ponto 3 abaixo.

## 3 - Configurar novo fluxo de integração no Teams:

3.1 - Busque e clique na opção “Microsoft Teams Webhook”

![[Pasted image 20260513105351.png]]

3.2 - Selecione a opção “When a Teams webhook request is received”

![[Pasted image 20260513105406.png]]

3.3 - Em “Who can trigger the flow?” selecione a opção “Anyone”

![[Pasted image 20260513105422.png]]

3.4 - Clique no botão “New Step”, busque por “Teams” e selecione “Microsoft Teams”:

![[Pasted image 20260513105442.png]]

3.5 - Busque e selecione a opção “Post card in a chat or channel”

![[Pasted image 20260513105504.png]]

3.6 - Configurar as opções de configuração desse passo da seguinte forma:

- “Post as”: Flow bot
- “Post in”: Channel
- Team: (selecionar o seu Teams ID) - nesse exemplo foi selecionado o Teams ID
- “Integrations”
- Channel: (selecionar o channel que deseja receber as mensagens de integração) -
nesse exemplo foi selecionado o channel “best-practices”

![[Pasted image 20260513105549.png]]

3.7 - Em “Adaptative Card”, clicar em “add dynamic content +” e clicar em “Adaptive Card”:

![[Pasted image 20260513105606.png]]

Essa seleção irá permitir envio de mensagens no formato JSON para “Adaptive Cards” no
Teams.

3.8 - Clique em “Save”

![[Pasted image 20260513105627.png]]

Após concluir o processo de salvar, será gerado “HTTP POST URL” logo acima, clique na
parte de cima do workflow que foi gerado e copia a URL utilizando o botão ao lado:

![[Pasted image 20260513105643.png]]

Use essa nova URL para configurar a notificação “Teams” no Melhores Práticas para
integração de mensagens de notificação, exemplo:

```

https://default<ID_GERADO_PELO_TEAMS>.4c.environment.api.powerplatform.com:443/p
owerautomate/automations/direct/workflows/<WORKFLOW>/triggers/manual/paths/invoke?
api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=<SIG_GERADO>

```

3.9 Faça a criação da notificação no Melhores Práticas:

![[Pasted image 20260513105826.png]]

Exemplo de envio de mensagens do Melhores Práticas via integração workflow para o Teams:

![[Pasted image 20260513105844.png]]