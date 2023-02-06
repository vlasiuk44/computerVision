import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)
cam.set(cv2.CAP_PROP_EXPOSURE, -4)

eye = cv2.CascadeClassifier("haarcascade_eye.xml")
glasses = cv2.imread("dealwithit.png")


def detector(img, classifier, scale=None, min_nbs=None):
    result = img.copy()
    rects = classifier.detectMultiScale(result, scaleFactor=scale, minNeighbors=min_nbs)

    for (x, y, w, h) in rects:
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 255, 255))

    if len(rects) == 2:
        cx1 = rects[0][0]
        cy1 = rects[0][1]
        cx2 = rects[1][0]
        cy2 = rects[1][1]
        if cx2 > cx1:
            cx2 += rects[1][2]
        else:
            cx1 += rects[1][2]
        if cy2 > cy1:
            cy2 += rects[1][3]
        else:
            cy1 += rects[1][3]
        if cx1 > cx2:
            cx1, cx2 = cx2, cx1
            cy1, cy2 = cy2, cy1

        range_x = cx2 - cx1
        range_y = max(cy1, cy2) - min(cy1, cy2)

        dealwithit = cv2.imread("dealwithit.png", -1)
        dealwithit = cv2.resize(dealwithit, (range_x, range_y))

        y1, y2 = cy1, cy1 + dealwithit.shape[0]
        x1, x2 = cx1, cx1 + dealwithit.shape[1]

        alpha_s = dealwithit[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            try:
                result[y1:y2, x1:x2, c] = \
                    (alpha_s * dealwithit[:, :, c] + alpha_l * result[y1:y2, x1:x2, c])
            except:
                pass
    return result


while cam.isOpened():
    ret, frame = cam.read()
    key = cv2.waitKey(1)

    result = detector(frame, eye, 1.2, 5)
    if key == ord('q'):
        break

    cv2.imshow("Camera", result)

cam.release()
cv2.destroyAllWindows()
