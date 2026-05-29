#finops #azure #cloudcomputing #arquitetura_solucoes 
## 1 - Objetivo

O objetivo deste playbook é apresentar boas práticas para o uso de tags em recursos de TI, com foco em governança, rastreabilidade de custos, segurança e conformidade. Além disso, um objetivo muito especial deste playbook é ser um guia didático sobre o uso de metadados para FinOps.

## 2 - Escopo

Esse playbook se aplica a todos os tipos de metadados, embora adote nomenclatura de "tag", o que pode aludir inicialmente ao ecossistema Azure. Entretanto, o conteúdo pode ser utilizado também em ambientes on-premises e nas demais clouds como AWS, GCP e Huawei.

## 3 - Benefício no uso de Tags

### 3.1 - Visibilidade e Rastreabilidade de Custos

As tags permitem associar recursos de TI diretamente aplicações, áreas de negócio e centros de custo. Assim é possível identificar quem está consumindo/o quanto está sendo consumido. Esse benefício garante a distribuição correta dos custos entre os seus respectivos responsáveis.

### 3.2 - Governança e Segurança da Informação

Tags contribuem para maior controle e visibilidade sobre o ciclo de vida dos recursos. É possível utilizá-las como um reforço de segurança da informação, reduzindo riscos de exposição e identificando todos os recursos que possivelmente possam ter sido afetados por um cyber ataque.

### 3.3 - Automação de Processos

Diversas automações utilizam tags como gatilhos, automatizando tarefas como Start/Stop de servidores, ciclo de vida de armazenamento de dados, monitoramento de recursos e escalabilidade. Trata-se de uma estratégia que reduz custos operacionais e garante padronização dos processos.

### 3.4 - Suporte a auditorias e compliance

Organizações estão sujeitas a regulamentações e normas específicas, como LGPD, ISO e afins. As tags oferecem suporte direto para classificar recursos auditáveis ou de conformidade necessária, facilitando inclusive a rastreabalidade e consistência na criação de relatórios. Segue abaixo exemplos:

- **Classificação de dados**: {Compliance:LGPD}
- **Criticidade do recurso**: {Compliance:Confidential}
- **Status de aderência**: {Compliance:Auditing}

Esse tipo de tag permite que as auditorias se tornem mais rápidas.

### 3.5 - Organização de Recursos

Em ambientes complexos, que podem abranger múltiplas clouds, regiões e projetos, a aplicação de tags garante uma **estrutura lógica de organização** que vai além dos agrupamentos nativos de cada provedor. Isso simplifica a localização, categorização e gerenciamento de ativos, além de reduzir desperdícios com recursos órfãos ou duplicados.

## 4 - Convenções de Nomeação e Padrões

A adoção de convenções de nomeação para **tags e seus valores** é fundamental para garantir consistência, confiabilidade e rastreabilidade na classificação de recursos. Sem padronização, as tags perdem valor, já que pequenas variações ortográficas ou semânticas podem gerar fragmentação de dados e inviabilizar relatórios de FinOps, compliance ou segurança.

### Recomendações:

- **Consistência**: as chaves e valores precisam ser documentadas e padronizadas, para evitar variações. Exemplo: Application ≠ APPLICATION ≠ application
- **Clareza**: as chaves e valores precisam ser de fácil identificação para todos os times.
- **Convenções**: tags precisam adotar uma forma uniforme e um idioma padrão. Recomenda-se utilizar letra maiúscula no início ou CamelCase, sem espaços, caracteres especiais ou acentos.
- **Granularidade adequada**: as tags precisam ser auditadas frequentemente, para garantir adoção integral.
- **Escopo organizacional**: a convenção de nomenclatura precisa ser aplicável em todas as áreas, ambientes e provedores de nuvem. É preciso estipular um catálogo corporativo de tags válidas.
- **Automações**: níveis maiores de maturidade demandarão a utilização de scripts, ferramentas, policies e pipelines para validar os padrões adotados.

### Modelo básico de tags

Uma boa prática é exigir tags somente para metadados básicos necessários, e para isso, um padrão recomendado utilizaria as seguintes tags:

