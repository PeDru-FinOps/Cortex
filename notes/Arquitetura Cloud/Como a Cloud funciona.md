#arquitetura_solucoes #cloudcomputing 
Muitas pessoas não sabem de fato o que é uma nuvem, embora a utilizam diariamente. Quando armazenamos nossas fotos e imagens no Google Drive, muitas vezes não nos perguntamos para onde esses arquivos estão sendo enviados. Portanto, precisamos entender os fundamentos da Cloud Computing, e seus principais componentes.

### Datacenters, Regiões e Zonas de Disponibilidade

Datacenters são instalações físicas que contém infraestrutura computacional. Ela é composta por:

  

- Servidores físicos: racks com CPU, RAM, discos e interfaces de rede.
    
- Storage: block storage, object storage e file storage para compartilhamento de arquivos (NFS/SMB).
    
- Equipamentos de rede: switches, roteadores, firewalls, load balancers.
    
- Sistema de energia
    
- Sistema de resfriamento
    
- Segurança física
    

Regiões são conjuntos geográficos de datacenters separados fisicamente, conectados por uma rede de baixa latência e isolados para tolerância a falhas. Seus principais fundamentos são:

  
- Latência: usuários conseguirem acessar servidores mais próximos.
    
- Regulamentação: respeitar requisitos de data residency.
    
- Resiliência: arquiteturas multi-region mantém a aplicação ativa em caso de falhas.
    
### Virtualização de recursos

A virtualização é o fundamento técnico do cloud computing, e sem ela a cloud não existiria. Num modelo tradicional cada servidor hospedava uma aplicação, o que gerava problemas com desperdício de recursos computacionais, tendo em vista que a maior parte do servidor ficava ocioso.

Com a virtualização, um único servidor pode executar diversas máquinas virtuais ou contêineres, através do uso de um Hypervisor ou tecnologias como Docker. Quando falamos de virtualização, podemos lidar com dois tipos:
  

- Virtualização de Hardware: um Hypervisor cria VMs completas, incluindo processador, memória e sistema operacional.
    
- Virtualização de Nível de OS (Contêineres): utilizam recursos do kernel Linux para criar ambientes restritos, mas que compartilham o mesmo kernel.
    

Abstrações da cloud

Cloud Computing funciona criando Camadas de Abstração, ou seja, escondendo complexidade.

Hardware > Virtualização > Serviços de Infraestrutura > Serviços de Plataforma > Serviços de Aplicação

  
Perceba que a cada novo grau de abstração a complexidade se torna cada vez menor para o usuário, que poderá focar mais atenção em requisitos funcionais e não funcionais, de acordo com a necessidade de controle da infraestrutura, tamanho do time disponível ou capacidade técnica do mesmo.

Assim a abstração trabalha com os trade-offs que o usuário precisa assumir. Quanto maior o nível de abstração, menor o controle direto sobre a infraestrutura e a responsabilidade operacional.

### Modelo de responsabilidade compartilhada

É importante ressaltar que em Cloud Computing trabalhamos com o conceito de Responsabilidade Compartilhada, ou seja, a cloud não elimina a responsabilidade do cliente, apenas divide.

No geral, o cloud provider é responsável pela segurança da nuvem (instalações físicas, hardware, rede, etc), enquanto o usuário é responsável pela segurança na nuvem (acesso aos dados, IAM, atualizações, etc).

Conforme podemos constatar no livro [[Cloud FinOps]]:

> Os recursos de autoatendimento, escalabilidade e operação sob demanda permitem que um engenheiro invista o dinheiro da empresa apenas com um clique em um botão ou uma linha de código, sem passar pelos processos de aprovação tradicionais das áreas de finanças ou compras.

### Elasticidade e sob demanda

Uma das grandes vantagens da cloud é poder contratar recursos de acordo com a necessidade efetiva, diferente do modelo on-premises, onde servidores eram comprados de forma superdimensionada, ante a complexidade para realizar novas compras, que deveriam receber aprovação do Setor de Compras e Financeiro.

Elasticidade  é a capacidade de aumentar ou reduzir recursos de acordo com a necessidade, em casos de picos súbitos e erráticos. Isso pode ser realizado de forma automática através de Auto Scaling ou manualmente. 

Escalabilidade é a capacidade de lidar com o crescimento gradual de carga ao longo do tempo, como quando ocorre crescimento do negócio. 

### O que a cloud resolve (e o que não resolve)

O uso de Cloud resolve boa parte dos problemas encontrados em ambientes On-Premises. O primeiro deles é o Provisionamento Lento.  O ciclo de mensuração, requisição, aprovação e compra de servidores e licenças de software do modelo on-premises torna o provisionamento lento. Na nuvem, com poucos cliques é possível comprar e configurar um servidor de forma quase instantânea.

Essa característica deu origem a um dos princípios de FinOps, pelo qual cada envolvido se responsabiliza pelo uso que está fazendo da nuvem. A decisão de compra se descentralizou das mãos do setor Financeiro e foram para as mãos do time técnico e de engenheiros, que precisam se responsabilizar por custos do design da arquitetura e das operações em andamento. 

Outro problema que a nuvem resolve é a Possibilidade de Escalar Horizontalmente de maneira rápida e efetiva. A implementação pode ser realizada através de Auto Scaling ou IaC (Infraestructure as Code).

Em terceiro lugar, Alta Disponibilidade através de Zonas de Disponibilidade, Regiões e estratégias Multi-Zone e Multi-Region.

Na parte financeira, redução do uso de CAPEX, já que os servidores deixam de ser patrimônio adquirido e depreciável e passam a ser contratos de consumo.  

Quanto ao que não resolve:

- Arquitetura ruim: se o sistema é mal projetado, uso de cloud não vai salvar.
    
- Código ruim: código ineficiente continua sendo obstáculo, por melhor que seja a infraestrutura projetada.
    
- Falta de Governança: falta de políticas, regras de provisionamento, acessos e monitoramento continuam sendo um problema.
    
- Latência Física: a velocidade da luz limita o tempo das respostas e dados que transitam entre regiões distantes vão levar mais tempo para chegar.
    