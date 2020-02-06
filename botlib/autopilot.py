from .utils import PIDController

from threading import Thread

import numpy as np
import math
import cv2

#import time
#traces = {}
#def trace(idx: str):
#    global traces
#    if idx not in traces:
#        traces[idx] = time.time()
#    else:
#        now = time.time()
#        print('delta {}: {}'.format(idx, now - traces[idx]))
#        traces[idx] = now

class Autopilot(object):
    """
    A class that delivers values correcting the bots steer direction.
    """
    def __init__(self, bot):
        self._bot = bot

        conf = self._bot.config().steer_pid()
        cp, p, i, d = conf['cp'], conf['p'], conf['i'], conf['d']
        self._pid = PIDController(cp, p, i, d)

        from .linetracking import LRTracker
        self._tracker = LRTracker(self._bot.camera())

        self._track_process = None
        self._track_active = False

    def _setup_autopilot(self):
        from time import sleep

        def follow():
            try:
                while not self._track_active:
                    sleep(0.2)

                for improve in self._tracker:
                    # trace('linetracking')
                    if improve != None:
                        improve = self._pid.correct(improve)
                        self._bot.drive_steer(improve)

                    while not self._track_active:
                        sleep(0.2)
            except KeyboardInterrupt:
                pass
            finally:
                self._bot.stop_all()

        self._track_process = Thread(group=None, target=follow, daemon=True)
        self._track_process.start()

    def is_active(self):
        """
        :return: a bool indicating the active state.
        """
        return self._track_active

    def active(self, active: bool):
        """
        Spawns a new thread and adjusts the steer position automatically.

        :param active: a bool that enables/disables automatic steering.
        """
        self._track_active = active

        if self._track_process == None:
            self._setup_autopilot()
