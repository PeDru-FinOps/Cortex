#cloud8 #governance #security 

O gerenciamento de **Usuários e Perfis de Acesso na Cloud8** segue as melhores práticas de segurança da informação, em especial o **Princípio do Menor Privilégio**. Com papéis pré-definidos que variam de acesso total (Admin) até leitura restrita (Readonly/Report), a plataforma garante flexibilidade e controle sobre quem pode visualizar, alterar ou gerenciar recursos. 

Além disso, a possibilidade de criar **roles customizadas** amplia a governança, permitindo que cada organização adapte os acessos às necessidades reais de suas equipes, evitando excessos de permissão e fortalecendo a proteção dos dados e operações.

Em resumo, quanto mais alinhados os perfis de acesso estiverem às funções de cada usuário, maior será a segurança, a eficiência operacional e a conformidade no uso da Cloud8.

## Criando novos Usuários

Logo que uma conta é criada na **Plataforma da Cloud8**, a regra é que o usuário terá um **Perfil de Acesso Administrativo**, que garante permissões irrestritas de gerenciamento, inclusive para a criação de novos usuários, com diferentes políticas de acesso e gestão. 

Para criar novos usuários, clique em _**Users**_, no menu lateral esquerdo, e em _**New**_.

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-01.webp "Usuários e Perfis de Acesso")

Preencha todas as informações e defina a _**Access Role**_ que irá se aplicar ao usuário. Em seguida, clique em _**Save**_.

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-02.webp "Usuários e Perfis de Acesso")

## Configurando _Access Roles_

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-03.webp "Usuários e Perfis de Acesso")

### **1. _Role_: Admin**

**Perfil:** Acesso total ao sistema. Engloba todas as áreas — gerenciamento de conta, usuários, automações, relatórios, componentes e integrações.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração, editar dados pessoais, ver/alterar plano de pagamento, acessar extrato da conta, gerenciar provedores e unidades de negócio.|
|**Users**|Gerenciar roles e usuários; configurar SSO.|
|**FinOps – Analytics**|Acessar análises por produtos, tags, resource groups, labels.|
|**FinOps – Reports**|Todos os relatórios (Insights, Pivot Table, Fatura Anual, Savings, Budgets, Inventário, Novos Componentes, Recursos Taggeados/Não Taggeados, Preços de Nuvem).|
|**FinOps – Anomalies**|Identificar anomalias de custo ou uso.|
|**Automations**|Gerenciar servidores, dados, volumes, zonas DNS, apps, containers e relatórios automatizados.|
|**Best Practices**|Definir e revisar boas práticas.|
|**Notifications**|Notificações sobre custos, relatórios, instâncias reservadas, monitoramento de infraestrutura e bancos de dados, sincronizações e segurança.|
|**Integrations**|Configurar integrações com outros sistemas.|
|**Reports**|Métricas, cobertura de backup, credenciais IAM, instâncias/hora.|
|**Components**|DNS, instâncias, IPs elásticos, load balancers, volumes, dados, backups (por período e GFS), imagens, snapshots, grupos de segurança, chaves privadas, Kubernetes.|
|**Auditing logs**|Auditoria de logs.|
|**Help Desk / Sugestõe**|Abrir e gerenciar chamados.|

**Resumo:** É o superusuário. Pode configurar, criar, alterar e excluir qualquer recurso.

### **2. _Role_: Demo**

**Perfil:** Acesso amplo a quase todas as áreas, mas com foco em demonstração — não é restrito como Readonly, mas também não é administrador total.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração.|
|****Providers****|Visualização de todos os provedores cadastrados, sem possibilidade de criação, alteração ou deleção.|
|****Business Unit****|Visualização de todas as Business Units criadas, sem possiblidade de criação, alteração ou deleção.|
|****FinOps – Analytics****|Visão simplificada de custos mensal e anual. Acesso a Tags, RGs e Labels.|
|****FinOps – Reports****|Todos os relatórios (exceto gestão de roles).|
|****FinOps – Anomalies****|Painel de detecção de anomalias.|
|****Automations****|Visualizar todos os módulos de automação (servidores, dados, volumes, DNS, apps, containers).|
|**Notifications**|Visualizar opções de notificações de custos, relatórios, instâncias reservadas, monitoramento de infraestrutura e bancos de dados, sincronização e segurança.|
|**Reports**|Métricas, backup coverage, credenciais IAM, instâncias/hora.|
|**Components**|Todos (DNS, instâncias, IPs, load balancers, volumes, dados, backups, imagens, snapshots, security groups, chaves privadas, Kubernetes).|
|**Auditing logs**|Acesso ao registro de todos os logs de uso da Cloud8.|

**Resumo:** Ideal para demonstrações técnicas e comerciais. Tem acesso quase total, mas sem gestão de usuários/roles.

### **3. _Role_: DevOps**

