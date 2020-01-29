from readchar import readkey, key
from inputs import devices, get_gamepad

PORT = 6666

class Protocol:
    MSG_STOP = 1
    MSG_STEER_LEFT = 2
    MSG_STEER_RIGHT = 4
    MSG_SPEED_UP = 8
    MSG_SPEED_DOWN = 16
    MSG_FORKLIFT_PICKUP = 32
    MSG_FORKLIFT_CARRY = 64

    MSG_STEER = 128
    MSG_SPEED = 256
    MSG_FORKLIFT_HEIGHT_POWER = 512
    MSG_FORKLIFT_ROTATE_POWER = 1024

    def parse(seq):
        parts = seq.split(':')
        msg = {
            'cmd': int(parts[0]),
            'data': None
        }
        if 2 <= len(parts):
            msg['data'] = float(parts[1])
        return msg

    def to(cmd, data=None):
        return '{}:{}'.format(cmd,data) if data else '{}'.format(cmd)

def send_command(s, cmd, body=None):
    msg = Protocol.to(cmd, body)
    s.sendall(msg.encode('ascii'))

def keyboard_to_protocol(inp):
    keymap = {
        key.RIGHT: Protocol.MSG_STEER_RIGHT,
        key.LEFT: Protocol.MSG_STEER_LEFT,
        key.UP: Protocol.MSG_SPEED_UP,
        key.DOWN: Protocol.MSG_SPEED_DOWN,
        'w': Protocol.MSG_FORKLIFT_PICKUP,
        's': Protocol.MSG_FORKLIFT_CARRY
    }
    if inp not in keymap:
        return None
    return keymap[inp]

def control_keyboard(s):
    inp = None
    while inp != key.BACKSPACE:
        inp = readkey()
        cmd = keyboard_to_protocol(inp)
        if cmd != None:
            send_command(s, cmd)

def control_gamepad(s):
    power = 0
    while True:
        events = get_gamepad()
        for event in events:
            # TODO: implement `select` to disconnect
            if event.code == "ABS_RZ":
                power = round(event.state / 10.23, 0)
                send_command(s, Protocol.MSG_SPEED, power)
            elif event.code == "ABS_Z":
                power = round(event.state / 10.23, 0)
                send_command(s, Protocol.MSG_SPEED, -power)
            #elif event.code == "ABS_RY":
            #    if (event.state >= 0 < power) or (event.state < 0 > power):
            #        power = power * (-1)
            #    # power = round(event.state/327.67, 0)
            #    send_command(s, Protocol.MSG_SPEED, power)
            elif event.code == "ABS_X":
                steer = round(event.state / 32767, 2)
                send_command(s, Protocol.MSG_STEER, steer)
            elif event.code == "ABS_HAT0X":
                if event.state == 1:
                    send_command(s, Protocol.MSG_FORKLIFT_ROTATE_POWER, 80)
                elif event.state == -1:
                    send_command(s, Protocol.MSG_FORKLIFT_ROTATE_POWER, -80)
                else:
                    send_command(s, Protocol.MSG_FORKLIFT_ROTATE_POWER, 0)
            elif event.code == "ABS_HAT0Y":
                if event.state == 1:
                    send_command(s, Protocol.MSG_FORKLIFT_HEIGHT_POWER, 80)
                elif event.state == -1:
                    send_command(s, Protocol.MSG_FORKLIFT_HEIGHT_POWER, -80)
                else:
                    send_command(s, Protocol.MSG_FORKLIFT_HEIGHT_POWER, 0)

def main():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = input('address: ')
        s.connect((addr, PORT))
        print('connected.')

        if devices.gamepads:
            control_gamepad(s)
        else:
            control_keyboard(s)

if __name__ == '__main__':
    main()
