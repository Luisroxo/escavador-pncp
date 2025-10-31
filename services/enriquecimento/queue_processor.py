import pika
import json
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "cnpj_processing")

def process_message(ch, method, properties, body):
    try:
        logging.info("Mensagem recebida da fila.")
        message = json.loads(body)
        cnpj = message.get("cnpj")
        if not cnpj:
            logging.warning("Mensagem inválida: CNPJ ausente.")
            return

        logging.info(f"Processando CNPJ: {cnpj}")
        # Aqui você pode chamar a função enriquecer_cnpj ou outra lógica de processamento
        # enriquecer_cnpj(cnpj)

        logging.info(f"CNPJ {cnpj} processado com sucesso.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def main():
    try:
        logging.info("Conectando ao RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        logging.info(f"Fila '{RABBITMQ_QUEUE}' declarada com sucesso.")

        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)
        logging.info("Aguardando mensagens. Para sair, pressione CTRL+C.")

        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Encerrando consumidor de fila.")
    except Exception as e:
        logging.error(f"Erro na conexão com o RabbitMQ: {e}")

if __name__ == "__main__":
    main()