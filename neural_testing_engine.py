from modules.neuralist import *
from modules.system import System, File
from modules.version_control import Project
import sys

# scale Network
# Index[i][0] is for Neuron amount
# Index[i][1] is for Neuron input amount
scale_network = [
    [768, 1],
    [768, 768],
    [768, 768],
    [768, 768],
    [768, 768],
    [768, 768],
    [768, 768],
    [768, 768],
    [3072, 768],
    [3072, 3072]
]

Neuralist = NeuralistNetwork(scale_network, sys.argv,
                             project_obj=Project('image_upscaler', 'XOYZ-Code [xoyz.productions@gmail.com]'))

for arg in range(len(sys.argv)):
    if sys.argv[arg] == '-summary':
        if sys.argv[arg + 1] == 'all':
            Neuralist.NeuralistNetworkLayers.NeuralistInputLayer.summary()
            for i in Neuralist.NeuralistNetworkLayers.NeuralistHiddenLayers:
                i.summary()
            Neuralist.NeuralistNetworkLayers.NeuralistOutputLayer.summary()
    if sys.argv[arg] == '--get-training-data':
        Neuralist.get_training_data(sys.argv[arg + 1], sys.argv[arg + 2], sys.argv[arg + 3])
    if sys.argv[arg] == '-train':
        Neuralist.train_network(sys.argv[arg + 1])
