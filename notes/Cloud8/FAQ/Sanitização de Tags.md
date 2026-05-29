#cloud8 #finops #bestpractices #governance #cloudcomputing 

Provedores de cloud, com exceção do AWS (que você deve indicar quais _Tags_ quer utilizar conforme documentamos anteriormente), trazem todas as _Tags_ nos relatórios de custos. Se o número de _Tags_ for excessivo, pode prejudicar a visualização e a produtividade. 

A primeira vantagem da sanitização é escolher somente as _Tags_ principais para **FinOps**. A segunda, é arrumar a grafia das _Tags_ para compatibilizar grupos de _Tags_ e arrumar o histórico. 

O princípio é simples: escolher um nome de _Tag_ ‘_principal_’ e associar variações a ele. 

**Exemplo**: tag principal, “produto”. Variações: “Produto”, “ produto” (com espaço na frente), “Product”, “cliente” (qualquer variação que está sendo migrada).

Para acessar esta aplicação, disponibilizamos uma aplicação em “**FinOps – Analytics**”: 

![](https://www.cloud8.com.br/wp-content/uploads/2024/11/finops-tag-sanitize.webp)

Com esta aplicação, localizada em “Custos – Analytics”, é possível fazer o mapeamento de nomes e valores alternativos, consolidando grafias legadas e/ou erradas. 