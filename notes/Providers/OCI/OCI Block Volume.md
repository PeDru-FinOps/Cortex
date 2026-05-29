#oci #cloudcomputing #data_engineering

[[Armazenamento em Bloco]] é uma forma de armazenamento em nuvem usado para manter dados, onde são armazenados em blocos com endereço exclusivo. O armazenamento em bloco também oferece um nível impressionante de flexibilidade porque pode ser acessado por diferentes sistemas operacionais como volumes de unidades montadas e tem a capacidade de usar sistemas de arquivos específicos do sistema operacional (como o New Technology File System (NTFS) para Windows e Virtual Machine File System (VMFS) para VMware).

O Oracle Cloud Infrastructure (OCI) Block Volumes fornece armazenamento em bloco confiável, de alto desempenho e baixo custo que persiste além da vida útil de uma máquina virtual, com redundância integrada e capacidade de dimensionamento para 1 PB por instância de computação.

O serviço Oracle Cloud Infrastructure Block Volume usa infraestrutura de armazenamento baseada em NVMe, projetada para consistência, e oferece desempenho flexível e elástico. Você só precisa provisionar a capacidade necessária e o desempenho será escalado com as características do nível selecionado até o nível máximo do serviço.

Você não precisa decidir sobre as necessidades de desempenho antes de criar e anexar volumes em blocos. Quando você cria um volume, por padrão, ele é configurado para o nível de desempenho **Balanceado**. Você pode alterar essa opção ao criar o volume ou pode atualizá-lo a qualquer momento após a criação do volume. A capacidade de desempenho elástico do serviço permite pagar pelas características de desempenho necessárias, independentemente do tamanho dos volumes em blocos e dos volumes de inicialização. Se os requisitos mudarem, você só precisará ajustar as definições de desempenho para o volume; não será necessário criar novamente os volumes.
## Níveis de Desempenho do Serviço Block Volume🔗

Quando você cria um volume, pode selecionar o nível de desempenho. Consulte [Criando um Volume em Blocos](https://docs.oracle.com/pt-br/iaas/Content/Block/Tasks/creatingavolume.htm "Crie um volume em blocos no serviço Block Volumes."). Você também pode alterar o nível de desempenho de um volume existente. Para obter mais informações, consulte [Alterando o Desempenho de um Volume](https://docs.oracle.com/pt-br/iaas/Content/Block/Tasks/changingvolumeperformance.htm "O serviço Block Volume permite que você configure dinamicamente o nível de desempenho para volumes em blocos e de inicialização."). Na Console, você configura o desempenho usando o controle deslizante ou o controle de VPU, conforme mostrado na captura de tela a seguir.

Os seguintes níveis de desempenho estão disponíveis:

- **Altíssimo Desempenho**: Recomendado para cargas de trabalho com os mais altos requisitos de E/S, exigindo o melhor desempenho possível. Com essa opção, você pode comprar entre 30 e 120 VPUs por GB/mês. Para obter mais informações, incluindo o throughput e os números de desempenho de IOPS específicos para vários tamanhos de volume, consulte [Altíssimo Desempenho](https://docs.oracle.com/pt-br/iaas/Content/Block/Concepts/blockvolumeultrahighperformance.htm "O nível Altíssimo Desempenho é recomendado para cargas de trabalho com requisitos de E/S mais altos, exigindo o melhor desempenho possível, como bancos de dados grandes.").
- **Melhor Desempenho**: Recomendado para workloads com requisitos altos de E/S que não exigem o desempenho do nível **Altíssimo Desempenho**. Com essa opção, você está comprando 20 VPUs por GB/mês. Para obter mais informações, incluindo o throughput e os números de desempenho de IOPS específicos para vários tamanhos de volume, consulte [Desempenho Mais Alto](https://docs.oracle.com/pt-br/iaas/Content/Block/Concepts/blockvolumehigherperformance.htm "A opção de Desempenho Superior é recomendada para workloads com requisitos altos de E/S que não exigem o desempenho do nível de Desempenho Ultra Alto.").
- **Balanceado**: O nível de desempenho padrão para volumes de inicialização e em blocos novos e existentes e fornece um bom equilíbrio entre desempenho e economia na maioria dos fluxos de trabalho. Com essa opção, você está comprando 10 VPUs por GB/mês. Para obter mais informações, incluindo o throughput e os números de desempenho de IOPS específicos para vários tamanhos de volume, consulte [Desempenho Equilibrado](https://docs.oracle.com/pt-br/iaas/Content/Block/Concepts/blockvolumebalancedperformance.htm "O nível de desempenho Balanceado oferece um bom equilíbrio entre desempenho e economia de custo para a maioria das cargas de trabalho, incluindo aquelas que executam E/S aleatória, como volumes de inicialização.").
- **Custo Inferior**: recomendado para cargas de trabalho de throughput intenso com E/S sequencial, como streaming, processamento de log e data warehouses. O custo é somente de armazenamento, não há custo de VPU adicional. Essa opção só está disponível para volumes em blocos; ela não está disponível para volumes de inicialização. Para obter mais informações, incluindo o throughput e os números de desempenho de IOPS específicos para vários tamanhos de volume, consulte [Menor Custo](https://docs.oracle.com/pt-br/iaas/Content/Block/Concepts/blockvolumelowercost.htm "A opção de desempenho elástico Menor Custo é recomendada para cargas de trabalho de throughput intenso com E/S sequencial, como streaming, processamento de log e data warehouses.").

## Tipos de Desempenho

As [[Unidades de Desempenho de Block Volume]] são:
### 1. Balanced

Tipo padrão e mais utilizado.

- Equilíbrio entre custo e performance
- Adequado para:
    - aplicações gerais
    - bancos de dados pequenos/médios
    - servidores web
    - workloads corporativos comuns

Características:

- IOPS e throughput medianos
- Escala proporcional ao tamanho do volume
- Boa relação custo-benefício

---

### 2. Higher Performance

Voltado para workloads intensivos.

Indicado para:

- bancos de dados de alta performance
- analytics
- aplicações com alta taxa de I/O
- sistemas críticos de baixa latência

Características:

- Mais IOPS
- Maior throughput
- Latência reduzida
- Custo superior ao Balanced

---

### 3. Ultra High Performance (UHP)

Perfil extremo de performance.

Usado para:

- Oracle Database crítico
- SAP HANA
- workloads HPC
- aplicações extremamente sensíveis à latência

Características:

- Altíssimas IOPS
- Throughput muito elevado
- Performance consistente
- Alto custo

---

### 4. Lower Cost

Otimizado para economia.

Indicado para:

- backup operacional
- ambientes de desenvolvimento
- dados pouco acessados
- workloads não críticos

Características:

- Menor custo por GB
- Menor performance
- IOPS reduzidas
## Referências

https://docs.oracle.com/pt-br/iaas/Content/Block/Concepts/overview.htm
https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumeperformance.htm?utm_source=chatgpt.com

