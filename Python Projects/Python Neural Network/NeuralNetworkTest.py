from NeuralNetwork import NeuralNetwork
import numpy as np
import pandas as pd
import csv

#Extracting the dataset
#dataset with shifted height and weight along with avaerage height and weight
df = pd.read_csv("Python Projects\Python Neural Network\TrainingSet.csv")
# Define dataset
avg_height = df["Avg height"].dropna().iloc[0]
avg_weight = df["Avg weight"].dropna().iloc[0]

# Shifted height and weight
data = df[["Shifted Height", "Shifted Weight"]].to_numpy()
#Extracting the value of the data
all_y_trues=df["Sex.1"].to_numpy()

# Train  neural network!
network = NeuralNetwork()
print("Training the neural network...")
network.train(data, all_y_trues)

# Make some predictions

exit=False

while not exit:
    print("Enter the height and weight of the person you want to predict")
    
    height=float(input("Enter the height in cm: "))
    weight=float(input("Enter the weight in kg: "))
    
    person=np.array([(height-avg_height), (weight-avg_weight)])  # Shifting the input
    prediction = network.feedforward(person)
    
    print(f"Prediction: {prediction:.3f}")
    if prediction > 0.5:
        print("The person is likely a guy")
    elif prediction < 0.5:
        print("The person is likely a girl")
    
    exit_input = input("Do you want to exit? (yes/no): ").strip().lower()
    if exit_input == "yes":
        exit = True
    
        
    
