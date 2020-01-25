import picamera

class Camera:
    def __init__(self, bot):
        self._bot = bot

        self._cam = picamera.PiCamera()
        self._buffer = picamera.PiCameraCircularIO(self._cam, seconds=3)
        self._initialized = False

    def start(self):
        if not self._initialized:
            self._cam.__enter__()
            self._buffer.__enter__()
            self._initialized = True
        self._cam.start_recording(self._buffer)

    def stop(self):
        if self._cam.recording:
            self._cam.stop_recording()

    def __del__(self):
        self.stop()
        if self._initialized:
            self._buffer.__exit__()
            self._cam.__exit__()
