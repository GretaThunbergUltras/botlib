#!/usr/bin/python3

from botlib.bot import Bot
from botlib.control import Action, REMOTE_PORT
from readchar import readkey, key

bot = Bot()
power, steer = 0, 0.0

def clamp(vmin, v, vmax):
    return max(vmin, min(v, vmax))

def stop():
    print('stopping...')
    bot.stop_all()

def create_server():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', REMOTE_PORT))
        s.listen()
        print('listening...')
        con, addr = s.accept()
        print('connected...')
        with con:
            while True:
                inp = con.recv(1024).decode('ascii')
                if len(inp) == 0:
                    continue
                try:
                    action = Action.parse(inp)
                    print('server received', action.cmd, action.data)
                    handle_event(action)
                except ValueError:
                    print('package invalid')
                except Exception as e:
                    print(e)
                    stop()
                    break

def run_local():
    from remoteclient import keyboard_to_action

    print('Up/Down: manage speed, Left/Right: manage direction, w/s: Carry/Pickup, Space: stop, Backspace: exit')

    inp = None
    while inp != key.BACKSPACE:
        inp = readkey()
        action = keyboard_to_action(inp)
        if action != None:
            handle_event(action)
    stop()

def handle_event(action):
    global bot
    global power
    global steer

    STEP_POWER, STEP_STEER = 10, 0.25

    cmd = action.cmd
    pval = action.data if action.data != None else 0

    if cmd == Action.SPEED:
        bot.drive_power(pval)
    elif cmd == Action.STEER:
        bot.drive_steer(pval)
    elif cmd == Action.FORKLIFT_HEIGHT_POWER:
        bot.forklift()._height_motor.change_power(pval)
    elif cmd == Action.FORKLIFT_ROTATE_POWER:
        bot.forklift()._rotate_motor.change_power(pval)
    elif cmd == Action.SPEED_DOWN or cmd == Action.SPEED_UP:
        if action.data:
            power = action.data
        else:
            power += STEP_POWER if cmd == Action.SPEED_UP else -STEP_POWER
            power = clamp(-100, power, 100)
        bot.drive_power(power)
    elif cmd == Action.STEER_RIGHT or cmd == Action.STEER_LEFT:
        if action.data:
            steer = action.data
        else:
            steer += STEP_STEER if cmd == Action.STEER_RIGHT else -STEP_STEER
            steer = clamp(-1.0, steer, 1.0)
        bot.drive_steer(steer)
    elif cmd == Action.STOP:
        bot.stop_all()
        power, steer = 0, 0
    elif cmd == Action.FORKLIFT_CARRY:
        bot.forklift().to_carry_mode()
    elif cmd == Action.FORKLIFT_PICKUP:
        bot.forklift().to_pickup_mode()
    elif cmd == Action.STEER:
        pass
    elif cmd == Action.SPEED:
        pass

def main():
    import sys

    global bot

    if '--camera' in sys.argv:
        bot.camera().start()
        bot.camera().enable_preview()

    print('calibrating...')
    bot.calibrate()

    if '--server' in sys.argv:
        create_server()
    else:
        run_local()

    if '--camera' in sys.argv:
        bot.camera().stop()

if __name__ == '__main__':
    main()
