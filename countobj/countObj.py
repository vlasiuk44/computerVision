import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage import morphology


def count_objects(image, mask):
    erosion = morphology.binary_erosion(image, mask)
    #Фильтр Эрозия уменьшает область изображения, приводя к истончению пикселей, расширяя и усиливая светлые места на изображении. 
    #Суть данного преобразования состоит в том, что нежелательные вкрапления и шумы размываются, а большие и, соответственно,
    #значимые участки изображения изменениям не подвергаются.
    dilation = morphology.binary_dilation(erosion, mask)
    #Фильтр Дилатация увеличивает область изображения, расширяя его пиксели и тем самым способствуя объединению областей изображения,
    #которые были разделены шумом и др.
    #Изображение после фильтра становится светлее и слегка размытым. То есть темные детали ослабляются или вообще исчезают,
    #что зависит от соотношения их размеров и яркостей с заданными параметрами фильтра.
    image -= dilation
    count = label(dilation).max()
    return count


image = np.load('ps.npy')

masks = np.array([
    np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ]),
    np.array([
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ])
], dtype=object)

all_objects = 0
i = 0
for mask in masks:
    val = count_objects(image, mask)
    all_objects += val
    i += 1
    print(f'Amount of objects type {i}:', val)
print('Amount of all objects:', all_objects)
