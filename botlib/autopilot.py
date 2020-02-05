import numpy as np
import math
import cv2

from .config import Config
from .utils import PIDController
from threading import Thread

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
    def __init__(self, bot):
        """
        A class that delivers values correcting the bots steer direction.
        """
        self._bot = bot

        # self._pid_config = Config(Config.STEER_PID_CONFIG)
        self._pid = PIDController(cp=85, p=1.8, i=0.002, d=0.6)

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

    def active(self, active: bool):
        """
        Spawns a new thread and adjusts the steer position automatically.

        :param active: a bool that enables/disables automatic steering.
        """
        self._track_active = active

        if self._track_process == None:
            self._setup_autopilot()
