import time
import mss
import numpy as np
import cv2
import pyautogui as pg

BOX_COORD = {'top': 610, 'left': 200, 'width': 250, 'height': 60}
BOX_COORD2 = {'top': 640, 'left': 100, 'width': 100, 'height': 30}
BOX_COORD3 = {'top': 640, 'left': 450, 'width': 100, 'height': 30}
BOX_COORD4 = {'top': 610, 'left': 450, 'width': 50, 'height': 30}
def make_scr():
    image = pg.screenshot(region=(0, 0, 1920, 1080))
    image = np.array(image)
    cv2.rectangle(image, (BOX_COORD['left'],BOX_COORD['top'] ),(BOX_COORD['left']+BOX_COORD['width'], BOX_COORD['top']+BOX_COORD['height']),(255, 0, 0), 2)
    cv2.rectangle(image, (BOX_COORD2['left'],BOX_COORD2['top'] ),(BOX_COORD2['left']+BOX_COORD2['width'], BOX_COORD2['top']+BOX_COORD2['height']),(0, 255, 0), 2)
    cv2.rectangle(image, (BOX_COORD3['left'],BOX_COORD3['top'] ),(BOX_COORD3['left']+BOX_COORD3['width'], BOX_COORD3['top']+BOX_COORD3['height']),(0, 0, 255), 2)
    cv2.rectangle(image, (BOX_COORD4['left'],BOX_COORD4['top'] ),(BOX_COORD4['left']+BOX_COORD4['width'], BOX_COORD4['top']+BOX_COORD4['height']),(255, 255, 0), 2)

    cv2.imwrite('pic2.png', image)

def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image


def screen_record():
    sct = mss.mss()
    last_time = time.time()

    while True:
        img = sct.grab(BOX_COORD)
        img2 = np.mean(process_image(np.array(sct.grab(BOX_COORD2))))
        img3 = np.mean(process_image(np.array(sct.grab(BOX_COORD3))))
        img4 = np.mean(process_image(np.array(sct.grab(BOX_COORD4))))

        img = np.array(img)
        processed_image = process_image(img)
        mean = np.mean(processed_image)

        if mean != float(0):
            pg.keyDown('up')
            time.sleep(0.050)
            pg.keyUp('up')
        if img2 == float(0):
            pg.keyDown('down')
            time.sleep(0.050)
            pg.keyUp('down')
        if img3 == float(0) and img4 != float(0):
            print(img3)


            pg.keyDown('down')
            time.sleep(0.4)
            pg.keyUp('down')


if __name__ == '__main__':
    make_scr()
    image = pg.screenshot(region=(0, 0, 1920, 1080))
    image = np.array(image)
    screen_record()
