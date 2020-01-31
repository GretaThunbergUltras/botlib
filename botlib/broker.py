from paho.mqtt.client import Client

import base64
import json

BROKER_HOST = 'Broker'
BROKER_PORT = 1883

class Broker:
    """
    Respresents a connection to the MQTT broker.
    """
    def __init__(self, name, host=BROKER_HOST, port=BROKER_PORT, subscriptions=None):
        """
        Create an instance and connect to broker.

        :param name: the clients id.
        :param host: the hoststring for the broker.
        :param port: the port of the broker.
        :param subscriptions: a dictionary in the form `topic name (string) => function to execute (callback)`. callback must be 
        able to receive three arguments - namely `client_id`, `userdata`, `message`.
        """
        self._name = name

        self._host = host
        self._port = port

        self._client = Client()
        self._client.connect(self._host, self._port, 60)

        self._subscribed_thread = None

        if subscriptions:
            self._subscribe(subscriptions)

    def _subscribe(self, subscriptions):
        from threading import Thread

        def on_connect(client_id, userdata, flags, rc):
            print('subscribed with code {}'.format(rc))

        def listen():
            for topic, callback in subscriptions.items():
                self._client.callback(callback, topic=topic, hostname=self._host)
            self._client.loop_forever()

        self._client.on_connect = on_connect

        self._subscribed_thread = Thread(group=None, target=listen, daemon=True)
        self._subscribed_thread.start()

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
