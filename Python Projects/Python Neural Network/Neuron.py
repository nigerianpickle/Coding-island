import numpy as np

def sigmoid(x):
    "Calculates the sigmoid activation funciton"
    return 1/(1+np.exp(-x))



class Neuron:
    def __init__(self,weights,bias):
        self.weights=weights
        self.bias=bias
        
        
    def feedfoward(self,inputs):
        #e.g inputs=[1,2]
        #weights=[0.5,0.5]
        #bias=0.5
        #total=np.dot(weights,inputs)+bias
        #total=(1*0.5 + 2*0.5) + 0.5 = 2.5
        total=np.dot(self.weights,inputs)+self.bias
        return sigmoid(total)
    
    
    def __str__(self):
        return f"Neuron(weights={self.weights}, bias={self.bias})"
    
        


