from botlib import *

import time

if __name__ == '__main__':
    Motor._bp.set_motor_power(BP.PORT_B, 20)
    time.sleep(1)
    Motor._bp.set_motor_power(BP.PORT_B, 0)

