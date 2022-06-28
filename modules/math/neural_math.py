import numpy as np

def sigmoid(x:float):
    '''
    The basic sigmoid function
    '''
    return 1 / ( 1 + np.exp(-x) )

def sigmoid_derivative(y:float):
    '''
    The derivative of sigmoid
    '''
    return y * ( 1.0 - y )
