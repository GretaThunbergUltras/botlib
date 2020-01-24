from .motor import Motor

class Forklift:
    def __init__(self, bot):
        self._bot = bot

        self._rotate_motor = Motor(Motor._bp.PORT_C)
        self._height_motor = Motor(Motor._bp.PORT_A)

    def calibrate(self):
        self._rotate_motor.calibrate()
        self._height_motor.calibrate()

    def to_carry_mode():
        # rotate backwards
        # move fork up
        pass

    def to_pickup_mode():
        # rotate forward
        # move fork down
        pass
