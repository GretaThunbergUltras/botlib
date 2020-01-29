#!/usr/bin/python3

def clamp(vmin, v, vmax):
    return max(vmin, min(v, vmax))

def main():
    import sys

    from botlib.bot import Bot
    from readchar import readkey, key
    from inputs import devices, get_gamepad

    bot = Bot()
    STEP_POWER, STEP_STEER = 10, 0.25
    power, steer = 0, 0.0
    running = True

    if '--camera' in sys.argv:
        bot._camera.start()
        bot._camera.enable_preview()

    print('calibrating...')
    bot.calibrate()

    print('Up/Down: manage speed, Left/Right: manage direction, w/s: Carry/Pickup, Space: stop, Backspace: exit')

    while running:
        if devices.gamepads:
            events = get_gamepad()
            for event in events:
                # print(event.ev_type, event.code, event.state)
                if event.code == "ABS_RZ":
                    power = round(event.state / 10.23, 0)
                if event.code == "ABS_RY":
                    if (event.state >= 0 < power) or (event.state < 0 > power):
                        power = power * (-1)
                    # power = round(event.state/327.67, 0)
                    bot.drive_power(power)
                    # print("power: " + str(power))
                if event.code == "ABS_X":
                    bot.drive_steer(round(event.state / 32767, 2))
                    # print("steering:" + str(round(event.state / 32767, 2)))
                if event.code == "ABS_HAT0X":
                    if event.state == 1:
                        bot._forklift.to_pickup_mode()
                    else:
                        bot._forklift.to_carry_mode()
                """if event.code == "ABS_HAT0Y":
                    if event.state == -1:
                        print("Forklift up")
                    else:
                        print("Forklift down")"""


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
