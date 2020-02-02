#!/usr/bin/python3

"""
adjust motor position values to default state
"""

from botlib.bot import Bot

def main():
    Bot().calibrate()

if __name__ == '__main__':
    main()
