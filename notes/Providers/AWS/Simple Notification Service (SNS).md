#aws #cloudcomputing #arquitetura_solucoes 

## O que é o SNS

É um serviço de entrega de notificações utilizando padrão Publisher/Subscriber. Um evento é enviado para o SNS que fica responsável por direcionar uma notificação para o serviço desejado. Ele funciona como um canal de comunicação. É composto por:

- Publisher: aplicação responsável pelo envio das mensagens
- Subscriber: aplicação que deseja consumir as mensagens
- Tópico: mecanismo utilizado para enviar e transmitir as mensagens

## Destinos possíveis

### A2A - Aplicação para aplicação

- AWS Lambda
- Amazon SQS
- Kinesis Data Firehose
- HTTP/HTTPS
### A2P Aplicação para pessoa

- E-Mail
- SMS
- Mobile Push


