# api-marcacoes

## Objetivo
API Responsável por enviar marcações ao RabbitMQ.

## Sobre a Solução 
Atualmente a API está hospedada em um servidor gratuito.

É possível acessar a página inicial através da URL https://api-marcacao-ponto.herokuapp.com/.

O arquivo config.py carrega as configurações para a execução.

## EndPoints disponíveis
* ./ - Marcação de Ponto Web
* ./marcacao - POST - Cadastra marcacação na fila do RabbitMQ
    - Payload de exemplo:

```json
{"includedAt":"2021-03-15 15:10:00", "employeeId": 123, "employerId": 999} 
```

## Testes
O testes da API pode, ser realizado diretamente pela Marcação de Ponto Web, entretanto, caso achar viável, poderá ser realizado testes via aplicativo Postman.