- **Environment**: diferenciar os custos de produção, desenvolvimento e homologação.
- **Application**: identificar a aplicação a qual os recursos pertencem.
- **Owner**: identificar a pessoa ou equipe que deve prestar contas pelo recurso.
- **CostCenter**: setor da organização onde os custos devem ser alocados.
- **Compliance**: identificar requisitos regulatórios, normas ou classificações específicas que determinado recurso deve seguir.

**Observação**: adotando um modelo híbrido de governança, podemos substituir as tags de Environment e CostCenter por algum dos componentes de hierarquia de contas.

## 5 - Procedimentos de Aplicação de Tags

### 5.1 - Camadas complementares à governança por Tags

Tags são mutáveis e não suportadas por todos os tipos de recursos. Assim, devem ser vistas como um complemento a estruturas de governança nativas da nuvem e da TI tradicional, e não substitutas.

Hierarquias de contas permitem construir uma estratégia bem-sucedida de alocação de custos, fazendo uso dos agrupamentos lógicos abaixo.

**5.1.1 - Subscriptions/ Accounts/ Tenants**

Pode ser utilizado para separar ambientes, como produção, desenvolvimento e homologação. Em caso de Holdings composta por empresas diversas, recomenda-se que cada empresa possua suas próprias subscriptions.

**5.1.2 - Resource Groups/ Projects/ Folders**

Criar agrupamentos lógicos que façam sentido com a organização interna de cada empresa, podendo representar ambientes, caso não haja separação por Subscription. Também podem ser utilizados para organizar recursos específicos de determinadas aplicações.

**5.1.3 - Management Groups/ Organizations/ Hierarchias**

Utilizar para definir políticas centralizadas de compliance, custo e segurança de várias Subscriptions pertencentes à uma determinada Unidade de Negócios ou Organização.

**5.1.4 - Naming Conventions (Padrões de Nomeação)**

Padrões de nomenclatura de recursos que sejam claros, consistentes e obrigatórios a todos os recursos.

### 5.2 - Modelo Híbrido de Governança

Considerando as camadas complementares de governança listadas acima, podemos dizer que o modelo de governança ideal não é aquele que adota tags como sua principal ferramenta, e sim aquele que faz a combinação ideal entre:

- **Hierarquias de contas fortes e bem planejadas** **(RGs, Subscriptions, Management Groups, etc.)**. A maneira como a infraestrutura é organizada formará a primeira camada estratégica de alocação de custos, permitindo isolar os custos de ambientes ou aplicações.
- **Naming Convention clara e consistente**, aplicada a todos os recursos. Deve-se encorajar a organização a ter um padrão de nomenclatura e processos bem definidos para assegurar que ele seja seguido a risca.
- **Tags complementares**, para granularidade, relatórios financeiros (FinOps), automação e casos de uso específicos (auditoria, compliance). As tags ajudam a passar os gastos existentes para seus respectivos responsáveis.

Assim, caso uma tag esteja ausente, ainda existe a categorização básica pelo agrupamento lógico. Se o recurso não aceitar tags, ele ainda pertencem a uma estrutura que traz contexto; e, se uma auditoria exigir rastreabilidade, será possível cruzar todos os dados acima para garantir consistência nas informações prestadas.

### 5.3 - Herança de Tags

Uma opção eficaz para garantir que o maior número possível de recursos esteja tagueado é utilizar a replicação de tags de um recurso pai para seus recursos filhos, como no caso de backups e discos atrelados a um determinado servidor. Alguns provedores, como a Azure, permitem a herança de tags à nível de Resource Group, garantindo que todos os recursos criados dentro daquele agrupamento recebam as mesmas tags.

### 5.4 - Políticas de Tagueamento

Para assegurar que as tags obrigatórias sejam declaradas em recursos que serão criados, o administrador da nuvem poderá criar Policies que impeçam a criação de novos recursos sem as chaves e/ou valores de tags obrigatórias.

Caso um usuário tente realizar a criação do recurso em desconformidade, uma política de Deny impedirá a criação do novo artefato no ambiente, notificando o usuário para que ajuste as tags antes da nova tentativa de deploy.

