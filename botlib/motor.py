from .brickpi3 import *

class Motor:
    _bp = BrickPi3()

    STATUS_POWER = 1

    def __init__(self, port, pmin=None, pmax=None):
        self._port = port

        # TODO: remove this limitation once we have proper power management
        self._bp.set_motor_limits(self._port, 85)

    def status(self):
        return self._bp.get_motor_status(self._port)

    # gracefully morph current power to pnew
    def change_power(self, pnew):
        import math
        import time

        if 100 < abs(pnew):
            return

        STEP_SIZE = 25.0
        pcur = self.status()[self.STATUS_POWER]
        # delta < 0: slow down; 0 < delta: accelerate
        delta = pnew - pcur
        steps = math.ceil(abs(delta)/STEP_SIZE)
        inc = delta/float(steps)

        for _ in range(steps):
            pcur += inc
            self._bp.set_motor_power(self._port, pcur)
            time.sleep(0.25)
        self._bp.set_motor_power(self._port, pnew)

    def stop(self):
        self.change_power(0)

class CalibratedMotor(Motor):
    def __init__(self, port, pmin=None, pmax=None, calpow=20):
        super().__init__(port, pmin, pmax)

        # power with which the motor will be calibrated
        self._calpow = calpow
        # minimum position
        self._pmin = pmin
        # maximum position
        self._pmax = pmax
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

