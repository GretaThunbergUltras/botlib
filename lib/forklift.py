class Forklift:
    def __init__(self, bot):
        self._ROTATE_MOTOR = bot._bp.PORT_C
        self._ROTATE_MOTOR_MIN = 0
        self._ROTATE_MOTOR_MAX = 0
        self._HEIGHT_MOTOR = bot._bp.PORT_A
        self._HEIGHT_MOTOR_MIN = 0
        self._HEIGHT_MOTOR_MAX = 0

        self._bot = bot

    def calibrate(self):
        # adjust minimum and maximum values
        pass

    def to_carry_mode():
        # rotate backwards
        # move fork up
        pass

    def to_pickup_mode():
        # rotate forward
        # move fork down
        pass
