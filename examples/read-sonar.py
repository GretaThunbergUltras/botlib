#!/usr/bin/python3

from botlib.bot import Bot
from botlib.sonar import Sonar

def main():
    bot = Bot()

    try:
        while True:
            dst = bot.sonar().read_all()
            print('left:', dst[Sonar.LEFT], 'left45:', dst[Sonar.LEFT45], 'left_front:', dst[Sonar.LEFT_FRONT], 'right_front:', dst[Sonar.RIGHT_FRONT], 'right45:', dst[Sonar.RIGHT45], 'right:', dst[Sonar.RIGHT], 'back:', dst[Sonar.BACK])
    except KeyboardInterrupt:
        print('ende')

if __name__ == '__main__':
    main()
