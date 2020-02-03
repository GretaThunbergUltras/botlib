import cv2
import numpy as np

class LineTracking:
    def track_line(self):
        cap = cv2.VideoCapture(0)
        ret, image = cap.read()
        resized = image[300:640, 0:480]

        dimensions_resized = resized.shape
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 20, 100, cv2.THRESH_BINARY_INV)

        dilated = cv2.dilate(thresh, None, iterations=3)
        _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        difference = -1

        contours_last = contours[-1]
        contours_first = contours[0]
        len_contours = len(contours_first[:,0])

        highP = contours_first[int(len_contours/2)]
        lowP = contours_first[0]

        cv2.line(image, (highP[0][0], highP[0][1]+300), (lowP[0][0], lowP[0][1]+300), (0, 0, 255), 5)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #print("(X1|Y1): {}/{}; (X2|Y2):{}/{}".format(highP[0][0], highP[0][1]+300, lowP[0][0], lowP[0][1]+300))
        ##Return (x1, y1, x2, y2)

        return ((highP[0][0], highP[0][1]+300, lowP[0][0], lowP[0][1]+300), image)

if __name__ == '__main__':
    lt = LineTracking()
    coords, _ = lt.track_line()
    print(coords)
