import numpy as np
import cv2

def nothing():
    pass

#Cascade für Wittenstein-Würfel
wuerfel_cascade = cv2.CascadeClassifier('cascade_wuerfel_logo_48_11.xml')

cap = cv2.VideoCapture(0)

#Trackbars für detectMultiScale parameter (scale_factor und min_neighbours)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("scale", "Trackbars", 11, 20, nothing)
cv2.createTrackbar("min", "Trackbars", 3, 6, nothing)
cv2.createTrackbar("Size", "Trackbars", 100, 200, nothing)

while 1:
    ret, img = cap.read()
    resize_val = cv2.getTrackbarPos("Size", "Trackbars")
    img = cv2.resize(img, (int(img.shape[1]*resize_val / 100), int(img.shape[0]*resize_val / 100)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    wuerfel = wuerfel_cascade.detectMultiScale(gray, cv2.getTrackbarPos("scale", "Trackbars") / 10, cv2.getTrackbarPos("min", "Trackbars"))

    for (x, y, w, h) in wuerfel:
        print("Wuerfel detected")
        print("X: {:d}, Y: {:d}, W: {:d}, H: {:d}".format(x, y, w, h))
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        break

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
