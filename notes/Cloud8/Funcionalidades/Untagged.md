#cloud8 

Através da funcionalidade Untagged o usuário é capaz identificar recursos sem [[Playbook - Tags]], ou mensurar o percentual de cobertura de determinada tag. No menu lateral esquerdo, clique em FinOps – Reports e selecione Untagged.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-01.webp "FinOps Reports: Tagged / Untagged")

### Identificando recursos sem qualquer marcação de tag

Ao acessar a funcionalidade, você pode identificar recursos sem qualquer tag associada, clicando no campo “Tags” e selecionando o valor “Without tags”.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-02.webp "FinOps Reports: Tagged / Untagged")

Selecione o período de verificação, que pode ser o valor padrão de visão mensal na opção “Entire month” ou um período especificado em horas, selecionando a opção “Last” e definindo um valor para “hours”, conforme imagem acima. 

Importante ressaltar que “Entire month” leva em consideração os meses definidos em “Periods”, que pode ou não coincidir com o momento da execução da função.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-03.webp "FinOps Reports: Tagged / Untagged")

Para executar a verificação, clique em Run e aguarde.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-04.webp "FinOps Reports: Tagged / Untagged")

O resultado irá gerar um gráfico demonstrando o total de recursos não tagueados.

### Identificando recursos com uma Tag específica

Também é possível verificar o nível de adesão de uma determinada tag dentro da infraestrutura do usuário. Ao invés de selecionar o valor “Without tags”, defina uma chave de tag que será verificada, como no exemplo abaixo. Configure o período para verificação e clique em Run.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-05.webp "FinOps Reports: Tagged / Untagged")

O exemplo abaixo apresenta características importantes da funcionalidade, tais quais:

**Tagueamento sintético e gestão multicloud**: o resultado retornado apresenta categorias de serviços nas quais há recursos sem a tag selecionada. Perceba que o exemplo demonstra que a ferramenta conseguiu identificar tags tanto na OCI quanto na Azure.

**Visão histórica da tag**: é possível verificar o histórico de adesão da tag durante o período de um ano. No exemplo trazido podemos verificar que houve esforços no período de Janeiro/2025 a Março/2025 para taguear todos os recursos. Percebe-se também que nos meses subsequentes a tag deixou de existir em todos os recursos, o que pode ser explicado por crescimento do ambiente sem uma política de tagueamento de novos recursos. 

**Alocação de custos**: o painel exibe o custo total dos recursos não tagueados, demonstrando o impacto financeiro da falta de identificação. Tratando-se da tag “application”, são recursos cuja classificação não foi atribuída a nenhuma aplicação específica, impossibilitando a correta associação do gasto a um sistema, projeto ou unidade de negócio.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-06.webp "FinOps Reports: Tagged / Untagged")

**Detalhamento de recursos**: a ferramenta não apresenta apenas a categoria de recursos sem tag, como também identifica exatamente quais são.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-07.webp "FinOps Reports: Tagged / Untagged")

### Atribuir tags em Untagged

Uma vez identificados os recursos sem tag atribuída, é possível exportar um arquivo csv do resultado.  Essa funcionalidade garante não apenas que o usuário possa agregar essa informação como um dataset de BI, como também gera uma coluna em branco no arquivo para que o usuário preencha com o valor da tag ausente. Para isso, clique em Download CSV (fill up tags).

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-08.webp "FinOps Reports: Tagged / Untagged")

Abra o arquivo e preencha a coluna da tag com os valores da tag em cada recurso identificado.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-09.webp "FinOps Reports: Tagged / Untagged")

Após preencher, clique em “Import filled up tags – BETA”. Antes de iniciar, é importante selecionar o provedor. A funcionalidade Untagged precisa ser gerenciada individualmente em cada provider configurado, e não irá funcionar em Unidades de Negócio. No topo da tela é possível visualizar o provider de exibição.

**Observação**: Ainda que seja possível listar uma tag utilizando Unidades de Negócio, a importação das tags é um trabalho que precisa ser realizado provedor por provedor.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-10.webp "FinOps Reports: Tagged / Untagged")

Na tela exibida, recomenda-se selecionar a opção “Apply automatically in the upcoming months”. Esta função evitará que os valores de tags para recursos já existentes precisem ser lançados manualmente a cada novo período. Assim, os valores de tags adotados no arquivo preenchido serão replicados nos mesmos recursos posteriormente.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-11.webp "FinOps Reports: Tagged / Untagged")

Também é possível alterar as tags diretamente no provedor de nuvem, selecionando a opção “Modify tags directly on cloud components using API calls”.  Os demais campos a serem preenchidos são:

- **Analized period**: o período do qual as tags preenchidas foram extraídas.
- **Filename**: ao clicar em Select é possível selecionar o arquivo preenchido que será importado.
- **Start period**: período a partir do qual as tags precisam ser preenchidas com os valores devidos, permitindo inclusive aplicar definição de tags atual para períodos anteriores.
- **End period**: último mês no qual as tags precisam ser ajustadas. Em regra o período do qual as tags preenchidas foram extraídas. Entretanto, nada impede um cenário onde uma tag precise ser classificada com um valor até um determinado mês, e nos subsequentes adotar um outro valor.
- **Notify e-mails**: a opção de ser notificado quando o processo de tagueamento for concluído.

Para concluir, clique em Import.

**Observação:** a funcionalidade de modificar tags diretamente nos componentes da cloud usando chamadas API encontra-se disponível apenas para provedores Azure e AWS. 

Se você quiser executar o tagueamento no Azure marcando a opção de chamar a API, o service principal precisa ser Contributor ou marcar o RBAC para a API do ResourceManager/tagOperations.

Se quiser executar o tagueamento na AWS marcando a opção de chamar a API, será necessário habilitar as seguintes credenciais de acesso:

```
...
tag:*
ec2:CreateTags
ec2:DeleteTags
rds:AddTagsToResource
rds:RemoveTagsFromResource
elasticloadbalancing:RemoveTags
elasticloadbalancing:AddTags
route53:ChangeTags*
dynamodb:Tag*
dynamodb:Untag*
logs:Tag*
logs:Untag*
eks:Tag*
eks:Untag*
elasticache:RemoveTagsFromResource
elasticache:AddTagsToResource
s3:DeleteObjectTagging
s3:DeleteJobTagging
s3:PutBucketTagging
s3:DeleteStorageLensConfigurationTagging
s3:ReplicateTags
s3:PutStorageLensConfigurationTagging
s3:PutObjectVersionTagging
s3:PutObjectTagging
s3:PutJobTagging
s3:DeleteObjectVersionTagging
dms:RemoveTagsFromResource
dms:AddTagsToResource
...
```

### Auditar tags ajustadas em Untagged

É possível administrar o histórico de alteração de tags realizado na ferramenta, através da opção “Applied tags – BETA”. Esta funcionalidade garante ainda mais controle sob a governança e alocação de tags, permitindo identificar alterações realizadas por provedor, recurso, região e valor de tag alterado.

![FinOps Reports: Tagged / Untagged](https://www.cloud8.com.br/wp-content/uploads/2025/10/finops-tagged-12.webp "FinOps Reports: Tagged / Untagged")