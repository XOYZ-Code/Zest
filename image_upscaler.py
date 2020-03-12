from modules.project import *
from PIL import Image
import os


# algorythms.improve_1(style.paint(parameter_subject='Path to image', parameter_request_input=True))
# algorythms.upscale_1('data/img/yuki_and_kurumi.jpg', 'yuki_and_kurumi_2x.jpg')
# algorythms.upscale_1('data/img/yuki_and_kurumi_2x.jpg', 'yuki_and_kurumi_4x.jpg')
# algorythms.improve_1('data/img/yuki_and_kurumi_2x.jpg', 'data/img/yuki_and_kurumi_2x_improved.jpg')
# algorythms.improve_1('data/img/yuki_and_kurumi_4x.jpg', 'data/img/yuki_and_kurumi_4x_improved.jpg')

layers_number_of_neurons = [256, 256, 256, 512]
layers_numer_of_inputs = [3, 768, 768, 768]

NeuralLayers = NeuralLayerStacks(layers_number_of_neurons, layers_numer_of_inputs)

square_size = 16

NeuralNetwork = NeuralNetwork(NeuralLayers, project)
NeuralNetwork.train('data/img/yuki_and_kurumi.jpg', 1)

# print('-------------------------------------------')
# for i in range(len(NeuralLayers.NeuralStacks)):
#     for j in range(len(NeuralLayers.NeuralStacks[i].synaptic_weights)):
#         print('Layer nr.' + str(i) + ' Neuron nr.' + str(j))
#         print(NeuralLayers.NeuralStacks[i].synaptic_weights[j])
#     print('-------------------------------------------')


# def train():
#     for im_w in range(im_smaller.size[0] - square_size):
#         for im_h in range(im_smaller.size[1] - square_size):
#             cache_list = []
#             for square_w in range(im_w, im_w + square_size):
#                 for square_h in range(im_h, im_h + square_size):
#                     cache_list.append(im_smaller_px[square_w, square_h])
#             os.system('cls')
#             training_set_inputs.append(cache_list)
#             print(len(training_set_inputs))
#             print((im_smaller.size[0] - 16) * (im_smaller.size[1] - 16))
#     os.system('cls')
#
#     for ii in range(len(training_set_inputs)):
#         # print(len(training_set_inputs[ii]))
#         pass
#
#
# im = Image.open('data/img/yuki_and_kurumi.jpg')
# im_size = im.size
# scale = 0.02
# im_smaller = im.resize((int(im_size[0] * scale), int(im_size[1] * scale)))
# im_smaller_px = im_smaller.load()
# im_px = im.load()
