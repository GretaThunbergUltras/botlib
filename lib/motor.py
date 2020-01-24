from .brickpi3 import *

class Motor:
    _bp = BrickPi3()

    def __init__(self, port, pmin=None, pmax=None):
        self._port = port
        self._pmin = pmin
        self._pmax = pmax

    def calibrate(self):
        # adjust minimum and maximum values
        pass

    # gracefully morph current power to pnew
    def change_power(self, pnew):
        if not (self._pmin <= pnew <= self._pmax):
            raise Exception('power {} is out of bounds for motor {}'.format(pnew, self._port))
        pass
