Implementation of a neural network from sratch

I followed the tutorial provided by: https://victorzhou.com/blog/intro-to-neural-networks/

1.Building Blocks: Neurons


Neuron takes input

multiplies the input by a weight 

then adds a bias


then the sum is passed through an activation function


We will use the sigmoid function


e.g 

We have a 2 input Neuron set to
w=[0,1]
b=4


suppose input is now x=[2,3]


when we pass it into  our model it becomes

0*2+1*3+4
=7


when we pass that into the function f(7) the article alledgely says we 


