# 1. Objetivo - Criar uma API que possibilite cadastrar marcações para envio ao RabbitMQ
# 2. URL Base - localhost
# 3. Endpoints -
    # - localhost/marcacao
# 4. Recursos - registro da marcação do ponto

from flask import Flask, jsonify, request
import pika

app = Flask(__name__)
    
@app.route('/marcacao', methods=['POST'])
def inlcuir_marcacao():
    nova_marcacao = request.get_json()
    
    parameters = pika.URLParameters('amqps://qsvvrqtm:XCvydaLcdvhxgwOUKjXAfviC3G30nK8f@woodpecker.rmq.cloudamqp.com/qsvvrqtm')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='marcacao-ponto', durable=True)

    channel.basic_publish(exchange='',
                        routing_key='marcacao-ponto',
                        body=str(nova_marcacao))

    connection.close()

    retorno = [
        {
            'message': 'Marcação incluída com sucesso!'
        }
    ]

    return jsonify(retorno)

app.run()

    