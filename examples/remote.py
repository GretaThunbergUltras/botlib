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
                print('server received', int(inp))
                handle_event(inp)
                if inp == key.BACKSPACE:
                    print('stopping...')
                    bot.stop_all()
                    break

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

def handle_event(inp):
    global bot
    global power
    global steer

    STEP_POWER, STEP_STEER = 10, 0.25
    return

    if inp == Protocol.MSG_SPEED_DOWN or inp == Protocol.MSG_SPEED_UP:
        power += STEP_POWER if inp == Protocol.MSG_SPEED_UP else -STEP_POWER
        power = clamp(-100, power, 100)
        bot.drive_power(power)
    elif inp == Protocol.MSG_STEER_RIGHT or inp == Protocol.MSG_STEER_LEFT:
        steer += STEP_STEER if inp == Protocol.MSG_STEER_RIGHT else -STEP_STEER
        steer = clamp(-1.0, steer, 1.0)
        bot.drive_steer(steer)
    elif inp == Protocol.MSG_STOP:
        bot.stop_all()
        power, steer = 0, 0
    elif inp == Protocol.MSG_FORKLIFT_CARRY:
        bot._forklift.to_carry_mode()
    elif inp == Protocol.MSG_FORKLIFT_PICKUP:
        bot._forklift.to_pickup_mode()
    elif inp == Protocol.MSG_STEER:
        pass
    elif inp == Protocol.MSG_SPEED:
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
