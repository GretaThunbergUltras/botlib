from paho.mqtt.client import Client

import base64
import json

BROKER_HOST = 'Broker'
BROKER_PORT = 1883

class Broker:
    def __init__(self, host=BROKER_HOST, broker=BROKER_PORT):
        self._client = Client()
        self._client.connect(host, port, 60)

    def _publish(self, topic, payload, qos=0):
        # TODO: add json headers here
        # msg = json.encode()
        self._client.publish(topic, payload, qos=qos)

    def send_message(self, topic, message):
        self._publish(topic, message)

    def send_file(self, topic, payload):
        self._publish(topic, base64.encode(payload))
