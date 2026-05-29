[[Untagged]] #cloud8 

Decidi testar o funcionamento do Untagged para atender um chamado da SGA. Basicamente o módulo Untagged não está listando recursos sem tags. Te perguntei se era porque a análise era com base numa unidade de Negócios, e você respondeu que sim. Porém fiz os seguintes testes utilizando o ambiente da Simpar.

**1 - Unidade de Negócios onde todos os providers são da mesma Cloud**

![[Pasted image 20260323211923.png]]

O Untagged funcionou corretamente. 

**2 - Unidade de Negócios multicloud**  

![[Pasted image 20260323211952.png]]

Funcionou, porém todos os recursos listados eram Azure. Para validar, decidi escolher especificamente providers de outras clouds.

![[Pasted image 20260323212003.png]]

![[Pasted image 20260323212015.png]]

Pelo visto o problema não foi não funcionar, e sim que os providers da OCI realmente estavam totalmente tagueados. Ou seja, em tese o Untagged deveria funcionar para BUs multi-cloud.  

**3 - Avaliação do Ambiente da SGA**

Dito isto, decidi validar o ambiente da SGA novamente. Eles estão incomodados com a seguinte mensagem:

**Aviso! Por falta de dados recentes, não foi possível encontrar os componentes.**

![[Pasted image 20260323212345.png]]

Essa mesma mensagem aparece nos prints do ambiente da Simpar, e entendo que queira dizer que não há recursos sem qualquer valor de tag. 