**Perfil:** Foco em operações e infraestrutura — acesso aos recursos técnicos e automações.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração.|
|****Providers****|Visualização de todos os provedores cadastrados, sem possibilidade de criação, alteração ou deleção.|
|****FinOps – Reports****|Savings (otimizações).|
|****Automations****|Todos os módulos de automação.|
|**Notifications**|Visualizar opções de notificações de monitoramento de infraestrutura, bancos de dados, sincronização e segurança.|
|**Integrations**|Acesso|
|**Reports**|Métricas, backup coverage, instâncias/hora.|
|**Components**|Todos (DNS, instâncias, IPs, load balancers, volumes, dados, backups, imagens, snapshots, security groups, chaves privadas, Kubernetes).|
|**Auditing logs**|Acesso ao registro de todos os logs de uso da Cloud8.|

**Resumo:** Atua na operação e otimização da infraestrutura, sem acesso a dados financeiros sensíveis como faturas e extratos.

### **4. _Role_: Finance**

**Perfil:** Voltado para o controle financeiro e análise de custos.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração, plano/pagamento, extrato, provedores, unidades de negócio.|
|******FinOps – Analytics******|Produtos, tags, RGs, labels.|
|****FinOps – Reports****|Todos os relatórios.|
|******FinOps – Anomalies******|Acesso a detecção de anomalias.|
|**Notifications**|Custos, relatórios, RIs, monitoramento infra/DB, sincronizações e segurança.|
|**Integrations**|Acesso|
|**Reports**|Métricas, IAM credentials.|
|**Auditing logs**|Acesso|

**Resumo:** Tem visão financeira e estratégica, com acesso a custos, relatórios e otimizações, mas não gerencia infraestrutura.

### **5. Role: Provider**

**Perfil:** Fornecedores ou parceiros com acesso amplo, mas não administrativo.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração, provedores.|
|****Providers****|Visualização de todos os provedores cadastrados, sem possibilidade de criação, alteração ou deleção.|
|****FinOps – Analytics****|Visão simplificada de custos mensal e anual. Acesso a Tags, RGs e Labels.|
|****FinOps – Reports****|Todos os relatórios.|
|****FinOps – Anomalies****|Acesso|
|****Automations****|Todos os módulos, com exceção de Reports.|
|**Notifications**|Custos, relatórios, RIs, monitoramento infra/DB, sincronizações e segurança.|
|**Integrations**|Acesso.|
|**Reports**|Métricas, backup coverage, instâncias/hora.|
|**Components**|Todos os componentes técnicos.|
|**Auditing logs**|Acesso ao registro de todos os logs de uso da Cloud8.|

**Resumo:** Papel técnico e de gestão de infraestrutura, similar a DevOps, mas com visão de relatórios e otimizações.

### **6. _Role_: Readonly**

**Perfil:** Acesso somente leitura — ideal para auditorias e visualização de dados.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração, provedores.|
|**Providers**|Visualização de todos os provedores cadastrados, sem possibilidade de criação, alteração ou deleção.|
|**Business Unit**|Visualização de todas as Business Units criadas, sem possibilidade de criação, alteração ou deleção.|
|**FinOps – Analytics**|Produtos, tags, RGs, labels.|
|**FinOps – Reports**|Todos os relatórios.|
|**FinOps – Anomalies**|Acesso|
|**Automations**|Todos os módulos.|
|**Notifications**|Visualização de notificações de custos, relatórios, RIs, monitoramento infra/DB, sincronizações e segurança.|
|**Integrations**|Acesso|
|**Reports**|Métricas, backup coverage, instâncias/hora.|
|**Components**|Todos os componentes técnicos.|
|**Auditing logs**|Acesso|

**Resumo:** Pode ver absolutamente tudo o que DevOps/Provider veem, mas não pode criar/alterar nada.

### **7. Role: Report**

**Perfil:** Usuários focados apenas em relatórios e métricas.

**Permissões:**

|   |   |
|---|---|
|**My Account**|Alterar senha/configuração, plano/pagamento, provedores.|
|**Automations**|Relatórios automatizados.|
|**Reports**|Métricas|

**Resumo:** Papel bem restrito, apenas para geração e visualização de relatórios.

## Criar políticas de acesso customizadas no Cloud8

Para criar novas políticas de acesso customizadas, clique em _**Roles**_ no menu lateral esquerdo, e em seguida selecione _**New**_.

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-04.webp "Usuários e Perfis de Acesso")

A Cloud8 já possui diversas sugestões de regras de acesso customizadas, que podem ser vistas ao clicar em _**Type**_. Cada uma delas já possui um padrão pré-definido de políticas de acesso e configuração de componentes.

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-05.webp "Usuários e Perfis de Acesso")

Uma característica importante a ser ressaltada na criação de _Roles_ customizadas é que você terá dois escopos de configuração: **_Components_** e **_Actions_**.

- **_Components_:** Diz respeito ao escopo de abrangência. Quais provedores, unidades de negócio, recursos ou agrupamentos de recursos o usuário poderá ter acesso.
- **_Actions_**: Diz respeito ao escopo de ação. Quais ações o usuário tem permissão para realizar nos componentes selecionados.

As _roles_ customizadas são uma boa forma de executar de maneira prática o **Princípio do Menor Privilégio**, dando aos usuários apenas as permissões estritamente necessárias para o escopo de suas funções.

![Usuários e Perfis de Acesso](https://www.cloud8.com.br/wp-content/uploads/2025/10/usuarios-06.webp "Usuários e Perfis de Acesso")