import numpy as np
from Neuron import Neuron

INITIAL_WEIGHT=np.array([0.5, 0.5])  # Example initial weights

class NeuralNetwork:
    def __init__(self):
        self.weights= INITIAL_WEIGHT
        self.bias = 0.5
        
        
        #Hidden layer
        self.h1==Neuron(sel.weights,self.bias)
        self.h2 = Neuron(self.weights, self.bias)
        
        
        #Output layer
        self.o1 = Neuron(self.weights, self.bias)
        