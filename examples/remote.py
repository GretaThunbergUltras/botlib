#!/usr/bin/python3

def clamp(vmin, v, vmax):
    return max(vmin, min(v, vmax))

def main():
    import sys

    from botlib.bot import Bot
    from readchar import readkey, key

    bot = Bot()
    STEP_POWER, STEP_STEER = 10, 0.5
    power, steer = 0, 0.0
    running = True

    if '--camera' in sys.argv:
        bot._camera.start()
        bot._camera.enable_preview()

    print('calibrating...')
    bot.calibrate()

    print('Up/Down: manage speed, Left/Right: manage direction, w/s: Carry/Pickup, Space: stop, Backspace: exit')

    while running:
        inp = readkey()
        if inp == key.DOWN or inp == key.UP:
            power += STEP_POWER if inp == key.UP else -STEP_POWER
            power = clamp(-100, power, 100)
            bot.drive_power(power)
        elif inp == key.RIGHT or inp == key.LEFT:
            steer += STEP_STEER if inp == key.RIGHT else -STEP_STEER
            steer = clamp(-1.0, steer, 1.0)
            bot.drive_steer(steer)
        elif inp == key.SPACE:
            bot.stop_all()
            power, steer = 0, 0
        elif inp == 'w':
            bot._forklift.to_carry_mode()
        elif inp == 's':
            bot._forklift.to_pickup_mode()
        elif inp == key.BACKSPACE:
            print('stopping...')
            bot.stop_all()
            running = False

    if '--camera' in sys.argv:
        bot._camera.stop()
        
    print('bye...')

if __name__ == '__main__':
    main()
