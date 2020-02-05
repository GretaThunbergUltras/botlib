class PIDController:
    _x1 = 320.0
    _y1 = 480.0
    _x2 = 320.0
    _y2 = 380.0

    def __init__(self):
        """
        A PID controller
        """
        self._centerpoint = 85

        # PID constants
        self._kp = 1.8
        self._ki = 0.002
        self._kd = 0.6

        self._last_err = 0
        self._total_err = 0
        self._last_value = 0

    def correct(self, value:int) -> float:
        #TODO: test without abs
        #error = abs(value-self._centerpoint)
        error = value - self._centerpoint
        self._total_err += error

        proportional = error * self._kp
        integral = self._total_err * self._ki
        derivative = (error - self._last_err) * self._kd

        pidret = proportional + integral + derivative

        #set last_err and _total_err to 0 when value passes _centerpoint
        if (self._last_value > self._centerpoint and value < self._centerpoint) or (self._last_value<self._centerpoint and value>self._centerpoint):
            self._last_err = 0
            self._total_err = 0

        if error == 0:
            self._total_err = 0

        if self._total_err < -100:
            self._total_err = -100

        if self._total_err > 100:
            self._total_err = 100

        if pidret > 100:
            pidret = 100

        if pidret < -100:
            pidret = -100

        self._last_err = error
        self._last_value = value

        return pidret / 100
