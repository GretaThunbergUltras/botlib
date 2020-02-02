class Camera:
    BUFFER_SECONDS = 20

    def __init__(self, bot):
        import picamera

        self._bot = bot
        self._resolution_x, self._resolution_y = (800, 600)

        self._cam = picamera.PiCamera()
        self._buffer = picamera.PiCameraCircularIO(self._cam, seconds=Camera.BUFFER_SECONDS)
        self._running = False

        self._preview = None

    def __del__(self):
        self.stop()
        if self._running:
            self._buffer.__exit__()
            self._cam.__exit__()

    def _initialize(self):
        if not self._running:
            self._cam.__enter__()
            self._buffer.__enter__()
            self._running = True

    def resolution(self):
        return (self._resolution_x, self._resolution_y)

    def enable_preview(self):
        if not self._preview:
            self._preview = CameraPreview(self)

    def start(self):
        """
        Start recording to the intern buffer.
        """
        if not self._running:
            self._initialize()
        self._cam.start_recording(self._buffer, format='h264')

    def get_capture(self):
        """
        Read the last frame from the buffer.

        :returns: A copy of the last frame.
        """
        if not self._running:
            self._initialize()
        # TODO: this is probably crap
        buf = []
        return self._buffer.copy_to(buf, frames=1)

    def stop(self):
        """
        Stop recording to the buffer.
        """
        if self._cam.recording:
            self._cam.stop_recording()

# TODO: replace this by opencv preview
from tkinter import *
from PIL import Image, ImageTk

class CameraPreview:
    def __init__(self, cam):
        from threading import Thread

        self._cam = cam
        self._thread = Thread(group=None, target=self.create, daemon=True)
        self._thread.start()

    def create(self):
        from io import BytesIO

        self._root = Tk()
        self._root.wm_title('Camera Preview')
        self._root.geometry('200x120')
        self._window = CameraPreviewWindow(self._root)
        self._load = BytesIO()

        self.update()

        self._root.mainloop()

    def update(self):
        self._cam._cam.capture(self._load, format='jpeg', use_video_port=True)
        self._load.seek(0)

        self._window.set_image(self._load)
        self._root.after(1000, self.update)

class CameraPreviewWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        self._preview = Label(self)
        self._preview.place(x=0, y=0)

    def set_image(self, load):
        image = Image.open(load)
        self._preview.image = ImageTk.PhotoImage(image)
