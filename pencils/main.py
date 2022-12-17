import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as scnd
from skimage.filters import threshold_triangle
from skimage.measure import label, regionprops


def to_bin(image, l_min, l_max):
    B = image.copy()
    B[B <= l_min] = 0
    B[B >= l_max] = 0
    B[B > 0] = 1
    return B


def attitude(region):
    return (region.perimeter ** 2) / region.area


def toGray(img):
    return (0.2989 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]).astype("uint8")


if __name__ == "__main__":
    pencils = 0
    for i in range(1, 13):
        img = plt.imread("images/img (" + str(i) + ").jpg")
        gray_img = toGray(img)  # переводим в градации серого
        # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plt.imshow(gray_img)
        plt.show()
        thr_img = threshold_triangle(gray_img)  # возвращает пороговое значение интенсивности
        # _, br = cv2.threshold(gray_img, thr_img, 255, 0)
        br = to_bin(gray_img, 0, thr_img)  # бинаризируем по этомум значению

        br = scnd.binary_dilation(br, iterations=1)  # dilation увеличивает размер объекта переднего плана.
        lab = label(br)  # помечаем объекты
        areas = []

        for r in regionprops(lab):
            areas.append(r.area)

        for r in regionprops(lab):
            if r.area < np.mean(areas):
                lab[lab == r.label] = 0  # если площадь объекта меньше средней, убираем его
            bbox = r.bbox
            # print(lab.shape[0])
            # print(lab.shape[1])
            if bbox[0] == 0 or bbox[1] == 0:  # если верхняя или левая координаты описывающей рамки= 0
                lab[lab == r.label] = 0  # убираем зашумленности по краям

        pencil = 0
        # 0 1 1 2 2 3 3 1 2 2 3 1
        for reg in regionprops(lab):
            if (((attitude(reg) > 105) and (300000 < reg.area < 450000))):
                pencil += 1
        pencils = pencils + pencil
        print(f" in img {i}: {pencil} pencils\n")
    print(f"in all images: {pencils}")
