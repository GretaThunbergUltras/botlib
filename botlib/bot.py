from .forklift import Forklift
from .motor import CalibratedMotor, Motor
import cv2

class Bot:
    """
    Control instance for a bot.
    """
    def __init__(self):
        self._drive_motor = Motor(Motor._bp.PORT_B)
        self._steer_motor = CalibratedMotor(Motor._bp.PORT_D, calpow=30)
        self._cap = None
        self._forklift = Forklift(self)

        with open('/etc/hostname', 'r') as hostname:
            self._name = hostname.read().strip()

    def name(self):
        """
        Returns the bot hostname.
        """
        return self._name

    def setup_broker(self, subscriptions=None):
        from .broker import Broker
        """
        Initialize a `Broker` connection.
        """
        self._broker = Broker(self, subscriptions)

    def detectObject(self, cascade: str):
        """
        Detect Objects
        """
        from .objectDetection import ObjectDetection
        detection = ObjectDetection(self)
        return detection.detect(cascade)

    def getCap(self) -> cv2.VideoCapture:
        if self._cap is None:
            self._cap = cv2.VideoCapture(-1)
        return self._cap

    def setup_camera(self):
        from .camera import Camera
        """
        Initialize a `Camera` object.
        """
        self._camera = Camera(self)

    def __del__(self):
        self._steer_motor.to_init_position()

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
        self._steer_motor.calibrate()
        self._forklift.calibrate()

    def stop_all(self):
        """
        Stop driving and steering motor as well as `Forklift`.
        """
        self._drive_motor.stop()
        self._steer_motor.stop()
        self._forklift.stop_all()
