#API Responsável por receber e enviar as marcações ao RabbitMQ

from flask import Flask, jsonify, request, render_template
import pika

app = Flask(__name__, template_folder='template')

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/marcacao', methods=['POST'])
def inlcuir_marcacao():
    nova_marcacao = request.get_json()
    
    parametros = pika.URLParameters('amqps://qsvvrqtm:XCvydaLcdvhxgwOUKjXAfviC3G30nK8f@woodpecker.rmq.cloudamqp.com/qsvvrqtm')
    connection = pika.BlockingConnection(parametros)
    channel = connection.channel()
    channel.queue_declare(queue='marcacao-ponto', durable=True)
    channel.confirm_delivery()
    channel.basic_publish(exchange='',
                        routing_key='marcacao-ponto',
                        body=str(nova_marcacao),
                        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()

    retorno = [
        {
            'message': 'Marcação incluída com sucesso!'
        }
    ]

    return jsonify(retorno)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

    