#cloud8 #finops #data_analysis #governance #cloudcomputing #oci #aws #azure #gcp #bestpractices 

A funcionalidade do **Melhores Práticas** da **Cloud8** oferece uma visão consolidada de boas práticas de segurança, conformidade e eficiência dos ambientes em nuvem. Além disso, possui diversas recomendações de otimização de uso e custo. Através dela é possível avaliar rapidamente a infraestrutura e identificar riscos, bem como definir prioridades para ações de melhoria.

O painel apresenta um score geral, calculado com base na aderência às boas práticas recomendadas pelos principais _benchmarks_ do mercado, avaliando detalhadamente nas categorias de Backup, Compliance & _Availability_, _Cost Optimization_ e _Security_. As recomendações são classificadas por ordem de criticidade, permitindo que o usuário aloque seus esforços nas ações mais urgentes e efetivas.

![Utilizando Melhores Práticas Cloud8](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-01.webp "Utilizando Melhores Práticas Cloud8")

## Adoção dos principais benchmarks do mercado

Os _**CIS Benchmarks**_ são conjuntos de boas práticas de segurança e configuração publicados pelo **[Center for Internet Security (CIS)](https://www.cisecurity.org/)**, fornecendo recomendações amplamente adotadas pelo mercado para reduzir riscos, melhorar a postura de segurança e atender requisitos de compliance em ambientes de nuvem e _containers_. O painel da Cloud8 apresenta os seguintes _benchmarks_:

- **CIS Benchmark AKS**: melhores práticas de segurança para clusters Kubernetes gerenciados no Azure (AKS)
- **CIS Benchmark AWS Compute Services**: melhores práticas na segurança e configuração de workloads de computação na AWS.
- **CIS Benchmark AWS Database Services**: melhores práticas para proteção de dados sensíveis e garantia de resiliência dos bancos de dados.
- **CIS Benchmark AWS Foundations**: melhores práticas de configuração e controle em contas AWS.
- **CIS Benchmark Azure Compute Services**: melhores práticas na segurança e configuração de workloads de computação na Azure.
- **CIS Benchmark Azure Foundations**: melhores práticas de observabilidade e controle em workloads Azure.
- **CIS Benchmark EKS**: específico para Kubernetes gerenciados pela AWS.
- **CIS Benchmark GCP Foundations**: melhores práticas para GCP.
- **CIS Benchmark GKE**: específico para Kubernetes gerenciados pela GCP.
- **CIS Benchmark OCI Foundations**: melhores práticas de observabilidade e controle em workloads OCI.
- **CIS Benchmark OKE**: específico para Kubernetes gerenciados pela OCI.
- **LGPD**: benchmark de compliance regulatório, focado na [Lei Geral de Proteção de Dados (LGPD)](https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd)

Para gerar uma visualização da pontuação de conformidade em cada benchmarking, selecione a opção “**_Categories / Certifications_**” canto direito do painel.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-02.webp "Utilizando Melhores Práticas Cloud8")

## Relatórios e Notificações

O painel do **Melhores Práticas** permite a geração de **relatórios de diagnósticos**, clicando na opção “_**Reports**_”, que podem ser exportados nos formatos PDF e JSON. 

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-03.webp "Utilizando Melhores Práticas Cloud8")

## Global Notifications

É possível configurar o envio de **notificações de Melhores Práticas** através da opção “_**Global notifications**_”, no topo da tela. O usuário poderá configurar notificações com base em severidade, informando o endereço de e-mail a ser notificado e a granularidade do envio das notificações.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-04.webp "Utilizando Melhores Práticas Cloud8")

## Análise de conformidade no decurso do tempo

O painel também permite analisar o score do melhores práticas dentro de um _time range_ específico, selecionando a opção “_**Analytics**_”. O usuário será capaz de definir os seguintes campos:

- **Time scale**: definir a granularidade de maneira diária ou semanal.
- **Time range**: definir o período de tempo que será exibido no gráfico.
- **Clouds**: definir os provedores de serviço de nuvens a serem considerados na avaliação.
- **Provider**: selecionar os provedores cadastrados que serão avaliados.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-05.webp "Utilizando Melhores Práticas Cloud8")

O painel _Analytics_ também permite avaliar os savings gerados pelas recomendações do Melhores Práticas.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-06.webp "Utilizando Melhores Práticas Cloud8")

## Painel de Estimativa de Economia

O painel exibe uma visão consolidada dos _savings_ potenciais, categorizados por provedor e tipo de recomendação. Os dados deste painel também podem ser exportados clicando no botão “_**Export CSV**_”.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-07.webp "Utilizando Melhores Práticas Cloud8")

## Configurando as recomendações

**Todas as recomendações do Melhores Práticas são customizáveis**, bastando clicar no botão de configurações. Desta forma o usuário poderá configurar todas as condições necessárias para uma determinada recomendação, bem como desativá-la, caso assim deseje, clicando no botão “_**Enabled / Disabled**_”. Em seguida, clique em “_**Save**_”.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-08.webp "Utilizando Melhores Práticas Cloud8")

## Analisando as recomendações

Através do Melhores Práticas o usuário receberá não apenas os melhores _insights_, como cada recomendação virá com a listagem de recursos nos quais ela poderá ser aplicada. Basta **clicar no ícone de [+] ao lado da recomendação**.

A listagem gerada poderá ser exportada clicando em “_**Export CSV**_”.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-09.webp "Utilizando Melhores Práticas Cloud8")

Caso o usuário deseje excluir um ou mais recursos de uma determinada regra de Melhores Práticas, basta selecionar e clicar em “_**Do not monitor these items**_”.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-10.webp "Utilizando Melhores Práticas Cloud8")

A ação acima não possui caráter definitivo, e poderá ser revertido clicando em “_**Items affected**_” e selecionando “_**Excluded**_”. Na lista de recursos excluídos da regra de monitoração, você poderá selecionar aqueles que desejar e clicar em “_**Undo exclusion**_”.

![Utilizando Melhores Práticas](https://www.cloud8.com.br/wp-content/uploads/2026/02/utilizando-melhores-praticas-11.webp "Utilizando Melhores Práticas Cloud8")

A funcionalidade Melhores Práticas da Cloud8 consolida, em um único painel, **os principais pilares de uma gestão madura de ambientes em nuvem: segurança, conformidade, disponibilidade e otimização de custos**. Ao integrar _benchmarks_ reconhecidos pelo mercado, como os **CIS Benchmarks** e requisitos regulatórios como a **LGPD**, a plataforma permite uma avaliação contínua e confiável da postura do ambiente, traduzida em um _score_ claro e acionável.

Com recursos como análise histórica de conformidade, estimativa de _savings_, relatórios exportáveis, notificações automatizadas e customização total das recomendações, a Cloud8 não apenas identifica riscos e oportunidades, mas também apoia a priorização e a tomada de decisão estratégica. Dessa forma, o usuário ganha visibilidade, controle e eficiência operacional, transformando boas práticas em ações concretas que elevam o nível de governança e sustentabilidade dos ambientes em nuvem ao longo do tempo.