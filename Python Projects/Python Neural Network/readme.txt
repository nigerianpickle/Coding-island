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


when we pass that into the sigmoid function f(7) 



Training a neural network:

Say we have the measurements:
Name	Weight (lb)	Height (in)	Gender
Alice	   133	       65	      F
Bob	        160	       72	      M
Charlie	   152	        70	      M
Diana	   120	        60	      F


In order to make it easier for a computer to use we change the genders to 0 and 1
We also perform  shifting on the values using the average


Say we have the measurements:
Name	Weight (lb)	Height (in)	Gender
Alice	   133	       65	      F
Bob	        160	       72	      M
Charlie	   152	        70	      M
Diana	   120	        60	      F



Before we also train, we need to identify the loss:
We will use  mean squared error to identify the difference between what our prediction was and the actual value

the better our prediction, the lower our loss will be




After we get the loss, we have a goal. To minimize this loss