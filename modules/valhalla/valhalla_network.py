import numpy as np

class Valhalla_Network:
    
    def __init__(self, x, y) -> None:
        self.input      = x
        self.weights    = [
            np.random.rand(self.input.shape[1], len(y)),
            np.random.rand(len(y), len(y[0]))
        ]
        self.y          = y
        self.output     = np.zeros(self.y.shape)
    
    # Some Helper Functions
    def sigmoid(self, x):
        '''
        The basic sigmoid function
        '''
        return 1 / ( 1 + np.exp(-x) )
    
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

        self.layer1 = self.sigmoid(np.dot(x_in, self.weights[0]))
        self.output = self.sigmoid(np.dot(self.layer1, self.weights[1]))
    
    def backprop(self):
        '''
        Backoperation to find loss
        '''
        d_weights = [0.0 for _ in range(len(self.weights))]

        d_weights[1] = np.dot(self.layer1.T, (2 * (self.y - self.output) * self.sigmoid_derivative(self.output)))

        d_weights[0] = np.dot(self.input.T, (np.dot(2 * (self.y - self.output) * self.sigmoid_derivative(self.output), self.weights[1].T) * self.sigmoid_derivative(self.layer1)))

        # Now update the weights
        for i in range(len(self.weights)):
            self.weights[i] += d_weights[i]
