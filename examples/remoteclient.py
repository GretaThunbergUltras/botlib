#!/usr/bin/python3

from botlib.control import Action, REMOTE_PORT
from readchar import readkey, key
from inputs import devices, get_gamepad

def send_action(s, action):
    s.sendall(str(action).encode('ascii'))

def keyboard_to_action(inp):
    keymap = {
        key.RIGHT: Action.STEER_RIGHT,
        key.LEFT: Action.STEER_LEFT,
        key.UP: Action.SPEED_UP,
        key.DOWN: Action.SPEED_DOWN,
        key.SPACE: Action.STOP,
        'w': Action.FORKLIFT_PICKUP,
        's': Action.FORKLIFT_CARRY,
        'f': Action.FOLLOW_LINE
    }
    if inp not in keymap:
        return None
    return Action(keymap[inp])

def gamepad_to_action(evt):
    if event.code == 'BTN_EAST' and event.state == 1:
        return Action(Action.STOP)
    elif event.code == 'ABS_RZ':
        power = round(event.state / 10.23, 0)
        return Action(Action.SPEED, power)
    elif event.code == 'ABS_Z':
        power = round(event.state / 10.23, 0)
        return Action(Action.SPEED, -power)
    elif event.code == 'ABS_X':
        steer = round(event.state / 32767, 2)
        return Action(Action.STEER, steer)
    elif event.code == 'ABS_HAT0X':
        if event.state == 1:
            data = 80
        elif event.state == -1:
            data = -80
        else:
            data = 0
        return Action(Action.FORKLIFT_ROTATE_POWER, data)
    elif event.code == 'ABS_HAT0Y':
        if event.state == 1:
            data = 80
        elif event.state == -1:
            data = -80
        else:
            data = 0
        return Action(Action.FORKLIFT_HEIGHT_POWER, data)
    return None

def control_keyboard(s):
    inp = None
    while inp != key.BACKSPACE:
        inp = readkey()
        action = keyboard_to_action(inp)
        if action != None:
            send_action(s, action)

def control_gamepad(s):
    while True:
        events = get_gamepad()
        for event in events:
            action = gamepad_to_action(event)
            if action != None:
                send_action(s, action)

def main():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = input('address: ')
        s.connect((addr, REMOTE_PORT))
        print('connected.')

        if devices.gamepads:
            print('reading gamepad.')
            control_gamepad(s)
        else:
            print('reading keyboard.')
            control_keyboard(s)

if __name__ == '__main__':
    main()
