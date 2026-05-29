#finops #cloud8 #cloudcomputing 

## Definição 

Uma **_Tag_** é um metadado essencial para organizar e gerenciar recursos em ambientes de **Cloud Computing**. Trata-se de um par de valores composto por uma **chave (Nome)** e um **valor (Valor)**, que permite categorizar e identificar os recursos na nuvem de maneira eficiente. Por exemplo, você pode criar uma tag com o Nome “Departamento” e o Valor “TI” ou “Marketing”.

As tags desempenham um papel fundamental na administração de infraestrutura em provedores como **AWS**, **Azure**, **Google Cloud**, **Oracle Cloud Infrastructure (OCI)** e **Huawei Cloud**, facilitando tarefas como controle de custos, rastreamento de recursos e aplicação de políticas de segurança.
## Tipos de Tags

A Cloud8 oferece suporte para dois tipos de Tags:
### Tag Nativa:

São as tags oriundas dos cloud providers. Nossa plataforma é capaz de catalogar todas as tags existentes na infraestrutura do cliente e utilizá-las para os mais diversos tipos de filtro. Tags Nativas são ideais para workloads de automação e regras de negócio que se apliquem exclusivamente ao provedor de serviços.
### Tag Sintéticas:

São tags cujo nome ou valor são definidos diretamente na plataforma da Cloud8. Com a Cloud8 é possível atribuir tags e valores de tags à recursos que nativamente não podem ser tagueados, permitindo alcançar 100% de alocação de custos. Isto ocorre porque as tags na Cloud8 podem ser utilizadas sem a necessidade de taguear os recursos no cloud provider. Tags sintéticas são ideais para workloads de showback e chargeback, bem como para gestão de custos cloud.

Já um valor sintético de Tag é utilizado quando a tag já existe, porém o recurso não possui valor de tag atribuído ao mesmo, seja por não definição da operação, seja pela inviabilidade técnica, no caso de recursos que nativamente não podem ser tagueados.

## Procedimento para adoção de Tags Sintéticas

O usuário poderá entrar em contato com o Suporte Técnico e solicitar a criação de uma tag sintética que será utilizada exclusivamente na plataforma da Cloud8, e caso necessário, poderá ser propagada via API para o provedor de serviço de nuvem. O e-mail deverá conter as seguintes informações:

- Convenção de Nomenclatura (kebab-case, Camel-Case, UPPERCASE, etc)
- Período a partir do qual a tag precisa refletir na plataforma, podendo retroagir à data da solicitação.
- Informar se a tag desejada será de fato sintética, ou uma tag nativa da cloud à qual o usuário atribuirá valores sintéticos.

**Observação**: Na hipótese de tags nativas com valores sintéticos, a Cloud8 irá sobrescrever o valor das tags existentes no Cloud8. Com isto, o report no Cost and Usage Report (CUR) ficará diferente do painel da Cloud8.
## Convenções de Nomeação e Padrões

A adoção de convenções de nomeação para **tags e seus valores** é fundamental para garantir consistência, confiabilidade e rastreabilidade na classificação de recursos. Sem padronização, as tags perdem valor, já que pequenas variações ortográficas ou semânticas podem gerar fragmentação de dados e inviabilizar relatórios de FinOps, compliance ou segurança. 

Tags são, em regra, case sensitive, de forma que qualquer variação de escrita gera uma nova tag ou valor de tag. Veja o exemplo utilizando a tag "Ambiente" como padrão:

Ambiente: Desenvolvimento - Uma Tag e um valor de Tag
AMBIENTE: Desenvolvimento - Tag Diferente e valor de Tag igual
Ambiente: DESENVOLVIMENTO - Mesma Tag e dois valores Tag
AMBIENTE: DESENVOLVIMENTO - Tags e Valores diferentes

### Recomendações:

- **Consistência**: as chaves e valores precisam ser documentadas e padronizadas, para evitar variações. Exemplo: Application ≠ APPLICATION ≠ application
- **Clareza**: as chaves e valores precisam ser de fácil identificação para todos os times.
- **Convenções**: tags precisam adotar uma forma uniforme e um idioma padrão. Recomenda-se utilizar letra maiúscula no início ou CamelCase, sem espaços, caracteres especiais ou acentos.
- **Granularidade adequada**: as tags precisam ser auditadas frequentemente, para garantir adoção integral.
- **Escopo organizacional**: a convenção de nomenclatura precisa ser aplicável em todas as áreas, ambientes e provedores de nuvem. É preciso estipular um catálogo corporativo de tags válidas.
- **Automações**: níveis maiores de maturidade demandarão a utilização de scripts, ferramentas, policies e pipelines para validar os padrões adotados.
-  **No caso do AWS que precisa escolher as tags, sugerimos fortemente que marque as tags que ele próprio gerencia**: “aws:createdBy”, “aws:ecs:serviceName”, “aws:ecs:clusterName”, “aws:autoscaling:groupName”, “aws:eks:cluster-name”

## Procedimentos de Aplicação de Tags

### Camadas complementares à governança por Tags

