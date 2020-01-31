import base64
import time

from botlib.broker import Broker

def callback(cid, userdata, msg):
    with open('image.jpeg', 'wb') as out:
        out.write(base64.b64decode(msg.payload))

subs = {
    'test_channel': callback
}

b = Broker('jockel', subscriptions=subs)

while True:
    time.sleep(1)
