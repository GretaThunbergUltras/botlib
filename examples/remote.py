#!/usr/bin/python3

from botlib.bot import Bot
from readchar import readkey, key
from remoteclient import PORT, Protocol

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
        s.bind(('', PORT))
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
                    req = Protocol.parse(inp)
                    print('server received', req['cmd'], req['data'])
                    handle_event(req['cmd'], req['data'])
                except ValueError:
                    print('package invalid')
                except Exception as e:
                    print(e)
                    stop()
                    break

def run_local():
    from remoteclient import keyboard_to_protocol
    from inputs import devices, get_gamepad

    if devices.gamepads:
        while True:
            events = get_gamepad()
            for event in events:
                # TODO: implement `select` to disconnect
                if event.code == 'BTN_EAST' and event.state == 1:
                    handle_event(Protocol.MSG_STOP)
                elif event.code == "ABS_RZ":
                    power = round(event.state / 10.23, 0)
                    handle_event(Protocol.MSG_SPEED, power)
                elif event.code == "ABS_Z":
                    power = round(event.state / 10.23, 0)
                    handle_event(Protocol.MSG_SPEED, -power)
                # elif event.code == "ABS_RY":
                #    if (event.state >= 0 < power) or (event.state < 0 > power):
                #        power = power * (-1)
                #    # power = round(event.state/327.67, 0)
                #    send_command(s, Protocol.MSG_SPEED, power)
                elif event.code == "ABS_X":
                    steer = round(event.state / 32767, 2)
                    handle_event(Protocol.MSG_STEER, steer)
                elif event.code == "ABS_HAT0X":
                    if event.state == 1:
                        handle_event(Protocol.MSG_FORKLIFT_ROTATE_POWER, 80)
                    elif event.state == -1:
                        handle_event(Protocol.MSG_FORKLIFT_ROTATE_POWER, -80)
                    else:
                        handle_event(Protocol.MSG_FORKLIFT_ROTATE_POWER, 0)
                elif event.code == "ABS_HAT0Y":
                    if event.state == 1:
                        handle_event(Protocol.MSG_FORKLIFT_HEIGHT_POWER, 80)
                    elif event.state == -1:
                        handle_event(Protocol.MSG_FORKLIFT_HEIGHT_POWER, -80)
                    else:
                        handle_event(Protocol.MSG_FORKLIFT_HEIGHT_POWER, 0)
    else:
        inp = None

        print('Up/Down: manage speed, Left/Right: manage direction, w/s: Carry/Pickup, Space: stop, Backspace: exit')

        while inp != key.BACKSPACE:
            inp = readkey()
            cmd = keyboard_to_protocol(inp)
            if cmd != None:
                handle_event(inp)
    stop()

def handle_event(cmd, data=None):
    global bot
    global power
    global steer

    STEP_POWER, STEP_STEER = 10, 0.25

    pval = data if data != None else 0

    if cmd == Protocol.MSG_SPEED:
        bot.drive_power(pval)
    elif cmd == Protocol.MSG_STEER:
        bot.drive_steer(pval)
    elif cmd == Protocol.MSG_FORKLIFT_HEIGHT_POWER:
        bot._forklift._height_motor.change_power(pval)
    elif cmd == Protocol.MSG_FORKLIFT_ROTATE_POWER:
        bot._forklift._rotate_motor.change_power(pval)
    elif cmd == Protocol.MSG_SPEED_DOWN or cmd == Protocol.MSG_SPEED_UP:
        if data:
            power = data
        else:
            power += STEP_POWER if cmd == Protocol.MSG_SPEED_UP else -STEP_POWER
            power = clamp(-100, power, 100)
        bot.drive_power(power)
    elif cmd == Protocol.MSG_STEER_RIGHT or cmd == Protocol.MSG_STEER_LEFT:
        if data:
            steer = data
        else:
            steer += STEP_STEER if cmd == Protocol.MSG_STEER_RIGHT else -STEP_STEER
            steer = clamp(-1.0, steer, 1.0)
        bot.drive_steer(steer)
    elif cmd == Protocol.MSG_STOP:
        bot.stop_all()
        power, steer = 0, 0
    elif cmd == Protocol.MSG_FORKLIFT_CARRY:
        bot._forklift.to_carry_mode()
    elif cmd == Protocol.MSG_FORKLIFT_PICKUP:
        bot._forklift.to_pickup_mode()
    elif cmd == Protocol.MSG_STEER:
        pass
    elif cmd == Protocol.MSG_SPEED:
        pass

def main():
    import sys

    global bot

    if '--camera' in sys.argv:
        bot._camera.start()
        bot._camera.enable_preview()

    print('calibrating...')
    bot.calibrate()

    if '--server' in sys.argv:
        create_server()
    else:
        run_local()

    if '--camera' in sys.argv:
        bot._camera.stop()

if __name__ == '__main__':
    main()
