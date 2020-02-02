import cv2 as cv

class ObjectDetector:
    def __init__(self, bot):
        self._bot = bot
        self._classifier = {}

    def _load_classifier(self, cascade: str):
        self._classifier[cascade] = cv.CascadeClassifier(cascade)

    def detect(self, cascade: str):
        if cascade not in self._classifier:
            self._load_classifier(cascade)
        classifier = self._classifier[cascade]

        # cv.namedWindow("Trackbars")
        # cv.createTrackbar("min", "Trackbars", 3, 8, nothing)
        # cv.createTrackbar("scale", "Trackbars", 11, 22, nothing)
        # cv.createTrackbar("size", "Trackbars", 100, 200, nothing)
        # cv.createTrackbar("color", "Trackbars", 150, 255, nothing)
        # cap.set(3, 1280)
        # cap.set(4, 720)
        # cap.set(15, 0.1)

        ret, frame = self._bot.get_capture().read()
        if ret:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # gray = cv.resize(gray, (int(gray.shape[1] * cv.getTrackbarPos("size", "Trackbars") / 100),
            #                         int(gray.shape[0] * cv.getTrackbarPos("size", "Trackbars") / 100)))
            objects = classifier.detectMultiScale(gray, 1.1, 3)
            return objects
        else:
            print('frame is invalid')

    # def showImage(self, cascade: str):
    #     objects = self.detect(cascade)
    #     ret, frame = self._cap.read()
    #     if ret:
    #     for (x, y, w, h) in objects:
    #         cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    #         cv.putText(frame, str((x + w / 2) / frame.shape[1]), (x, y + 20), cv.FONT_HERSHEY_SIMPLEX, 1, 255)
    #         steer = round((x + w / 2) / frame.shape[1] * 150, 0)
    #         print(steer)
    #         controller = Controller(bot)
    #         controller.controll(steer)
    #
    #         cv.imshow("Object Detection", frame)
