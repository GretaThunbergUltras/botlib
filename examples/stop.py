#!/usr/bin/python3

"""
stops all motors
"""

from botlib.bot import Bot

def main():
    print('stopping all...')
    Bot().stop_all()
    print('done...')

if __name__ == '__main__':
    main()
