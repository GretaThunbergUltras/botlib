import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(True):
    ret, image = cap.read()

    resized = image[300:640, 0:480]
    #resized = image
    dimensions_resized = resized.shape
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 20, 100, cv2.THRESH_BINARY_INV)

    dilated = cv2.dilate(thresh, None, iterations=3)
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    difference = -1

    for contour in contours:
        #print(contour)
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(resized, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    #cv2.line(resized, (280, 0), (280, 515), (255, 0, 0), 5)

    cv2.imshow("Resized", resized)
    cv2.imshow("Result", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
