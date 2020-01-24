from .camera import Camera
from .forklift import Forklift
from .motor import Motor

class Bot:
    def __init__(self):
        self._drive_motor = Motor(Motor._bp.PORT_B)
        self._steer_motor = Motor(Motor._bp.PORT_D)

        self._camera = Camera(self)
        self._forklift = Forklift(self)
    
    def calibrate(self):
        self._drive_motor.calibrate()
        self._steer_motor.calibrate()
        self._forklift.calibrate()
