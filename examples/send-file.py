#!/usr/bin/python3

from botlib.broker import Broker
from io import BytesIO
import picamera

def main():
    broker = Broker('senderbot', host='localhost')
    buf = BytesIO()

    with picamera.PiCamera() as cam:
        cam.capture(buf, format='jpeg')

    buf.seek(0)
    broker.send_file('/status', buf.read())

if __name__ == '__main__':
    main()
