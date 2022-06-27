import numpy as np
from modules.valhalla.valhalla_network import Valhalla_Network

x = np.array(
    [
        [0.75, 0.25, 0.25, 0.75],
        [0.75, 0.25, 0.25, 0],
        [0.75, 0, 0.25, 1],
        [0, 1, 0, 0]
    ]
)

y = np.array(
    [
        [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
)

valhalla = Valhalla_Network(x, y)

for i in range(10000):
    valhalla.feed_forward()
    valhalla.backprop()

print(valhalla.weights)

print('-------------------------------------')

# import image
from PIL import Image

img = Image.new('RGB', (4, 4))

valhalla.feed_forward(np.array(
    [0, 0.5, 1, 0]
))

for i in range(y.shape[0]):
    print(i, valhalla.output[i])

    for pixel in range(len(y[i])):
        gray = int(valhalla.output[pixel] * 255)
        img.putpixel(
            (pixel % 4, pixel // img.width),
            (gray, gray, gray)
        )

img.show()
