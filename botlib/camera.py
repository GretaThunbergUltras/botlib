from vidgear.gears import PiGear

class Camera:
    def __init__(self, bot):
        self._bot = bot

        self._resolution = (800, 600)
        self._framerate = 24

        self._stream = PiGear(self._resolution, framerate=self._framerate)
        self._running = False

    def __del__(self):
        self.stop()

    def resolution(self):
        return self._resolution

    def start(self):
        """
        Start recording to the intern buffer.
        """
        if not self._running:
            self._stream.start()
            self._running = True

    def capture(self):
        """
        Read the last frame from the buffer.

        :returns: A copy of the last frame.
        """
        return self._stream.read()

    def stop(self):
        """
        Stop recording to the buffer.
        """
        self._stream.stop()
        self._running = False
