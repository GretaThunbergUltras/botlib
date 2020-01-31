from .brickpi3 import *

class Motor:
    """
    Wrapper for BrickPi3 motor control.
    """

    _bp = BrickPi3()

    STATUS_POWER = 1

    def __init__(self, port):
        """
        Create a `Motor` instance.

        :param port: which BrickPi motor to address.
        """
        self._port = port

        # TODO: remove this limitation once we have proper power management
        self._bp.set_motor_limits(self._port, 85)

    def status(self):
        """
        Retrieve information about the motor e.g. position, power.
        """
        return self._bp.get_motor_status(self._port)

    def change_power(self, pnew):
        """
        Set the new power of the motor. This function gracefully transitions the current power 
        to parameter `pnew`.

        :param pnew: a value between -100 and 100. if value is not in range, nothing will be changed.
        """
        import math
        import time

        if 100 < abs(pnew):
            return

        STEP_SIZE = 25.0
        pcur = self.status()[self.STATUS_POWER]
        # delta < 0: slow down; 0 < delta: accelerate
        delta = pnew - pcur
        steps = math.ceil(abs(delta)/STEP_SIZE)

        if steps == 0:
            return

        inc = delta/float(steps)

        for _ in range(steps):
            pcur += inc
            self._bp.set_motor_power(self._port, pcur)
            time.sleep(0.25)
        self._bp.set_motor_power(self._port, pnew)

    def stop(self):
        """
        Turn motor power to zero.
        """
        self.change_power(0)

class CalibratedMotor(Motor):
    """
    A `Motor` that can be positioned. Due to positions being different on every bot,
    such `Motor`s need to be `calibrated` first.
    """

    def __init__(self, port, pmin=None, pmax=None, calpow=20):
        """
        Create a `CalibratedMotor` instance. If 

        :param port: which BrickPi motor to address.
        :param pmin: the minimum position (if known).
        :param pmax: the maximum position (if known).
        :param calpow: the power with which the motor will be calibrated.
        """
        super().__init__(port, pmin, pmax)

        # power with which the motor will be calibrated
        self._calpow = calpow
        # minimum position
        self._pmin = pmin
        # maximum position
        self._pmax = pmax

        # if min and max were given, calculate initial position
        if self._pmin and self._pmax:
            self._pinit = (self._pmax + self._pmin) * 0.5
        else:
            # initial position for this motor. will be determined in `calibrate`
            self._pinit = None

    # adjust minimum and maximum values
    def calibrate(self):
        """
        Determine minimum, maximum and initial position. This sets the motor power to `calpow`
        and waits until the position does not change anymore giving minimum position. Repeat
        process in the opposite direction afterwards. The initial position is the median between both values.

        Hacky, but works in most cases.
        """
        import time

        CALIBRATE_SLEEP = 0.75

        self.change_power(-self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            time.sleep(CALIBRATE_SLEEP)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmin = encnow
        self.change_power(0)

        self.change_power(self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            time.sleep(CALIBRATE_SLEEP)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmax = encnow
        self.change_power(0)

        if self._pmax == self._pmin:
            raise Exception('motor {} does not move'.format(self._port))

        self._pinit = (self._pmax + self._pmin) * 0.5
        time.sleep(0.5)
        self.to_init_position()

    def change_position(self, pnew):
        """
        Set the new position of the motor.
        
        :param pnew: If minimum and maximum are known, this value must be between both.
        """
        if (self._pmin and self._pmax) and not (self._pmin <= pnew <= self._pmax):
            raise Exception('position ({} < {} < {}) is invalid for motor {}'.format(self._pmin, pnew, self._pmax, self._port))
        self._bp.set_motor_position(self._port, pnew)

    def to_init_position(self):
        """
        Reset the motor to its initial position. Throws exception if value is not known.
        """
        if not self._pinit:
            raise Exception('initial position for motor {} not known'.format(self._port))
        self.change_position(self._pinit)

    def position_from_factor(self, factor):
        """
        Determines the position from a factor. Minimum, maximum and initial position must be known.

        :param factor: number between -1.0 and 1.0. 
        """
        assert self._pinit and self._pmin and self._pmax
        if 0 == factor:
            return self._pinit
        if 0 < factor:
            return self._pinit + (self._pmax - self._pinit) * factor
        return self._pinit - (self._pinit - self._pmin) * abs(factor)
