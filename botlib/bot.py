from .config import ConfigSet
from .forklift import Forklift
from .log import Log
from .motor import CalibratedMotor, Motor
from .utils import Task

import cv2

class Bot(object):
    """
    Control instance for a bot.
    """
    def __init__(self):
        with open('/etc/hostname', 'r') as hostname:
            self._name = hostname.read().strip()

        self._config = ConfigSet
        self._log = Log()

        self._drive_motor = Motor(self, Motor._bp.PORT_B)
        self._steer_motor = CalibratedMotor(self, Motor._bp.PORT_D, calpow=30)

        # submodules of the bot. these will be created lazily by their
        # corresponding constructors e.g. `bot.forklift()`
        self._autopilot = None
        self._broker = None
        self._camera = None
        self._forklift = None
        self._objectdetector = None
        self._sonar = None

    def __del__(self):
        self._steer_motor.to_init_position()

    def name(self):
        """
        Returns the bot hostname.
        """
        return self._name

    def autopilot(self):
        """
        Initialize an `Autopilot` object.

        :return: A `Autopilot` instance.
        """
        if self._autopilot == None:
            from .autopilot import Autopilot
            self._autopilot = Autopilot(self)
        return self._autopilot

    def broker(self, subscriptions=None):
        """
        Initialize a `Broker` connection.

        :return: A `Broker` instance.
        """
        if self._broker == None:
            from .broker import Broker
            self._broker = Broker(self.name(), subscriptions)
        return self._broker

    def camera(self):
        """
        Initialize a `Camera` object.

        :return: A `Camera` instance.
        """
        if self._camera == None:
            from .camera import Camera
            self._camera = Camera(self)
        return self._camera

    def config(self):
        return self._config

    def forklift(self):
        """
        Initialize a `Forklift` object.

        :return: A `Forklift` instance.
        """
        if self._forklift == None:
            self._forklift = Forklift(self)
        return self._forklift

    def log(self):
        """
        :return: the current `Log` instance.
        """
        return self._log

    def objectdetector(self):
        """
        Initialize an `ObjectDetector` object.

        :return: An `ObjectDetector` instance.
        """
        if self._objectdetector == None:
            from .objectdetect import ObjectDetector
            self._objectdetector = ObjectDetector(self)
        return self._objectdetector

    def sonar(self):
        """
        Initialize a `Sonar` object.

        :return: A `Sonar` instance.
        """
        if self._sonar == None:
            from .sonar import Sonar
            self._sonar = Sonar(self)
        return self._sonar

    def drive_power(self, pnew):
        """
        Set the driving power

        :param pnew: a value between -100 and 100.
        """
        self._drive_motor.change_power(pnew)

    def drive_steer(self, pnew):
        """
        Set the steering position.

        :param pnew: a value between -1.0 and 1.0.
        """
        pos = self._steer_motor.position_from_factor(pnew)
        self._steer_motor.change_position(pos)

    def calibrate(self):
        """
        Find minimum and maximum position for motors.
        """
        steer_task = Task(self._steer_motor.calibrate)
        steer_task.start()

        self.forklift().calibrate()
        steer_task.join()

    def stop_all(self):
        """
        Stop driving and steering motor as well as `Forklift`.
        """
        self._drive_motor.stop()
        self._steer_motor.stop()
        self.forklift().stop_all()
