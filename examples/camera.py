#!/usr/bin/python3

"""
adjust motor position values to default state
"""

from botlib.bot import Bot

def main():
    bot = Bot()
    bot.camera().start()
    bot.camera().enable_preview()

    while input('press q') == 'q':
        pass

    bot.camera().stop()

if __name__ == '__main__':
    main()
