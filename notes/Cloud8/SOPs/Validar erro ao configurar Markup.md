#cloud8 #sop

## Erro - Esta função é utilizada para editar os dados de uma conta de revenda. Utilize "Editar"

Se o cliente retornar o seguinte erro:

![[Pasted image 20260515123147.png]]

Caso ele tenha tentado utilizar a opção abaixo:

![[Pasted image 20260515123249.png]]

### Solução:

Este erro ocorre quando o usuário configura uma conta como se fosse stand-alone. Para validar se é a hipótese, verifique em **Provedores** se a coluna **Tier II** está em branco.

![[Pasted image 20260515123538.png]]

A melhor maneira para criar um novo Tenant no CSP é criar um Tier II associado ao Tenant do cliente, pois desse jeito qualquer subscrição nesse tenant e no CSP será carregada junto. Clique em **MSP/Tier II** e em seguida **Novo Tier II**. No último campo preencha com o Tenant do Cliente.

![[Pasted image 20260515123758.png]]

Outra vantagem é que se o cliente tiver muitas subscriptions, você consegue editar o Markup de End User de todas subscriptions através do Tier II.

Caso você queira realmente carregar somente uma subscription do tenant do cliente que está no seu CSP, o procedimento que você fez continua válido, neste caso é só movimentar a conta da Cristalia para debaixo do Tier II raiz "SLMIT - Azure - MSP".  Depois de fazer isso você consegue editar o markup dessa subscrição individualmente.

![[Pasted image 20260515123955.png]]

![[Pasted image 20260515124000.png]]