from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import numpy as np


def make_alphabet(region):
    if np.all(region.image):
        return "-"

    count_lakes, count_bays = lakes_and_bays(region.image)

    if count_lakes == 2:
        if if_line(region):
            return "B"
        else:
            return "8"

    if count_lakes == 0:
        if if_line(region):
            return "1"
        if count_bays == 2:
            return "/"
        cut_cl, cut_cb = lakes_and_bays(region.image[2:-2, 2: -2])
        if cut_cb == 4:
            return "X"
        if cut_cb == 5:
            if check_center(region.image):
                return "*"
            return "W"

    if count_lakes == 1:
        if count_bays == 3:
            return "A"
        elif count_bays == 2:
            if check_center(region.image):
                return "P"
            return "D"
        else:
            return "0"
    return None


def lakes_and_bays(img):
    b = ~img
    lb = label(b)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == img.shape[0] - 1 or x == img.shape[1] - 1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1
    return count_lakes, count_bays


def if_line(region):
    lines = np.sum(region.image, 0) // region.image.shape[0]
    return 1 in lines


def check_center(img):
    cy = region.image.shape[0] // 2
    cx = region.image.shape[1] // 2
    if img[cy, cx] > 0:
        return True
    return False


if __name__ == "__main__":
    img = plt.imread("test.png")
    bin = np.sum(img, 2)
    bin[bin > 0] = 1

    labeled = label(bin)

    regions = regionprops(labeled)

    d = {None: 0}
    for region in regions:
        chr = make_alphabet(region)
        if chr is not None:
            labeled[np.where(labeled == region.label)] = 0
        if chr not in d:
            d[chr] = 0
        d[chr] += 1
    print("Alphabet: ", d)
    print("Percentage of character recognition: ", round(
        (1. - d[None] / sum(d.values())) * 100, 2))