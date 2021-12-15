# -*- coding: utf-8 -*-
import math

import cv2

import numpy as np

if __name__ == '__main__':
    def nothing(*arg):
        pass


    cv2.namedWindow("out_window")
    cap = cv2.VideoCapture(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    color_blue = (255, 0, 0)
    color_red = (0, 0, 128)
    while True:
        flag, img = cap.read()

        height, width = img.shape[:2]
        edge = 10
        hsv_min = np.array((0, 66, 123), np.uint8)
        hsv_max = np.array((17, 116, 194), np.uint8)

        low = np.array((0, 74, 80), np.uint8)
        high = np.array((52, 144, 255), np.uint8)
        try:
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(img_hsv, hsv_min, hsv_max)
            mask = cv2.inRange(img_hsv, low, high)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                center = (int(rect[0][0]), int(rect[0][1]))
                center1 = (int(rect[0][0]) +100, int(rect[0][1]) + 200) #нижний правый(по х, по у)
                center2 = (int(rect[0][0]) + 100, int(rect[0][1]) - 100)#верхний правый
                center3 = (int(rect[0][0]) - 100, int(rect[0][1]) + 200)#нижний левый
                center4 = (int(rect[0][0]) - 100, int(rect[0][1]) - 100) #верхний левый
                area = int(rect[1][0] * rect[1][1])

                if area > 7000:
                    cv2.line(img, center1, center2, color_blue, thickness=2, lineType=8, shift=0)
                    cv2.line(img, center2, center4, color_blue, thickness=2, lineType=8, shift=0)
                    cv2.line(img, center4, center3, color_blue, thickness=2, lineType=8, shift=0)
                    cv2.line(img, center3, center1, color_blue, thickness=2, lineType=8, shift=0)

                    # cv2.line(img, center3, center4, color_blue, thickness=2, lineType=8, shift=0)
                    # cv2.line(img, center1, center4, color_blue, thickness=2, lineType=8, shift=0)

                    break

            # cv2.imshow("thresh", thresh)
            cv2.imshow("out_window", img)
            cv2.imshow("mask", mask)
        except:
            cap.release()
            raise

        ch = cv2.waitKey(50)
        # для выхода надо нажать esc
        if ch == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
