# Idea for Neural Network Calculating:
# Take A Square of 16 by 16 Pixels and let it slide over the whole image
# The 16-Int RGB Tuple Array should be calculated

from numpy import exp, array, random, dot
from numpy.core.tests.test_mem_overlap import xrange
import numpy
from tqdm import tqdm
from PIL import Image
import os
from .system import File
from .style import Style


class NeuralLayer:
    def __init__(self, number_of_neurons, number_of_inputs):
        self.synaptic_weights = 2 * random.random((number_of_neurons, number_of_inputs)) - 1


class NeuralLayerStacks:
    NeuralStacks = []
    NeuralFile = File()

    def __init__(self, array_number_of_neurons, array_number_of_inputs):
        file = 'data/synaptic_weights/test_weights.nnw'
        weights = []
        for i in range(len(array_number_of_inputs)):
            self.NeuralStacks.append(NeuralLayer(array_number_of_neurons[i], array_number_of_inputs[i]))
            weights.append(self.NeuralStacks[i].synaptic_weights)
        self.NeuralFile.save_raw(file, str(weights))


class NeuralNetwork:
    square_size = 16
    NeuralFile = File()
    NeuralStyle = Style()

    def __init__(self, layers, project_obj):
        self.project_obj = project_obj

    def train(self, training_file, epochs):
        training_set_inputs = []
        training_set_outputs = []

        im = Image.open(training_file)
        im_size = im.size
        # im = im.resize((int(im_size[0] * 0.2), int(im_size[1] * 0.2)))
        im_size = im.size
        scale = 0.5
        im_smaller = im.resize((int(im_size[0] * scale), int(im_size[1] * scale)))
        im_smaller_px = im_smaller.load()
        im_px = im.load()

        analyze_progress = tqdm(total=((im_smaller.size[0] - self.square_size)
                                       * (im_smaller.size[1] - self.square_size)),
                                position=0, leave=True, unit=' Squares')

        try:
            os.makedirs('data/neural_network_data/training_data_' +
                        self.project_obj.project_version_str.replace(' ', '-'))
            os.makedirs('data/neural_network_data/training_data_' +
                        self.project_obj.project_version_str.replace(' ', '-') + '/training_data_' +
                        self.project_obj.project_version_str.replace(' ', '-') + '_input')
            os.makedirs('data/neural_network_data/training_data_' +
                        self.project_obj.project_version_str.replace(' ', '-') + '/training_data_' +
                        self.project_obj.project_version_str.replace(' ', '-') + '_output')
        except Exception:
            pass

        frame = 0

        for im_w in range(im_smaller.size[0] - self.square_size):
            for im_h in range(im_smaller.size[1] - self.square_size):
                frame += 1
                cache_list_inputs = []
                cache_list_outputs = []

                for square_w in range(im_w, im_w + self.square_size):
                    for square_h in range(im_h, im_h + self.square_size):
                        cache_list_inputs.append(im_smaller_px[square_w, square_h])
                # training_set_inputs.append(cache_list_inputs)
                self.NeuralFile.save('data/neural_network_data/' +
                                     'training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '/training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '_input' +
                                     '/training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '_frame_' + self.NeuralStyle.fit_number(frame, 10) + '.nntd', str(cache_list_inputs))

                for square_w in range(im_w * 2, im_w * 2 + self.square_size * 2):
                    for square_h in range(im_h * 2, im_h * 2 + self.square_size * 2):
                        cache_list_outputs.append(im_px[square_w, square_h])
                # training_set_outputs.append(cache_list_outputs)
                self.NeuralFile.save('data/neural_network_data/' +
                                     'training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '/training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '_output' +
                                     '/training_data_' + self.project_obj.project_version_str.replace(' ', '-') +
                                     '_frame_' + self.NeuralStyle.fit_number(frame, 10) + '.nntd', str(cache_list_outputs))
                # print(len(training_set_inputs))
                # print((im_smaller.size[0] - 16) * (im_smaller.size[1] - 16))
            analyze_progress.update((im_smaller.size[1] - self.square_size))
            analyze_progress.set_description('Getting training data...'.format(im_w))
        analyze_progress.close()
