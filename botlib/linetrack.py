import numpy as np
import math
import cv2 as cv

from threading import Thread

from .utils import PIDController

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

class LineTracker:
    def __init__(self, bot):
        """
        A class that delivers values correcting the bots steer direction.
        """
        self._bot = bot
        self._pid_controller = PIDController()

        self._track_process = None
        self._track_active = False

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
        return self._pid_controller.correct(next_value) if next_value != None else None

    def _setup_autopilot(self):
        from time import sleep

        def follow():
            try:
                while not self._track_active:
                    sleep(0.2)

                for improve in self:
                    # trace('linetracking')
                    if improve != None:
                        self._bot.drive_steer(improve)

                    while not self._track_active:
                        sleep(0.2)
            except KeyboardInterrupt:
                pass
            finally:
                self._bot.stop_all()

        self._track_process = Thread(group=None, target=follow, daemon=True)
        self._track_process.start()

    def autopilot(self, active: bool):
        """
        Spawns a new thread and adjusts the steer position automatically.

        :param active: a bool that enables/disables automatic steering.
        """
        self._track_active = active

        if self._track_process == None:
            self._setup_autopilot()

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
