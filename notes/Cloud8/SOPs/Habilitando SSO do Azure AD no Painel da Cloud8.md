#cloud8 #sop #azure #cloudcomputing 

SSO (_Single Sign On_) é um método de autenticação seguro que permite que um usuário faça login sem precisar repetir o processo diversas vezes. Atualmente a Cloud8 possui suporte para as seguintes plataformas:

- Azure AD
- AWS SSO
- Google Suite
- Github
- Centrify/CyberArk
- JumpCloud
- Okta

Para habilitar o Single Sign On (SSO) da Azure na Plataforma Cloud8 usando _Active Directory_ (AD), o usuário deverá nos enviar um arquivo XML e 3 URLs, gerados diretamente na interface da Azure.

Configurando SSO no Azure AD

Os passos para gerar e configurar esses assets são os seguintes:

1. Acesse o Portal Azure;
2. Pesquise por Microsoft Entra ID;
3. Clique em Enterprise Application, para configurar SSO baseado em SAML ;
4. Clique em “Create your own application”.
5. Selecione a opção “Non-gallery application”
6. Defina um nome para aplicação e clique em “Create”.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NYtG55wQH3d4M7iJrwpcRmyrYkkKPwVKIBvVohQVxPVTw1p90jxf7DVD2rgtuUkzuDqJdoYP2SlEPk7M6hM0j3TJOb0VBXdkMlsv4CbArLBFM9oMMN9EabDhIFB=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-01.webp "Habilitando SSO no Painel da Cloud8")

Selecione a aplicação criada, e no menu lateral esquerdo clique em “Single sign-on”. Escolha a opção SAML.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NZgEVLUcT4ks385-AlTEhBWeXSFZPQrdF0m8BispmhMOMS7T7H9OaTl69K3BfKJzQvlOfTMd9Tmvn0jI5blOVnNNRE3k29HgwUR81Lj7rPvPGqWoWOaBMnbcYgX=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-02.webp "Habilitando SSO no Painel da Cloud8")

Em seguida, clique no ícone para editar em “Basic SAML Configuration” (Item 1 do Painel)

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_Nal1p6YvvEVxpbmLpun4Cv9YE_uuFog9AEWMKhj6T-mvO8O7NsXkJX7T9Z2TdIZOddgsVQKZ5miallOuJrfNczPYQefe00HuXNakcY2xVBZG3rlDDqgjZ0ijC69=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-03.webp "Habilitando SSO no Painel da Cloud8")

O _Identifier_ é um ID único utilizado para identificar a aplicação no Microsoft Entra ID. A Cloud8 sugere adotar a seguinte nomenclatura:

“[https://sso.webpanel.cloud/azure/](https://sso.webpanel.cloud/azure/)NOME_DO_APP“

A Reply URL é onde o aplicativo espera que a autenticação e o token, com a declaração, sejam enviados. Assim como no Identifier a Cloud8 irá passar uma URL para utilização como URL Assertion na opção “Reply URL” no formato a seguir:

“[https://sso.webpanel.cloud/azure/](https://sso.webpanel.cloud/azure/)NOME_DO_APP“

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NYoymL-6E8t6i2k3KEQGYQZsg3Hw41KxncNxigOHdugGWoiz7Gp98ImdU34mUGmQjZf91SlVFfmEOLcAZl4fPOEAF-A88ouWQGe5I90_1wDdhgqPwqYRRAQKoLP=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-04.webp "Habilitando SSO no Painel da Cloud8")

Após, clique em “Save” para salvar a configuração. Em seguida, clique em “No, I’ll test later”.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NaiPg8O5EGe0vfpMeF1t9n-7uWIkZiyh3nogHcNya8mh11ulvxMVf4a03asrzpy9AngkZr25YSD71twcRRsT74Pr_332szygKkT-noyiKct1ESgPx7A17_Gg7qB=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-05.webp "Habilitando SSO no Painel da Cloud8")

Em seguida, adicione os usuários que irão utilizar o SSO e clique em “Assign”.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_Nb7I80EqhIYO90fw5wY0dvmy3PMLJVZ7FBYkM_P_kpxOQK8AMwZWxk1T8Aiv0MAGR114d8oqI3aio9VNS3h5twRPEEMLCKBd-nXb0en2T2E6Djsm4aG7huUkeWE=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-06.webp "Habilitando SSO no Painel da Cloud8")

Em SAML Certificates (Item 3 do Painel) encontre a opção “Federation Metadata XML” e clique em “Download”.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NYxVhw4r3kdP3_2dKPZuJ3iRKYofSXFacE2XFg7RaXEj0opXS0TJrFYe1C6zIDDrOLkJ0_SoJvc-pLfnpkenTxrqSeo5DNO6zqnAVJGxRccYhRviS1QNWrP2KKX=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-07.webp "Habilitando SSO no Painel da Cloud8")

Já em “Set up” (Item 4 do Painel) você precisará copiar cada uma das URLs abaixo e enviar no passo seguinte.

![Habilitando SSO no Painel da Cloud8](https://ci3.googleusercontent.com/meips/ADKq_NY9-xtfe2PvjGLYdlks1MOzjqKNnF8vWNXwo0GB7eG5UVNmIFdKe3_Ww8zr0LDeGvyDQRSG8ZrYqtHFdDbvwwMvb_8neDwJiVTNuhvNOmgrVFta5odPUtjQ-p2x=s0-d-e1-ft#https://www.cloud8.com.br/wp-content/uploads/2025/11/azure-sso-08.webp "Habilitando SSO no Painel da Cloud8")

Finalizando configuração de SSO no Azure AD

Após a configuração do SSO, envie um email para [suporte@cloud8.com.br](mailto:suporte@cloud8.com.br) com o assunto “Habilitar SSO da Azure” e forneça os seguintes dados:

- Identifier definido em Basic SAML Configuration
- Login URL, Microsoft Entra Identifier e Logout URL do Set up
- Federation Metadata XML exportado no SAML Signing Certificate