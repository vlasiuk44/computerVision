from platform import freedesktop_os_release
from scipy.misc import face
import matplotlib.pyplot as plt
import numpy as np


def average(arr, w_blocks, h_blocks):
    new_shape = w_blocks, h_blocks
    new_arr = np.zeros(new_shape)
    block_size_y = arr.shape[0] // w_blocks
    block_size_x = arr.shape[1] // h_blocks

    for y in range(w_blocks):
        if y == w_blocks - 1:
            end_y = arr.shape[0]
        else:
            end_y = block_size_y * (y + 1)
        for x in range(h_blocks):
            if x == h_blocks - 1:
                end_x = arr.shape[1]
            else:
                end_x = block_size_x * (x + 1)
            new_arr[y, x] = np.mean(arr[y * block_size_y:end_y,
                                        x * block_size_x:end_x])
    return new_arr


face = face(gray=True)
image = np.copy(face)
image.setflags(write=1)
width = image.shape[0]
height = image.shape[1]
plt.subplot(121)
plt.imshow(face)
plt.subplot(122)
plt.imshow(average(image, width // 10, height // 10))
plt.show()