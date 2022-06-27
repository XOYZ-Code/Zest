import numpy as np
from modules.valhalla.valhalla_network import Valhalla_Network

x = np.array(
    [
        # [0.75, 0.25, 0.25, 0.75],
        # [0.75, 0.25, 0.25, 0],
        # [0.75, 0, 0.25, 1],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 0.5, 0, 0],
        [0, 0.25, 0, 0],
        [0, 1, 0, 1],
    ]
)

y = np.array(
    [
        # [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        # [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        # [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        # [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
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
    [1, 0, 0, 0.2]
))

for pixel in range(len(y[0])):
    gray = int(valhalla.output[pixel] * 255)
    img.putpixel(
        (pixel % 4, pixel // img.width),
        (gray, gray, gray)
    )
    print(gray, end=' - ')
    if pixel % 4 == 3:
        print()

img.show()
