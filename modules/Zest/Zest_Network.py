import numpy as np

class Zest_Network:
    
    def __init__(self, x, y) -> None:
        self.learning_rate = 0.0005
        self.extra_layers = 5
        self.input      = x
        self.weights    = [
            np.random.rand(self.input.shape[1], len(y)),
            np.random.rand(len(y), y.shape[1])
        ]
        for _ in range(self.extra_layers):
            self.weights.append(np.random.rand(y.shape[1], y.shape[1]))
        self.weights.append(np.random.rand(y.shape[1], len(y[0])))
        
        self.y          = y
        self.output     = np.zeros(self.y.shape)
    
    # Some Helper Functions
    def sigmoid(self, x):
        '''
        The basic sigmoid function
        '''
        sig = 1 / ( 1 + np.exp(-x / 500) )
        sig = np.minimum(sig, 0.99999)
        sig = np.maximum(sig, 0.00001)
        return sig
    
    def sigmoid_derivative(self, y):
        '''
        The derivative of sigmoid
        '''
        return y * ( 1.0 - y )
    
    # The real fun starts here

    def feed_forward(self, x_in = None):
        '''
        The basic training function of the nerual network.
        '''
        if x_in is None:
            x_in = self.input
        
        self.layers = []

        self.layers.append(self.sigmoid(np.dot(x_in, self.weights[0])))
        self.layers.append(self.sigmoid(np.dot(self.layers[0], self.weights[1])))

        for layer in range(self.extra_layers):
            self.layers.append(self.sigmoid(np.dot(self.layers[1 + layer], self.weights[2 + layer])))

        # self.layers.append(self.sigmoid(np.dot(self.layers[1], self.weights[2])))
        # self.layers.append(self.sigmoid(np.dot(self.layers[2], self.weights[3])))
        self.output = self.sigmoid(np.dot(self.layers[-1], self.weights[-1]))
    
    def backprop(self):
        '''
        Backoperation to find loss
        '''
        d_weights = [0.0 for _ in range(len(self.weights))]

        d_weights[-1] = np.dot(self.layers[-1].T, (2 * (self.y - self.output) * self.sigmoid_derivative(self.output)))

        d_weights[-2] = np.dot(self.layers[-2].T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[-1].T) * self.sigmoid_derivative(self.layers[-1])))

        # d_weights[2] = np.dot(self.layers[1].T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[3].T) * self.sigmoid_derivative(self.layers[2])))

        # d_weights[1] = np.dot(self.layers[0].T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[2].T) * self.sigmoid_derivative(self.layers[1])))

        for extra in range(self.extra_layers):
            d_weights[- (2 + (extra + 1))] = np.dot(self.layers[- (2 + (extra + 1))].T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[- (2 + extra)].T) * self.sigmoid_derivative(self.layers[- (2 + extra)])))

        d_weights[0] = np.dot(self.input.T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[1].T) * self.sigmoid_derivative(self.layers[0])))

        # Now update the weights
        for i in range(len(self.weights)):
            self.weights[i] += d_weights[i] * self.learning_rate
