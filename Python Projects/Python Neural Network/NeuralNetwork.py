import numpy as np
from Neuron import Neuron

INITIAL_WEIGHT=np.array([0.5, 0.5])  # Example initial weights

class NeuralNetwork:
    def __init__(self):
        self.weights= INITIAL_WEIGHT
        self.bias = 0.5
        
        
        #Hidden layer
        self.h1=Neuron(self.weights,self.bias)
        self.h2 = Neuron(self.weights, self.bias)
        
        
        #Output layer
        self.o1 = Neuron(self.weights, self.bias)
        
        
    def feedFoward(self, input):
        
        output_h1=self.h1.feedfoward(input)
        output_h2=self.h2.feedfoward(input)
        
        output_o1 = self.o1.feedfoward(np.array([output_h1, output_h2]))
        
        return output_o1
    
    
    
    
    
network=NeuralNetwork()
print(network.feedFoward(np.array([9, 2])))  # Example input
        
        