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
                req = Protocol.parse(inp)
                print('server received', req['cmd'], req['data'])
                handle_event(req['cmd'], req['data'])

def run_local():
    from remoteclient import keyboard_to_protocol

    inp = None

    print('Up/Down: manage speed, Left/Right: manage direction, w/s: Carry/Pickup, Space: stop, Backspace: exit')

    while inp != key.BACKSPACE:
        inp = readkey()
        cmd = keyboard_to_protocol
        if cmd != None:
            handle_event(inp)
    stop()

def handle_event(cmd, data=None):
    global bot
    global power
    global steer

    STEP_POWER, STEP_STEER = 10, 0.25

    if cmd == Protocol.MSG_SPEED:
        bot.drive_power(data)
    if cmd == Protocol.MSG_STEER:
        bot.drive_steer(data)
    if cmd == Protocol.MSG_SPEED_DOWN or cmd == Protocol.MSG_SPEED_UP:
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
