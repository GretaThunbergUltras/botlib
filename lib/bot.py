import brickpi3

from .forklift import Forklift

class Bot:
    def __init__(self):
        self._DRIVE_MOTOR = bot._bp.PORT_B
        self._DRIVE_MOTOR_MIN = 0
        self._DRIVE_MOTOR_MAX = 0
        self._STEER_MOTOR = bot._bp.PORT_D
        self._STEER_MOTOR_MIN = 0
        self._STEER_MOTOR_MAX = 0

        self._bp = brickpi3.BrickPi3()
        self._forklift = Forklift(self)
    
    def calibrate(self):
        self._forklift.calibrate()
