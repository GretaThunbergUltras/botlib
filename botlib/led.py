from enum import Enum, unique
from time import sleep

from .motor import Motor
from .utils import WorkerTask

# TODO: add docs

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

        self._state = None
        self._tickfn = None

    def _blink(self):
        if self._state is None:
            self._state = {'on': True}

        self._bp.set_led(100 if self._state['on'] else 0)
        self._state['on'] = not self._state['on']

    def _blink_fast(self):
        if self._state is None:
            self._state = {'on': True}

        self._bp.set_led(100 if self._state['on'] else 0)
        self._state['on'] = not self._state['on']

    def _fade(self):
        from math import sin
        TDELTA = 0.02

        if self._state is None:
            self._state = {'i': 0}
        
        self._state['i'] += TDELTA
        self._bp.set_led(int(100 * sin(self._state['i'])))

    def _tick(self, evt=None):
        if isinstance(evt, LEDStatus):
            if evt == LEDStatus.BLINK:
                self._tickfn = self._blink
            elif evt == LEDStatus.BLINK_FAST:
                self._tickfn = self._blink_fast
            elif evt == LEDStatus.FADE:
                self._tickfn = self._fade

            self._state = None

        if self._tickfn is None:
            return

        self._tickfn()

        sleep(0.1)

    def set_status(self, status):
        if self._task is None:
            self._task = WorkerTask(self._tick)
            self._task.start()

        if isinstance(status, float) or isinstance(status, int):
            print('using numbers for setting led status is discouraged. use enum LEDStatus.')
            status = LEDStatus(status)

        self._task.send_message(status)
