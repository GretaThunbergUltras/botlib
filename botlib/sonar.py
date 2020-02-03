import ctypes
from typing import List, Any, Union

class Sonar:
    LEFT = 0
    LEFT45 = 1
    LEFT_FRONT = 2
    RIGHT_FRONT = 3
    RIGHT_45 = 4
    RIGHT = 5
    BACK = 6

    def __init__(self, bot):

        self._bot = bot
        # FIXME: How many sonic devices have you plugged in? default: 7
        self._sensor_count = 7

        # TODO: search for shared object; don't hardcode path
        self._sonic = ctypes.CDLL('/usr/local/lib/libsonic.so')
        self._sonic.measure.restype = ctypes.c_double
        self._sonic.initialize()

    def read(self, sensor: int):
        return self._sonic.measure(ctypes.c_uint(sensor))

    def read_all(self):
        results = []
        for i in range(self._sensor_count):
            ret = self.read(i)
            if ret == 0:
                i -= 1
            else:
                results.append(round(ret, 2))
        return results

