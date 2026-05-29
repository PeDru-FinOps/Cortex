#cloudcomputing #arquitetura_solucoes #data_engineering 

É uma forma de armazenamento em nuvem usado para manter dados, onde são armazenados em blocos com endereço exclusivo. O armazenamento em bloco também oferece um nível impressionante de flexibilidade porque pode ser acessado por diferentes sistemas operacionais como volumes de unidades montadas e tem a capacidade de usar sistemas de arquivos específicos do sistema operacional (como o New Technology File System (NTFS) para Windows e Virtual Machine File System (VMFS) para VMware).

## Benefícios do armazenamento em nuvem

O armazenamento em bloco é uma escolha popular por conta de seus inúmeros benefícios.

- **Alta eficiência:** O alto IOPS e a baixa latência do armazenamento em bloco o tornam ideal para aplicações que exigem alto desempenho.
- **Compatibilidade:** O armazenamento em bloco funciona em diferentes sistemas operacionais e de arquivos, tornando-o compatível para empresas, independentemente de sua configuração e ambiente.
- **Flexibilidade:** O armazenamento em bloco deixa o redimensionamento horizontal extremamente flexível. Os nós do cluster podem ser adicionados sempre que for necessário, melhorando a capacidade geral de armazenamento.
- **Eficiência para arquivos grandes:** Em arquivos grandes, como os de vídeo, os dados devem ser completamente substituídos ao usar arquivo ou [armazenamento de objeto](https://www.oracle.com/br/cloud/storage/block-volumes/what-is-block-storage/vs-object-storage/). Com o armazenamento em bloco, a aplicação de gerenciamento identifica apenas o bloco a ser alterado dentro do arquivo grande, aumentando a eficiência das atualizações de dados.

## Limitações do armazenamento em blocos

Assim como qualquer outra plataforma de tecnologia, o armazenamento em bloco traz algumas limitações, mesmo com tantos benefícios.

- **Mais custo:** Embora o armazenamento em bloco possa ser facilmente redimensionado, ele também pode ser caro por conta dos custos com SANs. Além disso, requer treinamento mais especializado para gerenciamento e manutenção, aumentando a despesa geral.
- **Limitações de desempenho:** Com o armazenamento em bloco, os metadados são integrados e hierárquicos, e são definidos pelo sistema de arquivos. Como os dados são dividos em blocos, pesquisar pelo arquivo completo exige que todas as peças sejam identificadas corretamente. Isso pode criar problemas de desempenho para operações que acessam os metadados, principalmente com pastas com um grande número de arquivos. Enquanto o limite gira em torno de 10.000 arquivos, alguns problemas são vistos com diretórios que contêm somente 1.000 arquivos.

## Casos de uso de armazenamento em bloco

Assim como o [armazenamento de objetos](https://www.oracle.com/br/cloud/storage/object-storage/) e outros tipos de [armazenamento em nuvem](https://www.oracle.com/br/cloud/storage/what-is-cloud-storage/), o em blocos funciona melhor em circunstâncias específicas com base nas necessidades do usuário e em determinados parâmetros. Veja a seguir alguns casos efetivos sobre casos de uso do armazenamento em bloco:

- **Contêineres:** O armazenamento em bloco oferece suporte ao uso de plataformas de contêiner, como [Kubernetes](https://www.oracle.com/br/cloud-native/container-engine-kubernetes/what-is-kubernetes/), criando um volume de blocos que permite armazenamento persistente para todo o contêiner. Isso possibilita gestão e migração limpas dos contêineres, sempre que precisar.
- **Servidores de email:** Os servidores de email podem aproveitar a flexibilidade e a escalabilidade do armazenamento em bloco. De fato, no caso do Microsoft Exchange, o armazenamento em bloco é necessário devido à falta de suporte para armazenamento conectado à rede.
- **Bancos de dados:** O armazenamento em bloco é rápido, eficiente, flexível e escalável, oferecendo suporte a volumes redundantes. Isso permite suportar bancos de dados, principalmente aqueles que lidam com um grande volume de consultas e onde a latência deve ser minimizada.
- **Recuperação de desastres:** O armazenamento em bloco pode ser uma solução de backup redundante para armazenamento nearline e restauração rápida, com dados movidos rapidamente do backup para a produção por meio de acesso fácil.