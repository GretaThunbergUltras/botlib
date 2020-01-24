import time

if __name__ == '__main__':
    print(dir(botlib))
    print(botlib.__file__)
    Motor._bp.set_motor_power(BP.PORT_B, 20)
    time.sleep(1)
    Motor._bp.set_motor_power(BP.PORT_B, 0)

