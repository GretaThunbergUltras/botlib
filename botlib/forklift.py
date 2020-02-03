from .motor import CalibratedMotor

class Forklift:
    """
    The bots forklift.
    """
    def __init__(self, bot):
        self._bot = bot

        self._rotate_motor = CalibratedMotor(CalibratedMotor._bp.PORT_C, calpow=70)
        self._height_motor = CalibratedMotor(CalibratedMotor._bp.PORT_A, calpow=50)

    def __del__(self):
        self._height_motor.to_init_position()

    def stop_all(self):
        """
        Stop rotation and height motor.
        """
        self._rotate_motor.stop()
        self._height_motor.stop()

    def calibrate(self):
        """
        Find minimum and maximum position for motors.
        """
        # TODO: standard calibration routine does not work well with this one
        # self._rotate_motor.calibrate()
        self._rotate_motor._pmin = self._rotate_motor._pinit = -128
        self._rotate_motor._pmax = 15603

        self._height_motor.calibrate()

    def to_carry_mode(self):
        """
        Position forklift to carry an object around.
        """
        # rotate backwards
        self._rotate_motor.change_position(self._rotate_motor._pmax)

        # move fork up
        self._height_motor.to_init_position()

    def to_pickup_mode(self):
        """
        Position forklift for picking up an object.
        """
        # rotate forward
        self._rotate_motor.to_init_position()

        # move fork down
        pos = self._height_motor.position_from_factor(-1.0)
        self._height_motor.change_position(pos)

    def set_custom_height(self, height):
        # rotate forward
        self._rotate_motor.to_init_position()
        # move fork on the right height
        height = ((height/13.5)*2)-1
        #height = height / (maxHeight/2)-1
        pos = self._height_motor.position_from_factor(height)
        self._height_motor.change_position(pos)
