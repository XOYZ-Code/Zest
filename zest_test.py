import numpy as np
from modules.Zest import Zest
import time

start_time = time.time()

def runtime(x = ''):
    t = round((time.time() - start_time) * 1000)
    print(t, 'ms |', x)


in_x = np.array(
        [
            [1, 0.5]
        ]
    )

out_y = np.array(
        [
            [1, 0, 0, 0]
        ]
    )

zest = Zest(in_x, out_y)
runtime('Training begin')
for i in range(10000):
    zest.feed_forward()
    zest.backprop()



runtime('Finished')
