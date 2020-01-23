from .brickpi3 import *

class Motor:
    _bp = BrickPi3()

    # TODO: call set_motor_limits for limiting power
    def __init__(self, port, pmin=None, pmax=None):
        self._port = port
        self._pmin = pmin
        self._pmax = pmax
        self._pinit = None

    def status(self):
        return self._bp.get_motor_status(self._port)

    # gracefully morph current power to pnew
    def change_power(self, pnew):
        #if (self._pmin and self._pmax) and not (self._pmin <= pnew <= self._pmax):
            #raise Exception('power {} is out of bounds for motor {}'.format(pnew, self._port))
        self._bp.set_motor_power(self._port, pnew)

    def stop(self):
        self.change_power(0)

class CalibratedMotor(Motor):
    # TODO: call set_motor_limits for limiting power
    def __init__(self, port, pmin=None, pmax=None, calpow=20):
        super().__init__(port, pmin, pmax)

        # power with which the motor will be calibrated
        self._calpow = calpow
        # initial position for this motor. will be determined in `calibrate`
        self._pinit = None

    # adjust minimum and maximum values
    def calibrate(self):
        import time

        self.change_power(-self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            time.sleep(0.5)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmin = encnow
        self.change_power(0)

        self.change_power(self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            time.sleep(0.5)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmax = encnow
        self.change_power(0)

        if self._pmax == self._pmin:
            raise Exception('motor {} does not move'.format(self._port))

        self._pinit = (self._pmax + self._pmin) * 0.5
        time.sleep(0.5)
        self.to_init_position()

    def to_init_position(self):
        if not self._pinit:
            raise Exception('initial position for motor {} not known'.format(self._port))
        self._bp.set_motor_position(self._port, self._pinit)

