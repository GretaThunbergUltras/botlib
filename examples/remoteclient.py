from readchar import readkey, key
from remote import PORT, Protocol

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

def send_command(s, cmd):
    s.sendall(cmd.encode('ascii'))

def control_keyboard(s):
    inp = None
    while inp != key.BACKSPACE:
        inp = readkey()
        cmd = keyboard_to_protocol(inp)
        if cmd != None:
            send_command(s, cmd)

def control_gamepad(s):
    # TODO: Hi, louis. do stuff here pls
    pass

def main():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = input('address: ')
        s.connect((addr, PORT))

        if True:
            control_gamepad(s)
        else:
            control_keyboard(s)

if __name__ == '__main__':
    main()
