from .camera import Camera
from .forklift import Forklift
from .motor import CalibratedMotor, Motor

class Bot:
    def __init__(self):
        self._drive_motor = Motor(Motor._bp.PORT_B)
        self._steer_motor = CalibratedMotor(Motor._bp.PORT_D, calpow=20)

        self._camera = Camera(self)
        self._forklift = Forklift(self)

    def drive_power(self, pnew):
        self._drive_motor.change_power(pnew)

    def drive_steer(self, pnew):
        pos = self._steer_motor.position_from_factor(pnew)
        self._steer_motor.change_position(pos)
    
    def calibrate(self):
        self._steer_motor.calibrate()
        self._forklift.calibrate()

    def stop_all(self):
        self._drive_motor.stop()
        self._steer_motor.stop()
        self._forklift.stop_all()
