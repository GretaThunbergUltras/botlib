REMOTE_PORT = 6666

class Action:
    """
    Standardized actions that a `Bot` can execute.
    """

    STOP = 1
    STEER_LEFT = 2
    STEER_RIGHT = 4
    SPEED_UP = 8
    SPEED_DOWN = 16
    FORKLIFT_PICKUP = 32
    FORKLIFT_CARRY = 64

    STEER = 128
    SPEED = 256
    FORKLIFT_HEIGHT_POWER = 512
    FORKLIFT_ROTATE_POWER = 1024
    FOLLOW_LINE = 2048

    def __init__(self, cmd, data=None):
        self.cmd = cmd
        self.data = data

    def parse(seq):
        """
        Parses a string into an `Action` object.

        :param seq: a string in the form `<cmd>:<data>` where `<data>` is optional. `<cmd>` must be an int, 
        `<data>` must be a float.
        :returns: an `Action` object.
        """
        parts = seq.split(':')
        data = float(parts[1]) if 2 <= len(parts) else None
        return Action(int(parts[0]), data)

    def to(cmd, data=None):
        """
        Turn a command and some data into a string.

        :param cmd: an integer defining the action.
        :param data: a float containing the payload.
        :returns: the message as a string.
        """
        return '{}:{}'.format(cmd,data) if data else '{}'.format(cmd)

    def __str__(self):
        return Action.to(self.cmd, self.data)
