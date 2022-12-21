import cv2
import numpy as np
import time
import math

cam = cv2.VideoCapture(0)
last_cX = None
last_cY = None
last_time = None


def circularity(area, perimeter):
    return 4 * math.pi * area / perimeter ** 2


def get_speed(cX, cY, last_cX, last_cY, time, last_time):
    delta_time = time - last_time + 0.0000001
    distance = ((cX - last_cX) ** 2 + (cY - last_cY) ** 2) ** (1 / 2)
    return distance / delta_time, delta_time


while cam.isOpened():
    ret, image = cam.read()
    lower = np.array([0, 50, 100])
    upper = np.array([21, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(contours) > 0:
        for c in contours:
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            if area > 5000 and circularity(area, perimeter) > 0.65:
                M = cv2.moments(c)  # момент и центроид
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

                    if last_cX is not None:
                        #cv2.circle(image, (last_cX, last_cY), 7, (255, 0, 255), -1)
                        out1, out2 = get_speed(cX, cY, last_cX, last_cY, time.time(), last_time)
                        cv2.putText(image, str(out1), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255),
                                    2)
                        print(int(out1 / out2), "px in second", int(out1 / out2))

                    last_cX = cX
                    last_cY = cY
                    last_time = time.time()

    cv2.imshow('speed', image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