Tags são mutáveis e não suportadas por todos os tipos de recursos. Assim, devem ser vistas como um complemento a estruturas de governança nativas da nuvem e da TI tradicional, e não substitutas.

Hierarquias de contas permitem construir uma estratégia bem-sucedida de alocação de custos, fazendo uso dos agrupamentos lógicos abaixo.

**Subscriptions/ Accounts/ Tenants**

Pode ser utilizado para separar ambientes, como produção, desenvolvimento e homologação. Em caso de Holdings composta por empresas diversas, recomenda-se que cada empresa possua suas próprias subscriptions.

**Resource Groups/ Projects/ Folders**

Criar agrupamentos lógicos que façam sentido com a organização interna de cada empresa, podendo representar ambientes, caso não haja separação por Subscription. Também podem ser utilizados para organizar recursos específicos de determinadas aplicações.

**Management Groups/ Organizations/ Hierarchias**

Utilizar para definir políticas centralizadas de compliance, custo e segurança de várias Subscriptions pertencentes à uma determinada Unidade de Negócios ou Organização.

**Naming Conventions (Padrões de Nomeação)**

Padrões de nomenclatura de recursos que sejam claros, consistentes e obrigatórios a todos os recursos.

### Modelo Híbrido de Governança

Considerando as camadas complementares de governança listadas acima, podemos dizer que o modelo de governança ideal não é aquele que adota tags como sua principal ferramenta, e sim aquele que faz a combinação ideal entre:

- **Hierarquias de contas fortes e bem planejadas** **(RGs, Subscriptions, Management Groups, etc.)**. A maneira como a infraestrutura é organizada formará a primeira camada estratégica de alocação de custos, permitindo isolar os custos de ambientes ou aplicações.
- **Naming Convention clara e consistente**, aplicada a todos os recursos. Deve-se encorajar a organização a ter um padrão de nomenclatura e processos bem definidos para assegurar que ele seja seguido a risca.
- **Tags complementares**, para granularidade, relatórios financeiros (FinOps), automação e casos de uso específicos (auditoria, compliance). As tags ajudam a passar os gastos existentes para seus respectivos responsáveis.

Assim, caso uma tag esteja ausente, ainda existe a categorização básica pelo agrupamento lógico. Se o recurso não aceitar tags, ele ainda pertencem a uma estrutura que traz contexto; e, se uma auditoria exigir rastreabilidade, será possível cruzar todos os dados acima para garantir consistência nas informações prestadas.

### Herança de Tags

Uma opção eficaz para garantir que o maior número possível de recursos esteja tagueado é utilizar a replicação de tags de um recurso pai para seus recursos filhos, como no caso de backups e discos atrelados a um determinado servidor. Alguns provedores, como a Azure, permitem a herança de tags à nível de Resource Group, garantindo que todos os recursos criados dentro daquele agrupamento recebam as mesmas tags.

### Políticas de Tagueamento

Para assegurar que as tags obrigatórias sejam declaradas em recursos que serão criados, o administrador da nuvem poderá criar Policies que impeçam a criação de novos recursos sem as chaves e/ou valores de tags obrigatórias.

Caso um usuário tente realizar a criação do recurso em desconformidade, uma política de Deny impedirá a criação do novo artefato no ambiente, notificando o usuário para que ajuste as tags antes da nova tentativa de deploy.

## Tags nos provedores de cloud 

