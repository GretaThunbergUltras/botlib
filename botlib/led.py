from enum import Enum, unique
from time import sleep

from .motor import Motor
from .utils import Task

# TODO: add docs
# TODO: don't spawn a new thread on each `set_status`

@unique
class LEDStatus(Enum):
    BLINK = 1
    BLINK_FAST = 2
    FADE = 3

class LED(object):
    def __init__(self, bot):
        self._bot = bot
        self._bp = Motor._bp
        self._task = None

    def _blink(self):
        state = True
        while True:
            self._bp.set_led(100 if state else 0)
            state = not state
            sleep(0.5)

    def _blink_fast(self):
        state = True
        while True:
            self._bp.set_led(100 if state else 0)
            state = not state
            sleep(0.25)

    def _fade(self):
        from math import sin
        TDELTA = 0.02
        i, state = 0, 100
        while True:
            i += TDELTA
            self._bp.set_led(int(100 * sin(i)))
            sleep(TDELTA)

    def set_status(self, status):
        if isinstance(status, float) or isinstance(status, int):
            print('using numbers for setting led status is discouraged. use enum LEDStatus.')
            status = LEDStatus(status)

        if status == LEDStatus.BLINK:
            fn = self._blink
        elif status == LEDStatus.BLINK_FAST:
            fn = self._blink_fast
        elif status == LEDStatus.FADE:
            fn = self._fade
        else:
            raise ValueError('unknown LED status')

        self._task = Task(fn)
        self._task.start()
