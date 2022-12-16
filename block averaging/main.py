from scipy.misc import face
import matplotlib.pyplot as plt
import numpy as np


def average(arr, w_blocks, h_blocks):
    new_shape = w_blocks, h_blocks  # новый размер картинки
    new_arr = np.zeros(new_shape)  # новая картинка в виде массива
    block_size_y = arr.shape[0] // w_blocks  # размер блока
    block_size_x = arr.shape[1] // h_blocks  # размер блока
    for y in range(w_blocks):  # перебор пикселей по новой высоте изображения
        if y == w_blocks - 1:  # если пиксель крайний
            end_y = arr.shape[0]  # записываем старый размер 768
        else:
            end_y = block_size_y * (y + 1)  # размер блока * пиксель+1
        for x in range(h_blocks):  # перебор пикселей по новой ширине изображения
            if x == h_blocks - 1:  # если пиксель крайний
                end_x = arr.shape[1]  # записываем старый размер 1024
            else:
                end_x = block_size_x * (x + 1)  # размер блока * номер пикселя+1
            new_arr[y, x] = np.mean(arr[y * block_size_y:end_y, x * block_size_x:end_x])
            print(y * block_size_y, end_y)
            # берем среднее значение пикселей в квадратике и записываем его как новый пиксель

    return new_arr


face = face(gray=True)
image = np.copy(face)
width = image.shape[0]  # размеры картинки
height = image.shape[1]
plt.subplot(121)
plt.imshow(face)
plt.subplot(122)
plt.imshow(average(image, width // 10, height // 10))
plt.show()
