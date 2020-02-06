#!/usr/bin/python3

"""
test the orange status led
"""

from botlib.bot import Bot
from botlib.led import LEDStatus

def main():
    bot = Bot()
    led = bot.led()

    led.set_status(LEDStatus.FADE)

    while input('press q') != 'q':
        pass

if __name__ == '__main__':
    main()
