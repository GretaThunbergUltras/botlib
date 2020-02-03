import numpy as np
import math
import cv2 as cv

class LineTracker:
    def __init__(self, bot):
        """
        A class that delivers values correcting the bots steer direction.
        """
        self._bot = bot
        self._pid_controller = PIDController()

        # TODO: access `bot` camera here
        self.video_capture = cv.VideoCapture(0)
        self.video_capture.set(3, 160)
        self.video_capture.set(4, 120)

    def __iter__(self):
        """
        This enables iteration for `LineTracker`.
        """
        return self

    def __next__(self):
        """
        Determine the next control value. Automatically called inside `for` loops, but can
        be triggered manually using `next(line_tracker)`.
        """
        next_value = self.track_line()
        return self._pid_controller.correct(next_value)

    def track_line(self):
        """
        Algorithm that analyses the line in front of the bot.
        """
        # Capture the frames
        ret, frame = self.video_capture.read()

        # Crop the image
        # TODO: this depends on the resolution. adjust please
        crop_img = frame[60:120, 0:160]

        # Convert to grayscale
        gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv.GaussianBlur(gray, (5,5), 0)

        # Color thresholding
        ret,thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY_INV)

        # Find the contours of the frame
        contours, hierarchy = cv.findContours(thresh.copy(), 1, cv.CHAIN_APPROX_NONE)
        
	# Find the biggest contour (if detected)
        if len(contours) > 0:
            c = max(contours, key=cv.contourArea)
            M = cv.moments(c)

            # cy = int(M['m01']/M['m00'])

            # cv.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            # cv.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            # cv.drawContours(crop_img, contours, -1, (0,255,0), 1)

            # if cx >= 100:
                # print("Turn Right!")
            # if cx < 100 and cx > 70:
                # print("On Track!")
            # if cx <= 70:
                # print("Turn Left")
            # print(cx)

            # FIXME: we cannot divide by 0. is this intended?
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                return cx
        return None

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
            self._last_err = -1
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
