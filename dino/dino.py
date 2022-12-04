import time

import mss
import numpy as np
import cv2
import pyautogui as pg


BOX_COORD = {'top': 253 + 25, 'left': 200           , 'width': 50, 'height': 80 - 25}


def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image


def screen_record():
    sct = mss.mss()
    last_time = time.time()

    while True:
        img = sct.grab(BOX_COORD)
        img = np.array(img)
        processed_image = process_image(img)
        mean = np.mean(processed_image)
        if mean != float(0):
            pg.press('space')
        last_time = time.time()

if __name__ == '__main__':
    screen_record()