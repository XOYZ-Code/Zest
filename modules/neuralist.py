# Neuralist Libary written by XOYZ-Code
# Copyright goes to XOYZ
# This is NOT an open-source libary
# Please check your license before using this class

import numpy
from tqdm import tqdm
from .style import Style
from .system import File, System
from PIL import Image
import os

numpy.seterr('ignore')


class NeuralistLayer:
    weight_min = 0.0
    weight_max = 0.0
    weight_approx = 0.0
    weight_count = 0
    weight_sum = 0
    neurons_count = 0
    neurons_input_count = 0
    layer_id = ''
    layer_name = ''
    style = Style()
    pref_width = 70

    def __init__(self, neuron_amount, neuron_input_amount, low_cpu=False, lay_name='NeuralistLayer'):
        self.layer_id = self.style.create_id(10)
        self.layer_name = lay_name
        self.weights = 2 * numpy.random.random((neuron_input_amount, neuron_amount)) - 1
        self.low_cpu = low_cpu
        if not low_cpu:
            self.adv_detail(neuron_amount, neuron_input_amount)

    def adv_detail(self, neurons, neurons_inputs):
        for i in tqdm(range(len(self.weights)), leave=True, unit='weights',
                      desc=self.style.align_horizontal(self.layer_name, self.layer_id, length=30)):
            for j in self.weights[i]:
                self.weight_count += 1
                self.weight_sum += j
                if j < self.weight_min:
                    self.weight_min = j
                if j > self.weight_max:
                    self.weight_max = j

        self.weight_approx = self.weight_sum / self.weight_count
        self.neurons_count = neurons
        self.neurons_input_count = neurons_inputs

    def summary(self):
        summary = [
            '',
            self.style.align_center('Summary', self.pref_width, space_char='-'),
            self.style.align_horizontal('Layer name', str(self.layer_name), self.pref_width, space_char='.'),
            self.style.align_horizontal('Layer id', str(self.layer_id), self.pref_width, space_char='.'),
            self.style.align_horizontal('Weight min', str(self.weight_min), self.pref_width, space_char='.'),
            self.style.align_horizontal('Weight max', str(self.weight_max), self.pref_width, space_char='.'),
            self.style.align_horizontal('Weight sum', str(self.weight_sum), self.pref_width, space_char='.'),
            self.style.align_horizontal('Weight approx', str(self.weight_approx), self.pref_width, space_char='.'),
            self.style.align_horizontal('Weight count', str(self.weight_count), self.pref_width, space_char='.'),
            self.style.align_horizontal('Neuron count', str(self.neurons_count), self.pref_width, space_char='.'),
            self.style.align_horizontal('Neuron input count', str(self.neurons_input_count),
                                        self.pref_width, space_char='.'),
            ''
        ]
        for i in summary:
            print(i)

    def save_json_summary(self, file_obj, path):
        json_summary = {
            'Layer name': self.layer_name,
            'Layer id': self.layer_id,
            'Weight min': self.weight_min,
            'Weight max': self.weight_max,
            'Weight approx': self.weight_approx,
            'Weight count': self.weight_count,
            'Neuron count': self.neurons_count,
            'Neuron input count': self.neurons_input_count
        }
        file_obj.save_json(path + '/NeuraLayers/Neuralayer_' + self.layer_name.replace(' ', '-') +
                           '_' + self.layer_id + '.neuralayer', json_summary)

    # load_json_summary work in progress
    def load_json_summary(self, file_obj, path):
        json_summary = file_obj.read_json(path)
        self.layer_name = json_summary['Layer name']
        self.layer_id = json_summary['Layer id']
        self.weight_min = json_summary['Weight min']
        self.weight_max = json_summary['Weight max']
        self.weight_approx = json_summary['Weight approx']
        self.weight_count = json_summary['Weight count']
        self.neurons_count = json_summary['Neuron count']
        self.neurons_input_count = json_summary['Neuron input count']
        self.style.paint('Finished loading summary of ' + self.layer_name, 'Information')


