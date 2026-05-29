#cloud8 #sop #azure #gcp 

## Primeiro Passo - Crie um usuário utilizando o mesmo e-mail cadastrado no IDP

É necessário criar o usuário na Cloud8 após a configuração do IDP, utilizando o mesmo email. Importante configurar o Perfil de Acesso do Usuário antes de criar o usuário, tendo em vista que todas as autorizações são feitas na atribuição de perfil ao usuário.

Se o perfil de acesso desejado ainda não existe, precisará ser criado antes da autorização.

## Segundo Passo - Autorização do Usuário

Entra em "Usuários", seleciona o usuário desejado e clique em "SSO".

![[Pasted image 20260503215844.png]]

Você pode colocar como "Somente SSO" ou hibrido. Em seguida, selecione o IdP Provider cadastrado no sistema mediante chamado ao Suporte Técnico da Cloud8.

## Terceiro Passo - Testar a Configuração

Abre uma janela oculta do browser e em https://app.cloud8.com.br, seleciona SSO e execute o login.

![[Pasted image 20260503220109.png]]



