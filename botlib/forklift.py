from .motor import CalibratedMotor

class Forklift:
    def __init__(self, bot):
        self._bot = bot

        self._rotate_motor = CalibratedMotor(CalibratedMotor._bp.PORT_C)
        self._height_motor = CalibratedMotor(CalibratedMotor._bp.PORT_A, calpow=40)

    def stop_all(self):
        self._rotate_motor.stop()
        self._height_motor.stop()

    def calibrate(self):
        # TODO: standard calibration routine does not work well with this one
        # self._rotate_motor.calibrate()
        self._height_motor.calibrate()

    def to_carry_mode():
        # rotate backwards
        # move fork up
        pass

    def to_pickup_mode():
        # rotate forward
        # move fork down
        pass