class NeuralistStacks:
    NeuralistInputLayer = None
    NeuralistHiddenLayers = None
    NeuralistOutputLayer = None

    def __init__(self, scale_matrix, low_cpu=False, neurastyle=None):
        self.NeuralistInputLayer = NeuralistLayer(scale_matrix[0][0], scale_matrix[0][1], low_cpu,
                                                  lay_name='Input Layer')
        self.NeuralistHiddenLayers = [NeuralistLayer(scale_matrix[i][0], scale_matrix[i][1], low_cpu,
                                                     lay_name='Hidden Layer nr.' + str(neurastyle.fit_number(i, 3)))
                                      for i in range(1, len(scale_matrix) - 1)]
        self.NeuralistOutputLayer = NeuralistLayer(scale_matrix[len(scale_matrix) - 1][0],
                                                   scale_matrix[len(scale_matrix) - 1][1], low_cpu,
                                                   lay_name='Output Layer')


class NeuralistNetwork:
    NeuralistNetworkLayers = None
    low_cpu = False
    NeuralistProject = None
    NeuraFile = File()
    NeruaStyle = Style()
    square_size = 16
    reduce_iterations = 0

    def __init__(self, network_scaling, arguments=None, project_obj=None):
        self.NeuralistProject = project_obj
        self.NeuralistProject.initialize_project_build()
        for i in range(len(arguments)):
            if arguments[i] == '--low-cpu':
                self.low_cpu = True
                self.NeuralistProject.log('WARNING: Low CPU activated! No advanced details available!', print_log=True)
            if arguments[i] == '--minor-update':
                self.NeuralistProject.new_minor_update()
                self.NeuralistProject.new_build()
            if arguments[i] == '--major-update':
                self.NeuralistProject.new_minor_update()
                self.NeuralistProject.new_build()
            if arguments[i] == '--reduce-operations':
                self.reduce_iterations = int(arguments[i + 1])
        self.NeuralistNetworkLayers = NeuralistStacks(network_scaling, self.low_cpu, self.NeruaStyle)
        self.NeuralistProject.save_info()

    def get_training_data(self, target_image, output_path, training_data_name='test'):
        image_original = Image.open(target_image)
        image_original_px = image_original.load()
        image_smaller = image_original.resize((int(image_original.size[0] * 0.5), int(image_original.size[1] * 0.5)))
        image_smaller_px = image_smaller.load()

        data_name = training_data_name + '_' + self.NeuralistProject.project_version_str.replace(' ', '-')

        self.NeuralistNetworkLayers.NeuralistInputLayer.save_json_summary(self.NeuraFile, output_path + '/' +
                                                                          data_name)
        for i in range(len(self.NeuralistNetworkLayers.NeuralistHiddenLayers)):
            self.NeuralistNetworkLayers.NeuralistHiddenLayers[i].save_json_summary(self.NeuraFile, output_path + '/' +
                                                                                   data_name)
        self.NeuralistNetworkLayers.NeuralistOutputLayer.save_json_summary(self.NeuraFile, output_path + '/' +
                                                                           data_name)

        frame = 0
        # for loops to run through the entire image
        for x in tqdm(range(image_smaller.size[0] - self.square_size), leave=True, unit='iters'):
            for y in range(image_smaller.size[1] - self.square_size):
                frame += 1
                cache_list_inputs = {}
                cache_list_outputs = {}

                # get training data | input
                row = -1
                for square_x in range(x, x + self.square_size):
                    row += 1
                    column = -1
                    for square_y in range(y, y + self.square_size):
                        column += 1
                        row_inputs = [
                            image_smaller_px[square_x, square_y][0],
                            image_smaller_px[square_x, square_y][1],
                            image_smaller_px[square_x, square_y][2]
                        ]
                        cache_list_inputs[str(self.NeruaStyle.fit_number(row, 2)) + '|' +
                                          str(self.NeruaStyle.fit_number(column, 2))] \
                            = row_inputs

                # get training data | output
                row = -1
                for square_x in range(2 * x, (2 * x) + (2 * self.square_size)):
                    row += 1
                    column = -1
                    for square_y in range(2 * y, (2 * y) + (2 * self.square_size)):
                        column += 1
                        row_outputs = [
                            image_original_px[square_x, square_y][0],
                            image_original_px[square_x, square_y][1],
                            image_original_px[square_x, square_y][2]
                        ]
                        cache_list_outputs[str(self.NeruaStyle.fit_number(row, 2)) + '|' +
                                           str(self.NeruaStyle.fit_number(column, 2))] \
                            = row_outputs

                # save inputs to json file
                self.NeuraFile.save_json(output_path + '/' + data_name + '/' + data_name + '_input/' +
                                         training_data_name + '_' + str(self.NeruaStyle.fit_number(frame, 10)) +
                                         '.neuraljson', cache_list_inputs)

                # save inputs to json file
                self.NeuraFile.save_json(output_path + '/' + data_name + '/' + data_name + '_output/' +
                                         training_data_name + '_' + str(self.NeruaStyle.fit_number(frame, 10)) +
                                         '.neuraljson', cache_list_outputs)

    def save_weights(self):
        pass

    def train_network(self, training_set_path, training_set_name=None):
        if training_set_name is None:
            training_set_name = training_set_path.split('\\')[len(training_set_path.split('\\')) - 1]
            self.NeuralistProject.log('Got \'training_set_name\' from the \'training_set_path\' : ' + training_set_name,
                                      print_log=True)
        self.NeuralistProject.log('Training data set name: ' + training_set_name, print_log=True)
        count_of_training_input_files = os.listdir(training_set_path + '\\' + training_set_name + '_input')
        count_of_training_output_files = os.listdir(training_set_path + '\\' + training_set_name + '_output')
        self.NeuralistProject.log('Available Input Files: ' + str(len(count_of_training_input_files)), print_log=True)
        self.NeuralistProject.log('Available Output Files: ' + str(len(count_of_training_output_files)), print_log=True)

        training_process = tqdm(
            desc='Training Network',
            leave=True, unit='files',
            total=len(count_of_training_input_files) - self.reduce_iterations
        )
        if not self.low_cpu:
            print(self.NeuralistNetworkLayers.NeuralistOutputLayer.weights)

        for train_file in range(len(count_of_training_input_files) - self.reduce_iterations):
            # loading training data into the arrays
            training_input = []
            expected_output = []

            absolute_inputfile_path = training_set_path + '\\' + training_set_name + '_input\\' + \
                                      count_of_training_input_files[train_file]
            absolute_outputfile_path = training_set_path + '\\' + training_set_name + '_output\\' + \
                                       count_of_training_output_files[train_file]
            for i in self.NeuraFile.read_json(absolute_inputfile_path):
                training_input.append(self.NeuraFile.read_json(absolute_inputfile_path)[i][0] / 255)
                training_input.append(self.NeuraFile.read_json(absolute_inputfile_path)[i][1] / 255)
                training_input.append(self.NeuraFile.read_json(absolute_inputfile_path)[i][2] / 255)
            for i in self.NeuraFile.read_json(absolute_outputfile_path):
                expected_output.append(self.NeuraFile.read_json(absolute_outputfile_path)[i][0] / 255)
                expected_output.append(self.NeuraFile.read_json(absolute_outputfile_path)[i][1] / 255)
                expected_output.append(self.NeuraFile.read_json(absolute_outputfile_path)[i][2] / 255)

            training_input = numpy.array(training_input).reshape((len(training_input), 1))
            expected_output = numpy.array(expected_output).reshape((len(expected_output), 1)).T
            # Let the neural network think with the random weights and enhance every time
            layer_outputs = self.think(training_input)
            len_out = len(layer_outputs)
            layer_errors = None
            layer_deltas = None
            layer_adjustments = []

            # Calculate Error, Delta and adjustments of Output Layer
            layer_errors = expected_output - layer_outputs[len_out - 1]
            layer_deltas = layer_errors * self.__sigmoid_derivative(layer_outputs[len_out - 1])
            layer_adjustments.append(layer_outputs[len_out - 2].T.dot(layer_deltas))
            if not self.low_cpu:
                print(self.total2Dsum(layer_adjustments[0]))
            # Calculate Error, Delta and adjustments of Hidden Layers
            layer_errors = layer_deltas.dot(self.NeuralistNetworkLayers.NeuralistOutputLayer.weights.T)
            layer_deltas = layer_errors * self.__sigmoid_derivative(layer_outputs[len_out - 2])
            layer_adjustments.append(layer_outputs[len_out - 3].T.dot(layer_deltas))

            for i in range(len(self.NeuralistNetworkLayers.NeuralistHiddenLayers) - 1, 0, -1):
                layer_errors = layer_deltas.dot(self.NeuralistNetworkLayers.NeuralistHiddenLayers[i].weights.T)
                layer_deltas = layer_errors * self.__sigmoid_derivative(layer_outputs[i])
                layer_adjustments.append(layer_outputs[i - 1].T.dot(layer_deltas))
                if not self.low_cpu:
                    print(self.total2Dsum(layer_adjustments[len(layer_adjustments) - 1]))
            # Calculate Error, Delta and adjustments of Input Layer
            layer_errors = layer_deltas.dot(self.NeuralistNetworkLayers.NeuralistHiddenLayers[0].weights.T)
            layer_deltas = layer_errors * self.__sigmoid_derivative(layer_outputs[0])
            layer_adjustments.append(training_input.T.dot(layer_deltas))
            if not self.low_cpu:
                print(self.total2Dsum(layer_adjustments[len(layer_adjustments) - 1]))
            cachek = len(layer_adjustments)
            for k in range(len(layer_adjustments)):
                cachek -= 1
                if k == len(layer_adjustments) - 1:
                    self.NeuralistNetworkLayers.NeuralistInputLayer.weights += layer_adjustments[k]
                else:
                    if k == 0:
                        self.NeuralistNetworkLayers.NeuralistOutputLayer.weights += layer_adjustments[k]
                    else:
                        self.NeuralistNetworkLayers.NeuralistHiddenLayers[cachek - 1].weights += layer_adjustments[k]

            # update tqdm process
            training_process.set_description('Loss: ' + str(round(self.total2Dsum(layer_errors[0])['approx'], 4)))
            training_process.update(1)
        training_process.close()
        print(self.NeuralistNetworkLayers.NeuralistOutputLayer.weights)

    def think(self, inputs):
        return_outputs = [self.__sigmoid(numpy.dot(inputs, self.NeuralistNetworkLayers.NeuralistInputLayer.weights))]
        for i in range(len(self.NeuralistNetworkLayers.NeuralistHiddenLayers)):
            return_outputs.append(
                self.__sigmoid(
                    numpy.dot(return_outputs[i], self.NeuralistNetworkLayers.NeuralistHiddenLayers[i].weights)))
        return_outputs.append(numpy.dot(return_outputs[len(return_outputs) - 1],
                                        self.NeuralistNetworkLayers.NeuralistOutputLayer.weights))

        # return_outputs = numpy.array(return_outputs)

        return return_outputs

    def __sigmoid(self, x):
        return 1 / (1 + numpy.exp(-x))

    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    def total2Dsum(self, matrix, json=True):
        if not json:
            return [matrix.sum(), matrix.sum() / matrix.size, matrix.max(), matrix.min()]
        else:
            r = {
                'sum': matrix.sum(),
                'approx': matrix.sum() / matrix.size,
                'max': matrix.max(),
                'min': matrix.min()
            }
            return r