## 6 - Governança e Responsabilidades (RACI)

![[Pasted image 20260414154828.png]]

## 7 - Checklist de Conformidade

O checklist abaixo deve ser utilizado periodicamente pelas equipes de Governança, FinOps, Infraestrutura e Auditoria para assegurar que o uso de tags esteja consistente, atualizado e aderente às políticas definidas.

### 7.1 – Estrutura e Padrões

- Existe um **catálogo oficial de tags** definido e documentado.
- Todas as tags possuem **chave (Key) padronizada** em conformidade com as convenções estabelecidas.
- Os **valores (Values)** seguem os padrões acordados (listas controladas, formatos de datas, identificadores).
- O catálogo é revisado periodicamente para refletir mudanças de negócio, governança e compliance.

### 7.2 – Aplicação e Cobertura

- Todos os recursos críticos possuem as **tags obrigatórias** aplicadas.
- Existe **cobertura mínima (%) de recursos tagueados** definida (ex.: 95%).
- Recursos que não suportam tags estão devidamente **mapeados e compensados** por outras estratégias (ex.: tags sintéticas, convenções de nomes, agrupamentos lógicos).
- Recursos recém-criados recebem tags **no momento da criação** (automação ou política de bloqueio).

### 7.3 – Governança e Consistência

- Tags não possuem **valores inconsistentes** (ex.: “Produção”, “Prod”, “PRD”).
- Tags críticas (ex.: Owner, CostCenter, Compliance) são **validadas periodicamente**.
- Existe processo de **correção de tags inválidas ou ausentes** (alertas, automação, runbooks).
- Existe clareza sobre **quem é responsável** por cada tag (conforme matriz RACI).

### 7.4 – Uso e Integração

- Tags são utilizadas para **rateio de custos (FinOps)** de forma confiável.
- Tags estão integradas com **políticas de segurança** (ex.: controle de criptografia, ambientes críticos).
- Tags são utilizadas em **automação de processos** (ex.: desligamento automático de VMs não produtivas, backups, escalabilidade).
- Tags estão integradas a **relatórios de auditoria e compliance**.

### 7.5 – Auditoria e Monitoramento

- Existem **relatórios periódicos** de conformidade de tags (mensal, trimestral).
- Gaps de cobertura ou inconsistências são **monitorados e reportados**.
- Auditoria externa ou interna consegue **cruzar informações** entre tags, hierarquias e naming conventions.
- Há plano de ação para **redução de desvios** quando identificados.
- Tags são utilizadas para identificar recursos que precisam atender normas regulatórias e compliance.

## 8 - Ferramentas de Apoio

A gestão eficiente de tags depende não apenas de políticas e processos, mas também de ferramentas que facilitem sua **aplicação, monitoramento, auditoria e automação**. Abaixo estão exemplos de ferramentas que podem apoiar o processo:

### 8.1 – Ferramentas Nativas das Clouds

**8.1.1 - Azure**

- **Azure Policy**: permite criar regras para obrigar ou corrigir tags em recursos e resource groups.
- **Azure Cost Management + Power BI**: relatórios de custos baseados em tags.
- **Azure Resource Graph**: consultas para identificar recursos sem tags ou com tags inválidas.

**8.1.2 - AWS**

- **AWS Tag Editor**: ferramenta para visualizar e gerenciar tags em múltiplos serviços.
- **AWS Organizations + Service Control Policies**: aplicar políticas centralizadas de governança.
- **AWS Cost Explorer / CUR**: relatórios financeiros baseados em tags.

**8.1.3 - Google Cloud (GCP)**

- **Resource Manager Labels**: equivalente a tags para organizar recursos.
- **Billing Reports**: permite filtrar custos por labels.
- **Policy Controller**: validação de políticas de metadados em clusters.

**8.1.4 - Huawei Cloud**

- **Tag Management Service (TMS)**: permite criar, gerenciar e aplicar tags em múltiplos serviços.
- **Cost Center**: relatórios de custos filtrados por tags.

### 8.2 – Automação e Análise de Dados

