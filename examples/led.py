#!/usr/bin/python3

"""
test the orange status led
"""

from botlib.bot import Bot
from botlib.led import LEDStatus

from random import choice

def main():
    bot = Bot()
    led = bot.led()

    led.set_status(LEDStatus.FADE)

    while input('press q') != 'q':
        mode = choice([LEDStatus.FADE, LEDStatus.BLINK, LEDStatus.BLINK_FAST])
        print('new mode is', mode)
        led.set_status(mode)

if __name__ == '__main__':
    main()
