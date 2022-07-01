import numpy as np
from PIL import Image
from modules.Zest.Zest_Network import Zest_Network
from modules.Zest.Zest_ImageProcessing import Zest_ImageProcessing
from tqdm import tqdm
import time
import json
import os

start_time = time.time()

def runtime(x = ''):
    t = round((time.time() - start_time) * 1000)
    print(t, 'ms |', x)

runtime('Prepare Data')

in_x = np.array(
        [
            [0, 1],
            [1, 0],
            [0, 0]
        ]
    )

out_y = np.array(
        [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 0]
        ]
    )

alternative = ['D:\\#Data\\shiro-small_0.1-Build-306\\','D:\\#Data\\Anime-Girl-Cute_0.1-Build-308\\']
# alternative = None

if alternative is not None:
    inputs_array = []
    outputs_array = []
    runtime('Starting loading alternative inputs...')
    for alter in alternative:
        runtime('Starting loading [' + alter + '] inputs')
        for file in os.listdir(alter + 'input'):
            with open(alter + 'input\\' + file, 'r', encoding='utf-8') as neuraljson:
                inputs_array.append([])
                cache = json.loads(neuraljson.read())

                for key in cache:
                    for value in cache[key]:
                        inputs_array[-1].append(value / 255)
                
        runtime('Finished loading [' + alter + '] inputs')

        # outputs
        runtime('Starting loading [' + alter + '] outputs')
        for file in os.listdir(alter + 'output'):
            with open(alter + 'output\\' + file, 'r', encoding='utf-8') as neuraljson:
                outputs_array.append([])
                cache = json.loads(neuraljson.read())

                for key in cache:
                    for value in cache[key]:
                        outputs_array[-1].append(value / 255)
                
        runtime('Finished loading [' + alter + '] outputs')
    in_x = np.array(inputs_array)
    out_y = np.array(outputs_array)

zest = Zest_ImageProcessing(in_x, out_y)

runtime('Training begin')

foldername = 'D:\\#Data\\' + 'shiro-' + str(round(time.time())) + '-output\\'

os.makedirs(foldername, exist_ok=True)

if alternative is not None:
    for i in tqdm(range(500), desc='Training', unit='iterations'):
        zest.feed_forward()
        zest.backprop()

        zest.process_image('C:\\Users\\kpage\\Pictures\\shiro_small.jpg').save(foldername + str(i) + '.jpg')
else:
    for i in range(500000):
        zest.feed_forward()
        zest.backprop()

        if i % 10000 == 0:
            zest.feed_forward([0, 1])
            print(i, zest.output)

runtime('Finished')
