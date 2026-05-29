#arquitetura_solucoes #cloudcomputing #finops #security 

Em Arquitetura de Sistemas um trade-off é a decisão de sacrificar ou reduzir uma característica do sistema para fortalecer outra. Não existe solução perfeita, e o arquiteto deve trabalhar com o conceito do que é “menos pior”, mais adequado para os requisitos técnicos e de negócio. 

Avaliar um trade-off envolve basicamente três passos:

1. Identificar quais partes do sistema são afetadas por uma mudança.
    
2. Analisar o acoplamento.
    
3. Modelar cenários para cada domínio.
    

Segue abaixo alguns exemplos, embora iremos explorar o tema mais a frente de forma detalhada, quando formos abordar Requisitos Não-Funcionais.

Disponibilidade x Consistência 

Muitas vezes será necessário escolher entre um sistema mais consistente, que garante que os usuários utilizem dados o mais atualizado possível; ou ter um sistema com alta disponibilidade, operando e respondendo aos usuários mesmo que os dados estejam temporariamente desatualizados.

Performance x Consistência

Escolher entre diminuir a consistência para ganhar desempenho e diminuir a espera nas operações de escrita e leitura.

Escalabilidade x Complexidade x Custo

Escalar verticalmente aumenta a potência de um único servidor, aumentando o seu custo. Além disso, esse tipo de estratégia possui limitação física de upgrade. Por outro lado, escalar horizontalmente adiciona mais servidores e resolve o problema , mas também aumenta a complexidade operacional.

Segurança x Flexibilidade x Agilidade

Controles rígidos de segurança aumentam o grau de acoplamento dentro do sistema e criam dificuldade para mudança rápidas.

Resiliência x Custo

Aumentar a resiliência, ou seja, a capacidade de falhar e continuar operando exige redundância de hardware, o que torna o custo do ambiente cada vez maior. Cada “9” em disponibilidade reduz drasticamente o tempo de indisponibilidade, porém aumenta o custo na mesma proporção.