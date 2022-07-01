import numpy as np

def sigmoid(x:float):
    '''
    The basic sigmoid function
    '''
    sig = 1 / ( 1 + np.exp(-x) )
    sig = np.minimum(sig, 0.99999)
    sig = np.maximum(sig, 0.00001)
    return sig

def sigmoid_derivative(y:float):
    '''
    The derivative of sigmoid
    '''
    return y * ( 1.0 - y )
