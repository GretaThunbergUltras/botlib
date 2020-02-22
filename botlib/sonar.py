import ctypes
from typing import List, Any, Union

class Sonar:
    LEFT = 0
    LEFT45 = 1
    LEFT_FRONT = 2
    RIGHT_FRONT = 3
    RIGHT45 = 4
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

    def _try_read(self, sensor, times=3):
        for _ in range(times):
            ret = self.read(sensor)
            if ret != None:
                return ret
        return None

    def read(self, sensor: int):
        """
        Read try to read a sensor value

        :param sensor: the id of the sensor.
        :return: the read distance (rounded) or `None` if read failed
        """
        ret = self._sonic.measure(ctypes.c_uint(sensor))
        return None if ret == 0 else round(ret, 2)

    def read_all(self):
        """
        Read all sensors.

        :return: an array having `self._sensor_count` items. if error occurred on 
        sensor, the item is `None`.
        """
        results = []
        for i in range(self._sensor_count):
            ret = self.read(i)
            if ret == None:
                ret = self._try_read(i)
            results.append(ret)
        return results

