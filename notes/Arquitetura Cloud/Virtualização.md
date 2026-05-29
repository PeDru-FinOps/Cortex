#arquitetura_solucoes #cloudcomputing 
### Hypervisors

É o componente responsável por abstrair os recursos físicos (CPU, Memória, Rede e Armazenamento) e distribuí-los entre múltiplas instâncias virtuais. Existem dois tipos:

- Tipo 1 (Bare metal): executa diretamente sobre o hardware, sendo o mais eficiente e seguro.
    
- Tipo 2 (Hosted): executa sobre um sistema operacional, sendo mais comum em ambientes de desenvolvimento e teste.

O uso de hypervisors permite isolamento entre cargas de trabalho.

### Máquinas virtuais

Uma máquina virtual é uma instância isolada que simula um computador completo, incluindo sistema operacional, CPU, memória e disco. Oferece: 

  - Forte isolamento entre workloads
    
- Compatibilidade com diferentes sistemas operacionais
    
- Facilidade de migração e replicação
    
### Overcommit e isolamento

Para maximizar a utilização de recursos físicos utiliza-se uma técnica chamada overcommitment, que consiste em alocar mais recursos virtuais do que os recursos físicos disponíveis. Exemplo:

 Um servidor físico de 8 núcleos físicos pode disponibilizar mais de 8 vCPUs, assumindo que nem todas as máquinas virtuais utilizarão sua capacidade máxima simultaneamente. Isso pode gerar um problema chamado noisy neighbor problem, onde uma VM consume excessivamente e impacta o desempenho das demais.

 Isolamento entre VMs é garantido pelo Hypervisor, porém não elimina completamente a disputa por recursos físicos.

### Performance e custos

O modelo de cloud implica em custos diretamente proporcionais ao uso dos recursos, como tempo de execução da VM, quantidade de vCPU e memória alocados e uso de armazenamento e rede. Isso cria um trade-off importante:

  Maior isolamento e controle geralmente implica em maior custo e menor eficiência dos recursos.

 Entende-se eficiência como utilização do hardware alocado. Uma VM pode não utilizar todo desempenho contratado na sua configuração, além de utilizar parte dos recursos apenas para gerir o sistema operacional.

### Quando VMs fazem sentido

  - Aplicações legadas que dependem de um sistema operacional específico
    
- Workloads que exigem controle total do ambiente
    
- Sistemas não projetados para arquitetura distribuída
    
- Ambientes com requisitos de isolamento rígidos
    
### Limitações do modelo

  - Inicialização lenta
    
- Maior consumo de recursos
    
- Menor densidade de workloads
    
- Gestão operacional mais complexa
