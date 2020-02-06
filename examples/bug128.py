#!/usr/bin/python3

"""
this example tries to initially resolve the -128-bug. it is a problem that
sets brickpi3's motor power out of bounds and causes unexpected jumps when
kicking off the botlib functionality. apparently, this issue only occurres
when the bot is booted off 'cold' i.e. the powerbank was not previously
started.

there are also two github issues related to the topic, namely:
https://github.com/GretaThunbergUltras/botlib/issues/21
https://github.com/DexterInd/BrickPi3/issues/112
"""

from botlib.bot import Bot
from botlib.motor import Motor

def main():
    bot = Bot()

    motors = [bot._drive_motor, bot._steer_motor, bot.forklift()._rotate_motor, bot.forklift()._height_motor]

    for motor in motors:
        power = motor.status()[Motor.STATUS_POWER]
        if not (-100 <= power <= 100):
            print('motor {} is out of bounds'.format(motor._port))
            motor.change_power(0)

if __name__ == '__main__':
    main()
