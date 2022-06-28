import numpy as np
from modules.math.neural_math import sigmoid, sigmoid_derivative

class Zest:

    def __init__(
        self,
        input_length        :int,
        output_length       :int,
        hidden_layer_count  :int    = 1,
        hidden_layer_size   :int    = None
        ) -> None:
        '''
        ``input_length``: Defines how many inputs the network wants. [0, 1, 1] = Length 3
        ``output_length``: Defines how many outputs the network produces. [0, 1, 1] = Length 3
        ``hidden_layer_count``: Defines how many hidden layers will be created. Minimum 1
        ``hidden_layer_size``: Defines how many Neurons should be in each Hidden Layer
        '''

        # Hidden-Layer count can't be lower than 1
        if hidden_layer_count < 1:
            hidden_layer_count = 1

        # Set hidden_layer_size to output_length if it is None
        if hidden_layer_size is None:
            hidden_layer_size = output_length

        # Create the weight Array. The '+ 2' makes place for the input and output layer weights
        self.weights = [None for _ in range(hidden_layer_count + 2)]

        # Create random arrays for the weights
        self.weights[0]  = np.random.rand(input_length, hidden_layer_size)

        for weight_index in range(1, len(self.weights) - 1):
            self.weights[weight_index] = np.random.rand(hidden_layer_size, hidden_layer_size)

        self.weights[-1] = np.random.rand(hidden_layer_size, output_length)

        pass
