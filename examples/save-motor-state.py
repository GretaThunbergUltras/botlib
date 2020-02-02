#!/usr/bin/python3

from botlib.bot import Bot
from datetime import datetime

def main():
    bot = Bot()
    now = str(datetime.now())
    fname = '/tmp/status-{}-{}'.format(now[0:10], now[11:16])

    with open(fname, 'w') as temp:
        temp.write('Drive {}\n'.format(bot._drive_motor.status()))
        temp.write('Steer {}\n'.format(bot._steer_motor.status()))
        temp.write('Forklift Rotate {}\n'.format(bot._forklift._rotate_motor.status()))
        temp.write('Forklift Height {}\n'.format(bot._forklift._height_motor.status()))

    print('saved motor positions to {}'.format(fname))

if __name__ == '__main__':
    main()
