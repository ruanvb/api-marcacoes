#API Responsável por receber e enviar as marcações ao RabbitMQ

from flask import Flask, jsonify, request, render_template
import pika
from config import rabbitmq_server

app = Flask(__name__, template_folder='template')

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/marcacao', methods=['POST'])
def inlcuir_marcacao():
    nova_marcacao = request.get_json()
    
    print(nova_marcacao["includedAt"])
    print(nova_marcacao["employeeId"])
    print(nova_marcacao["employerId"])

    parametros = pika.URLParameters(rabbitmq_server["url_connection"])
    connection = pika.BlockingConnection(parametros)
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_server["queue"], durable=True)
    channel.confirm_delivery()
    channel.basic_publish(exchange='',
                        routing_key='marcacao-ponto',
                        body=str(nova_marcacao),
                        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()

    retorno = [
        {
            'message': 'success'
        }
    ]

    return jsonify(retorno)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

    