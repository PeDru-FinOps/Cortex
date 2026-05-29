#oci #cloudcomputing #data_engineering

Nova funcionalidade com as seguintes características:

- Oracle cobra de acordo com a performance units por GB por month.
- Grande quantidade de IOPS e throughput corresponde a VPU.
- VPU é inversamente proporcional ao custo do armazenamento.
- Medido em termos de IO per sec e Throughput por GB.

Para o Block Volume Elastic Performance, existem três opções de configuração de desempenho elástico, como descrito abaixo.

**Balanced:** Esta é a configuração padrão para novos block volumes e boot volumes e também que já existem. Ele fornece um bom equilíbrio entre desempenho e economia de custos para a maioria das cargas de trabalho, incluindo aqueles que executam I/O aleatórios tais como boot volumes. Esta opção proporciona dimensionamento linear de peformance com 60 IOPS/GB até 25.000 IOPS por volume.Throughtput scales de 480 KBPS/GB até um máximo de 480 MBPS por volume. Com esta opção, você está comprando 10 VPUs por GB/mês.

**Higher Performance****:** Recomendado para cargas de trabalho com os requisitos de I/O mais altos, exigindo o melhor desempenho possível, como grandes bancos de dados. Esta opção oferece a melhor escala de desempenho linear com 75 IOPS/GB até um máximo de 35.000 IOPS por volume. Throughput também escalas na taxa mais alta em 600 KBPS/GB até um máximo de 480 MBPS por volume. Com esta opção, você está comprando 20 VPUs por GB/mês.

**Lower Cost:** Recomendado para a entrada intensiva workloads com grande I/O sequencial, como streaming, processamento de log e armazéns de dados. O custo é apenas o custo de armazenamento, não há custo adicional de VPU.  Esta opção da uma escala linear 2 IOPS/GB até um máximo de 3000 IOPS por volume. Esta opção só está disponível para block volumes, não está disponível para boot volumes.

A tabela a seguir lista as características de desempenho para cada nível de desempenho elástico.

|                    |         |                 |               |                       |         |
| ------------------ | ------- | --------------- | ------------- | --------------------- | ------- |
| Performance Level  | IOPS/GB | Max IOPS/Volume | Throughput/GB | Max Throughput/Volume | VPUs/GB |
| Lower Cost         | 2       | 3000            | 240           | Up to 480             | 0       |
| Balanced           | 60      | 25,000          | 480           | 480                   | 10      |
| Higher Performance | 75      | 35,000          | 600           | 480                   | 20      |

## Criando um new volume

Faça login no Oracle Cloud e clique no Block Storage e selecione o Block Volumes.

![](https://www.oracle.com/technetwork/es/images/image001-5944777.jpg)

Clique em Create Block Volume

![](https://www.oracle.com/technetwork/es/images/image002-5944778.jpg)

Insira os detalhes do Block Volume e clique em “Create Block Volume”

```
Name: BV_PERF_UNIT 
Compartment : <keep value> 
Availability Domain : <keep value>   
Size (in GB) : 50  
Compartment for Backup Policies : <keep value> 
Backup Policy:  Bronze   
Volume Perfomance : Lower Cost – For this example  
Encryption : Encrypt using Oracle-Managed Keys.
```

![](https://www.oracle.com/technetwork/es/images/image003-5944779.jpg)![](https://www.oracle.com/technetwork/es/images/image004-5944780.jpg)![](https://www.oracle.com/technetwork/es/images/image005-5944781.png)

Este processo levará entre 1 e 2 minutos para ser concluído.

![](https://www.oracle.com/technetwork/es/images/image006-5944782.jpg)![](https://www.oracle.com/technetwork/es/images/image007-5944783.jpg)

## Alterando o volume performance

Faça login no Oracle Cloud e clique no Block Storage e selecione o  Block Volumes.

![](https://www.oracle.com/technetwork/es/images/image008-5944785.jpg)

Selecione o seu block volume. Para este exemplo BV_PERF_UNIT

![](https://www.oracle.com/technetwork/es/images/image009-5944786.jpg)

Clique em “Change Performance”

![](https://www.oracle.com/technetwork/es/images/image010-5944787.jpg)

Agora é possível que você selecione a melhor opção para o seu ambiente.  Para este teste, vamos selecionar o “Balanced” e clique em “Change Performance”

![Agora é possível que você](https://www.oracle.com/technetwork/es/images/image011-5944788.jpg)![Agora é possível que você](https://www.oracle.com/technetwork/es/images/image012-5944789.jpg)

Este processo levará entre 1 e 2 minutos para ser concluído.

![](https://www.oracle.com/technetwork/es/images/image013-5944791.jpg)![](https://www.oracle.com/technetwork/es/images/image014-5944792.jpg)

A partir de agora, OCI Block Volume Elastic Performance tem 2 limitações:

- Só altera a configuração de desempenho elástico de volumes de blocos em três volumes simultaneamente por tenancy.
- Os volumes de inicialização têm apenas 2 opções: Balanced or Higher performance.
## API para mudar configuração de VPU

Use a operação **UpdateVolume** com o atributo **`vpusPerGB`** dentro de **`UpdateVolumeDetails`**.
## É necessário dar restart da máquina no procedimento?

**Para mudar VPU entre Lower Cost, Balanced e Higher Performance:**  
em regra, **não há exigência documentada de restart da instância**. A documentação descreve a alteração como configuração dinâmica de performance para block volumes e boot volumes.

Durante a alteração de VPU, o volume entra em estado **Provisioning**. Nesse período, não é possível anexar o volume ou executar outras operações nele. Depois, ele volta para **Available**.

A Oracle também limita a alteração concorrente de performance a **três volumes por tenancy**.

**Exceção importante:**  

se você alterar um **block volume** para **Ultra High Performance**, vindo de outro nível, a Oracle documenta que é necessário **detach e attach novamente o volume**. Neste caso vai gerar indisponibilidade do disco.
## Referências

https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/update-performance-block-bv-volume.htm

https://www.oracle.com/br/technical-resources/articles/cloudcomp/block-volume-perf-unit.html

https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/changingvolumeperformance.htm

### API para Update de Volume

https://docs.oracle.com/en-us/iaas/api/#/en/iaas/20160918/Volume/UpdateVolume

https://docs.oracle.com/en-us/iaas/api/#/en/iaas/20160918/datatypes/UpdateVolumeDetails