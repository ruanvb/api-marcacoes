#API Responsável por receber e enviar as marcações ao RabbitMQ

from flask import Flask, jsonify, request, render_template
import pika
from config import rabbitmq_server

#utilizado Flask
app = Flask(__name__, template_folder='template')

logs = []

#criada rota para renderizar a página de marcação de ponto web
@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/logs')
def pagina_logs():
    return render_template('logs.html')

@app.route('/CarregaLogRabbit', methods=['GET'])
def carregar_log():
    return jsonify(logs)

@app.route('/cadastraLogRabbit', methods=['POST'])
def incluir_log():
    novo_log = request.get_json()
    logs.append(novo_log)

    return jsonify(logs)


#criada rota para enviar mensagem ao rabbit
@app.route('/marcacao', methods=['POST'])
def inlcuir_marcacao():
    nova_marcacao = request.get_json()

    #valida campos obrigatórios na chamada da API
    if nova_marcacao["includedAt"] is None:
        retorno = [{'message': 'Erro: a data da marcação "includedAt" não foi informada.'}]
        return jsonify(retorno), 500
    elif nova_marcacao["employeeId"] is None:
        retorno = [{'message': 'Erro: a empresa origem "employeeId" não foi informada.'}]
        return jsonify(retorno), 500
    elif nova_marcacao["employerId"] is None:
        retorno = [{'message': 'Erro: o colaborador "employerId" não foi informada.'}]
        return jsonify(retorno), 500
    else:
        #em caso de sucesso, realiza a conexão
        parametros = pika.URLParameters(rabbitmq_server["url_connection"])
        connection = pika.BlockingConnection(parametros)
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_server["queue"], durable=True)
        channel.confirm_delivery()
        #publica mensagem no rabbit
        channel.basic_publish(exchange='',
                            routing_key='marcacao-ponto',
                            body=str(nova_marcacao),
                            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

        connection.close()

        #retorna payload
        return nova_marcacao

#inicia flask no servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0')

    