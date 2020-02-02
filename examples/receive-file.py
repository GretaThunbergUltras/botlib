#!/usr/bin/python3

from botlib.broker import Broker

import base64
import time

def callback(cid, userdata, msg):
    with open('image.jpeg', 'wb') as out:
        out.write(base64.b64decode(msg.payload))

def main():
    subs = {
        'test_channel': callback
    }

    b = Broker('receiverbot', subscriptions=subs)

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
