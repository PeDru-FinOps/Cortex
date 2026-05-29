#cloud8 #aws #governance 

A ideia seria criar um tópico [[Simple Notification Service (SNS)]] na AWS, configurá-lo na Cloud8 e utilizar esse SNS para enviar notificações para um webhook no Teams.

A integração via SNS da AWS pode ser utilizada justamente para desacoplar o envio dos alertas da Cloud8 e redistribuí-los para outros destinos, como Microsoft Teams, Slack, webhooks internos, Lambda, entre outros.

O fluxo ficaria mais ou menos assim:

Cloud8 → SNS Topic (AWS) → Subscriber/Webhook → Canal do Teams

Nesse caso:

- A Cloud8 publicaria os alertas de budget no tópico SNS configurado;
- O SNS faria a entrega da mensagem para um subscriber configurado;
- Esse subscriber poderia ser, por exemplo:
    - uma AWS Lambda que formata a mensagem e envia para o webhook do Teams;
    - um endpoint HTTP/HTTPS intermediário;
    - ou até serviços de automação como Power Automate.

Importante apenas observar que o Microsoft Teams não consome SNS diretamente de forma nativa. Normalmente é necessário um intermediário (Lambda, API Gateway, Power Automate etc.) para adaptar o payload recebido do SNS ao formato esperado pelo webhook do Teams.

Pela documentação da Cloud8, o SNS é suportado como mecanismo de integração/notificação da AWS, então a arquitetura é compatível com esse tipo de cenário. Um procedimento semelhante é encontrado em [[Como integrar o Melhores Práticas com o Teams]]