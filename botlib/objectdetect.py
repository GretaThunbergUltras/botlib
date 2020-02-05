import cv2 as cv

class ObjectDetector(object):
    def __init__(self, bot):
        self._bot = bot
        self._classifier = {}

    def _load_classifier(self, cascade: str):
        self._classifier[cascade] = cv.CascadeClassifier(cascade)

    def detect(self, cascade: str):
        """
        Try to detect objects in the current `Camera` frame.

        :param cascade: name of the model to use for detection.
        """
        if cascade not in self._classifier:
            self._load_classifier(cascade)
        classifier = self._classifier[cascade]

        ret, frame = self._bot.camera().get_capture().read()
        if ret:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            objects = classifier.detectMultiScale(gray, 1.1, 3)
            return objects
        else:
            print('frame is invalid')
