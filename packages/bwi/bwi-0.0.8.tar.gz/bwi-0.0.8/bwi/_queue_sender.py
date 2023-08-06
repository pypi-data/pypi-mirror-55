import json
import os
import pika

RABBIT_HOST = os.environ.get('BWI_RABBIT_HOSTNAME')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST')
RABBIT_USERID = os.environ.get('BWI_RABBIT_USER')
RABBIT_PASSWORD = os.environ.get('BWI_RABBIT_PASSWORD')
RABBIT_CREDENTIALS = pika.PlainCredentials(RABBIT_USERID, RABBIT_PASSWORD)
_rabbit_channel = None


def get_connection():
    global _rabbit_channel
    if _rabbit_channel is not None:
        return _rabbit_channel
    rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST,
                                  credentials=RABBIT_CREDENTIALS,
                                  virtual_host=RABBIT_VHOST))
    _rabbit_channel = rabbit_connection.channel()
    return _rabbit_channel


def send_to_queue(queue_name: str, message: str):
    message = json.dumps(message)
    get_connection().basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message)
    print('Sent message "' + message + '" to queue "' + queue_name + '"')