- **Infra as Code (IaC):** Terraform, Bicep, ARM Templates, CloudFormation → permitem definir tags já no provisionamento.
- **Scripting & Automação:** PowerShell / Azure CLI / AWS CLI permitem criar scripts para validação e correção de tags.
- **Python (Pandas)**: análise de arquivos de billing para reconstruir tags ausentes a partir de naming conventions ou regras de negócio.
- **Monitoramento & Alertas:** Grafana / Prometheus para criação de dashboards que mostram cobertura de tags. Azure Monitor / AWS CloudWatch / GCP Operations para a geração de alertas para recursos não conformes.

## 9 - Limitações das Tags e Complemento da Governança

Embora tags sejam uma estratégia importantíssima para classificação e organização de recursos, é necessário sempre considerar:

### 9.1 - Nem todos os recursos suportam tags

Alguns recursos podem não permitir o uso de metadados. Desta forma, o usuário deve ponderar se critérios críticos para classificação ou rateio de custos devem estar vinculados à uma determinada tag, já que na prática nem todos os recursos poderão utilizá-las.

Assim, haverá um total de gastos não tagueados que precisará ser auditado através de análise de dados. A fim de reduzir ao máximo este cenário, podemos levar em conta as seguintes recomendações:

**9.1.1 - Primeira recomendação: Adotar ferramenta que permita aplicação de Tags Sintéticas:**

Ferramentas de gestão de custos, como a Cloud8, por exemplo, permitem a utilização de Tags Sintéticas. Este recurso permite que a plataforma gerencie tags agnósticas em seu próprio workload, aplicando-as inclusive a recursos que nativamente não podem ser tagueados.

Essa estratégia também conta com a vantagem de permitir o gerenciamento de metadados de diversos provedores de serviço diferentes de maneira unificada.

Referência:

[[Utilizando Tags na Cloud8]]
[[Tagged]]
[[Untagged]]

**9.1.2 - Segunda recomendação: Tags de Agrupamentos Lógicos**

Alguns provedores de nuvem permitem tagueamento em agrupamentos lógicos. A Azure, por exemplo, permite a aplicação de Tags em Resource Groups.

Assim, uma estratégia eficaz para lidar com recursos que não podem ser tagueados em ambientes cujos agrupamentos falharam na adoção de Naming Conventions é aplicar metadados nos mesmos. Assim é possível mitigar os impactos da não conformidade com o padrão de nomenclatura, bem como identificar custos de recursos que não permitem marcação nativa.

**9.1.3 - Análise de Dados com base em arquivos de billing**

Utilizando bibliotecas para análsie de dados, como Pandas (Python), é possível criar scripts com regras para preenchimento da coluna de Tags utilizando as próprias convenções de nomenclatura e outras regras de negócio da organização.

### 9.2 - Metadados não são imutáveis

Tags podem ser alteradas manualmente ou removidas inadvertidamente, o que pode comprometer sua confiabilidade se não houver automação e governança adequadas.

### 9.3 - Dependência exclusiva de Tags gera risco

Se toda a categorização de compliance, segurança ou custos estiver apenas em tags, perde-se a consistência quando essas tags não existem ou são aplicadas incorretamente.

## 10 - Referências Bibliográficas

Storment, J.R.; Fuller, Mike. Cloud Finops: Tomada de decisões colaborativas em tempo real sobre o valor da nuvem. São Paulo: Novatec Editora, 2025.

[https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-policies?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-policies)

[https://learn.microsoft.com/en-us/azure/governance/policy/tutorials/govern-tags](https://learn.microsoft.com/en-us/azure/governance/policy/tutorials/govern-tags)

[https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html)

[https://support.huaweicloud.com/intl/en-us/productdesc-tms/en-us_topic_0071335169.html](https://support.huaweicloud.com/intl/en-us/productdesc-tms/en-us_topic_0071335169.html)?

[https://cloud.google.com/kubernetes-engine/enterprise/policy-controller/docs/overview](https://cloud.google.com/kubernetes-engine/enterprise/policy-controller/docs/overview)

[https://cloud.google.com/compute/docs/labeling-resources](https://cloud.google.com/compute/docs/labeling-resources)

[https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)

[https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)