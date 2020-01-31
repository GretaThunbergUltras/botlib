from paho.mqtt.client import Client

import base64
import json

BROKER_HOST = 'Broker'
BROKER_PORT = 1883

class Broker:
    """
    Respresents a connection to the MQTT broker.
    """
    def __init__(self, host=BROKER_HOST, port=BROKER_PORT, subscriptions=None):
        """
        Create an instance and connect to broker.

        :param host: the hoststring for the broker.
        :param port: the port of the broker.
        :param subscriptions: a dictionary in the form `topic name (string) => function to execute (callback)`.
        """
        self._client = Client()
        self._client.connect(host, port, 60)

        if subscriptions:
            for topic, callback in subscriptions.items():
                pass

    def _publish(self, topic, payload, qos=0):
        # TODO: add json headers here
        # msg = json.encode()
        self._client.publish(topic, payload, qos=qos)

    def send_message(self, topic, message):
        """
        Send a text message to the broker.

        :param topic: mqtt topic to which the message will be published.
        :param payload: the message as string.
        """
        self._publish(topic, message)

    def send_file(self, topic, payload):
        """
        Send a file to the broker.

        :param topic: mqtt topic to which the message will be published.
        :param payload: the binary content of the file.
        """
        self._publish(topic, base64.encode(payload))
