import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.measure import regionprops, label


def find_rects_and_circles(circles, rects):
    for region in regions:
        fig_color = get_fig_color(region)
        if np.all(region.image):
            if fig_color in circles:
                circles[fig_color] += 1
            else:
                circles[fig_color] = 1
        else:
            if fig_color in rects:
                rects[fig_color] += 1
            else:
                rects[fig_color] = 1


def get_fig_color(region):
    center_row, center_col = map(int, region.centroid)
    fig_colors = hsv_image[center_row, center_col, 0] * 360

    if fig_colors < border_colors[0]:
        return 'red'
    elif fig_colors < border_colors[1]:
        return 'yellow'
    elif fig_colors < border_colors[2]:
        return 'green'
    elif fig_colors < border_colors[3]:
        return 'lightgreen'
    elif fig_colors < border_colors[4]:
        return 'blue'
    elif fig_colors < border_colors[5]:
        return 'purple'


def print_inventory(dct):
    for item, amount in dct.items():
        print("\t{}: {}".format(item, amount))


def get_colors(hsv_image):
    colors = []
    dist = 0
    start_index = 0

    unique_vals = np.unique(hsv_image[:, :, 0])
    epsilon = np.diff(unique_vals).mean()
    for i in range(1, unique_vals.shape[0]):
        d = abs(unique_vals[i] - unique_vals[i - 1])
        if abs(dist - d) > epsilon:
            dist = 0
            colors.append(unique_vals[start_index:i].mean() * 360)
            start_index = i
    colors.append(unique_vals[start_index:].mean() * 360)
    return colors


def get_border_colors(colors):
    border_colors = []
    for i in range(len(colors)):
        if i == len(colors) - 1:
            border_colors.append((colors[i] + 360.0) / 2)
        else:
            border_colors.append((colors[i] + colors[i + 1]) / 2)
    return border_colors


if __name__ == "__main__":
    image = plt.imread('balls_and_rects.png')
    hsv_image = color.rgb2hsv(image)
    binary = np.sum(image, 2)
    binary[binary > 0] = 1
    labeled = label(binary)
    regions = regionprops(labeled)
    colors = get_colors(hsv_image)[1:]
    border_colors = get_border_colors(colors)

    rects = {}
    circles = {}
    find_rects_and_circles(circles, rects)

    print("Total: ", labeled.max())
    print("Circles: ")
    print_inventory(circles)
    print("Rects: ")
    print_inventory(rects)
