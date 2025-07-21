You can play around with my version by running NeuralNetworkTest.
I got the csv data from kaggle, found the average male and female heights and shifted the values in the dataset
based on that
this way i am able to use the data for the example



Technologies used:
Python,Excel,Pandas,Numpy



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

I will fill in the math details later, maybe when i want to specialize but i would be writing nonsense if iii went inot the details.
But the idea is basically we get a Loss when we feed our input in, and these
Losses grow exponentially, meaning we want to find values thhat reduce this loss


Treating the Loss as a function of weights, we basically try to find values that would give us a lower loss? I think



Training:

Stochastic Gradient Descent

An optimization algorithm that tells us how to change  weights and  baises to minimize loss





w1<- w1- n L/w1
N is a constant called thre learning rate.
This controls how fast we train






