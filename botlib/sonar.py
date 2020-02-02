import ctypes
from typing import List, Any, Union

class Sonic:
    def __init__(self):
        # FIXME: How many sonic devices have you plugged in? default: 7
        self._sensor_count = 7

        self._sonic = ctypes.CDLL('/usr/local/lib/libsonic.so')
        self._sonic.measure.restype = ctypes.c_double
        self._sonic.initialize()

    def get_distance(self):
        results = []
        for i in range(self._sensor_count):
            ret = self._sonic.measure(ctypes.c_uint(i))
            if ret == 0:
                i -= 1
            else:
                results.append(round(ret, 2))
        return results
