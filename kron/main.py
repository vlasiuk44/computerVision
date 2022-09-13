import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


color1 = [255, 128, 0]
color2 = [0, 128, 255]

image = []
rng = 500
frame = 25
idx = rng // frame
buf = 1
for i in range(1, idx * idx + 1):
    if i % idx == 0:
        image.append(np.arange(buf, i + 1).tolist())
        buf = i + 1
image = np.array(image)
mask = np.ones((frame, frame))
result = np.kron(image, mask)
np.set_printoptions(edgeitems=26)

p = pd.DataFrame(result)
print(p)

plt.figure(1)
plt.imshow(p)

#преобразование массива в более четкий градиент по диагонали
# for i, v in enumerate(np.linspace(0, 1, p.shape[0])):
#     for j, v1 in enumerate(np.linspace(0, 1, p.shape[0])):
#         r = lerp(color1[0], color2[0], (v + v1) / 2)
#         g = lerp(color1[1], color2[1], (v + v1) / 2)
#         b = lerp(color1[2], color2[2], (v + v1) / 2)
#         p[i][j] = r
#
# plt.figure(2)
# plt.imshow(p)
# plt.show()
