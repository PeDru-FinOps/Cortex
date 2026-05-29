#azure #arquitetura_solucoes #cloudcomputing

Um diagrama de arquitetura de referência é um modelo de infraestrutura no qual uma solução da Microsoft Marketplace se baseia. Para soluções de PI (propriedade intelectual) do Azure, o diagrama também deve mostrar como sua solução usa os serviços de nuvem da Microsoft de acordo com os requisitos técnicos de venda conjunta de PI.

Um diagrama de referência não se destina a avaliar a qualidade de uma arquitetura. A intenção é mostrar como sua solução usa os serviços da Microsoft.

Você pode criar um diagrama de arquitetura de referência usando várias ferramentas.

## Componentes típicos de um diagrama de arquitetura de referência

Seu diagrama de arquitetura de referência deve identificar claramente seu IP como uma solução, aplicativo ou código de serviço que seja implantado _em_ e _o consumo de_ Microsoft Azure.

Seu código deve ser altamente reutilizável e não depender da personalização abrangente por implantação.

O diagrama deve fornecer uma boa compreensão de como sua solução usa os serviços da Microsoft. O diagrama deve incluir o seguinte:

- Uma descrição de alto nível do fluxo de dados fornecendo uma compreensão das interações entre componentes do diagrama
- Limites lógicos para nuvem do Azure, nuvem do cliente, ambiente local e integração com outros serviços de nuvem
- Serviços de nuvem do Azure que hospedam e interagem com sua solução, incluindo os que consomem recursos do Azure
- Identificação do código de PROPRIEDADE Intelectual Repetível (IP) ; o código que você está fornecendo como parte da solução
- Interfaces do usuário e outros serviços expondo a solução
###### Exemplo de diagrama de arquitetura de referência: chatbot vertical do setor

A imagem a seguir é um exemplo de um diagrama de arquitetura de referência que ilustra um chatbot vertical do setor que pode ser integrado com sites de intranet para ajudar a prever cenários de demanda usando um algoritmo de machine learning. Ele usa dados de cadeia de suprimentos e de agendamento de fabricação de vários sistemas ERP (planejamento de recursos corporativos). O bot foi projetado para responder a perguntas sobre quando um vendedor pode se comprometer com possíveis datas de entrega para um pedido.

[![Captura de tela de um diagrama de arquitetura de referência que ilustra um chatbot vertical do setor.](https://learn.microsoft.com/pt-br/partner-center/media/referrals/co-sell-architecture-diagram.png)](https://learn.microsoft.com/pt-br/partner-center/media/referrals/co-sell-architecture-diagram.png#lightbox)

## Referências

https://learn.microsoft.com/pt-br/partner-center/referrals/reference-architecture-diagram#typical-components-of-a-reference-architecture-diagram