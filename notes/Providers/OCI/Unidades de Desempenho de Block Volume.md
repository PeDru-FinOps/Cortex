#oci #cloudcomputing #data_engineering
### Unidades de Desempenho de Volumes🔗

O desempenho do serviço [[OCI Block Volume]] inclui o conceito de unidades de desempenho de volumes (VPUs). Você pode comprar mais VPUs para alocar mais recursos para um volume, aumentando o IOPS/GB e o throughput por GB. Você também tem a flexibilidade de comprar menos VPUs, o que reduz as características de desempenho de um volume, no entanto, também pode fornecer economia de custo. Você também pode optar por não comprar VPUs, o que pode fornecer economia de custo significativa para volumes que não exigem o aumento das características de desempenho.

Para obter detalhes específicos sobre preços, consulte [Preço do Oracle Storage Cloud](https://www.oracle.com/cloud/storage/pricing.html).

A tabela a seguir lista as características de desempenho para cada nível de desempenho, juntamente com o número de VPUs.

|Nível de Desempenho Elástico|VPUs (Unidades de Desempenho de Volumes)|IOPS por GB|Máximo de IOPS por Volume|Tamanho Máximo de IOPS (GB)|KBPS por GB|Máximo de MBPS por Volume|
|---|---|---|---|---|---|---|
|Custo Inferior|0|2|3.000|1.500|240|480|
|Balanceado|10|60|25.000|417|480|480|
|Melhor Desempenho|20|75|50.000|667|600|680|
|Altíssimo Desempenho|30|90|75.000|833|720|880|
|Altíssimo Desempenho|40|105|100.000|952|840|1.080|
|Altíssimo Desempenho|50|120|125.000|1.042|960|1.280|
|Altíssimo Desempenho|60|135|150.000|1.111|1.080|1.480|
|Altíssimo Desempenho|70|150|175.000|1.167|1.200|1.680|
|Altíssimo Desempenho|80|165|200.000|1.212|1.320|1.880|
|Altíssimo Desempenho|90|180|225.000|1.250|1.440|2.080|
|Altíssimo Desempenho|100|195|250.000|1.282|1.560|2.280|
|Altíssimo Desempenho|110|210|275.000|1.310|1.680|2.480|
|Altíssimo Desempenho|120|225|300.000|1.333|1.800|2.680|

### Calculando o Desempenho do Volume🔗

Você pode calcular o desempenho esperado para um volume usando os seguintes cálculos:

- A partir de 10 VPUs (nível de desempenho **Balanceado**), para cada incremento de 10 VPUs/GB, o desempenho é escalado da seguinte forma:
    
    - + escala de 15 IOPS/GB
        
    - + 25K IOPS para limite máximo de IOPS/Volume (até o máximo de 300K IOPS para 120 VPU/GB)
        
    - + escala de 120 KBPS/GB
        
    - + Limite máximo de 200 MBPS/Volume
        
- IOPS/GB = 1,5 * VPU/GB + 45
    
- Máximo de IOPS/Volume = 2.500 * VPU/GB
    
- KBPS/GB = 12 * VPU/GB + 360
    
- Máximo de MBPS/Volume = 20 * VPU/GB + 280