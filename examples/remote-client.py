from readchar import readkey, key
from remote import PORT, Protocol

def send_command(s, cmd):
    if isinstance(cmd, str):
        s.sendall(cmd.encode('ascii'))
    else:
        s.sendall(bytes(cmd))

def control_keyboard(s):
    keymap = {
        key.RIGHT: Protocol.MSG_STEER_RIGHT,
        key.LEFT: Protocol.MSG_STEER_LEFT,
        key.UP: Protocol.MSG_SPEED_UP,
        key.DOWN: Protocol.MSG_SPEED_DOWN,
        'w': Protocol.MSG_FORKLIFT_PICKUP,
        's': Protocol.MSG_FORKLIFT_CARRY
    }
    inp = None
    while inp != key.BACKSPACE:
        inp = readkey()
        if inp in keymap:
            send_command(s, keymap[inp])

def control_gamepad(s):
    # TODO: Hi, louis. do stuff here pls
    pass

def main():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = input('address: ')
        s.connect((addr, PORT))
        
        control_keyboard(s)

if __name__ == '__main__':
    main()
