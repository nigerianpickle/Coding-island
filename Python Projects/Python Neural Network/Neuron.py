import numpy as np

def sigmoid(x):
    "Calculates the sigmoid activation funciton"
    return 1/(1+np.exp(-x))



class Neuron:
    def __init(self,weights,bias):
        self.weights=weights
        self.bias=bias
        
        
    def feedfoward(self,inputs):
        total=np.dot(self.weights,inputs)+self.bias
        return sigmoid(total)
    
    
    def __str__(self):
        return f"Neuron(weights={self.weights}, bias={self.bias})"
    
        