- **AWS**: escolha as tags que serão visualizadas nos dados de Cost And Usage Reports em [https://console.aws.amazon.com/billing/home?region=us-east-1#/preferences/tags](https://console.aws.amazon.com/billing/home?region=us-east-1#/preferences/tags) 
- **Azure, Google Cloud, Huawei e Oracle**: irão publicar todas as tags que os componentes possuírem 
- **Azure**: processamos as tags dos componentes e as tags dos Resources Groups (grupos de recurso). Você pode escolher se quer trabalhar tagueando todos os componentes ou somente os RGs. Taguear os RGs é mais fácil, mas exige que os componentes estejam alocados corretamente. O Cloud8 mostra as tags de RGs como prefixo “azure:rg:”. Ex: “azure:rg:centrocustos” que será diferente de simplesmente “centrocustos” 

## Limitações no cadastro de tags 

- **As tags não se propagam retroativamente**. O dia e hora que marcar as tags é o início da contabilização pelo provedor de cloud. O ideal é inseri-las imediatamente na criação dos componentes e revisar antes de começar o próximo período contábil (exemplo: antes de virar o mês); 
- **Grafias diferentes – como um simples espaço – são considerados agrupamentos diferentes** – daí recomendarmos usar minúsculas e ASCII. 
- **Não são todos os componentes que suportam tags**. Consulte o provedor para saber mais. Nota: o Cloud8 possui um recurso para mapear o que não está com tag ([[Untagged]]) – mais à frente.
## Sanitização de Tags

Provedores de cloud, com exceção do AWS (que você deve indicar quais _Tags_ quer utilizar conforme documentamos anteriormente), trazem todas as _Tags_ nos relatórios de custos. Se o número de _Tags_ for excessivo, pode prejudicar a visualização e a produtividade. 

A primeira vantagem da [[Sanitização de Tags]] é escolher somente as _Tags_ principais para **FinOps**. A segunda, é arrumar a grafia das _Tags_ para compatibilizar grupos de _Tags_ e arrumar o histórico. 

O princípio é simples: escolher um nome de _Tag_ ‘_principal_’ e associar variações a ele. Essa medida permite mitigar problemas de Name Conventions, porém a melhor solução sempre será a correção das Tags utilizando os módulos [[Untagged]] e [[Tagged]].

**Exemplo**: 

Tag principal: "produto" 

**Variações:** 

“Produto”
“ produto” (com espaço na frente)
“Product”
“cliente” (qualquer variação que está sendo migrada).

A sanitização das tags pode ser feita clicando em **Provedores**. Selecione um dos provedores e clique em **FinOps Tags**: 

![[Pasted image 20260514063358.png]]

Com esta funcionalidade é possível fazer o mapeamento de nomes e valores alternativos, consolidando grafias legadas e/ou erradas. Você pode informar diversos valores alternativos, separando-os por vírgula.

## Tags em MultiCloud – Unidades de negócio 

Como mencionado anteriormente, é muito importante definir as _Tags_ em um formato que seja aceito por todos os clouds públicos. 

O Cloud8 permite a gestão de _Tags_ em ambiente _MultiCloud_ por meio do recurso de ‘**Unidades de Negócios**’. Ao replicar a estrutura da sua empresa / departamentos / clientes, você passa a contar com um novo ‘provedor’ e ganha todas as funcionalidades de acompanhamento de custos – sejam elas técnicas ou negócios (_Tags_).  

_Tags_ comuns a todos os provedores como por exemplo “**centrodecustos**” passam a ter um relatório consolidado. 

Caso os provedores tenham moedas diferentes, o Cloud8 se encarrega de convertê-las para Dólar ou Real e os custos de produtos e custos de _Tags_ ficam alinhados e compatíveis. 

![](https://www.cloud8.com.br/wp-content/uploads/2024/11/finops-business-units.webp)

## Conformidade nos valores das tags. 

Para garantir que todos os componentes tenham as tags e estão seguindo as definições do seu processo, disponibilizamos regras de conformidade dentro do “**Melhores Práticas**”.  

![](https://www.cloud8.com.br/wp-content/uploads/2024/11/finops-tag-compliance.webp)

Como já descrito anteriormente, o acompanhamento e correção dos componentes não _tagueados_ pode ser feito pela aplicação de “_Untagged_”. Mas como garantir que os valores (além dos nomes) colocados também estejam corretos? 

Por exemplo: definimos que as _Tags_ devem ser “**centrocustos**”, “**produtos**”, “**ambiente**”, “**equipe**”. Como garantir que os centros de custos usados nas _Tags_ estejam corretos e pertencendo a uma lista? Ex: **cc-0101**, **cc-2341**, **cc-7788**, etc. e que alguém não coloque por acidente um valor errado? 

Pelo **Melhores Práticas** você pode criar a sua política de _compliance_. Veja a regra “_Resource with noncompliance tags_” e defina nome / valores dentro dos filtros. Lembre-se que os valores são sempre _case sensitive_, então tome cuidado com maiúsculas e minúsculas. 

![](https://www.cloud8.com.br/wp-content/uploads/2024/11/finops-noncompliance-tags.webp)

Se um valor estiver fora da lista definida, você será alertado pelo canal de notificação que escolher.

## Tags e Descontos Baseados em Compromisso (RI e SP)

O Cloud8 possui duas visões: Produto e Invoice. Reservas de Instância e Savings Plans podem ser compradas em qualquer conta de uma organização e utilizadas por todas, o que impacta diretamente a utilização de Tags para filtrar dados.

- Na visão Produto, alocamos as contas que efetivamente usaram estes compromissos.
- Na visão Invoice, alocamos as contas que compraram e realizaram o pagamento dos compromissos.

Isto gera divergência entre as duas visões, além de visualização de créditos em Invoice. A utilização de tags e baseada em Invoice (quem pagou) e não em Produtos (quem utilizou), conforme exemplo abaixo:

|                             |          |                        |
| --------------------------- | -------- | ---------------------- |
|                             | Produtos | Invoice (sem créditos) |
| AWS - Cliente-hml           | 1266.41  | 696.87                 |
| AWS - Cliente-prod (com SP) | 4459.68  | 5029.21                |
| Total                       | 5726.09  | 5726.08                |

O painel **Reports - Dashboards** exibe Produtos, então quando é feito um relatório na conta AWS-Cliente_hml o usuário verá a tag "env=prod", tendo em vista que ela consumiu SP de Produção. É possível aplicar em cima do uso real (Produtos), mas a Invoice fica com as parcelas compartilhadas.

Assim, o usuário precisa levar em consideração a regra de negócio para Chargeback: olhar o invoice ou a utilização efetiva.


