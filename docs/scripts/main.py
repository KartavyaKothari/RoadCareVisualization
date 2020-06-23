import numpy as np
from . import nn
import csv
import pickle

def taskXor():
	""" Create a NeuralNetwork object with optimal parameters.

		1. epoch - number of iterations
		2. LR - Learning rate for the training
		3. Batch size for training   
	"""
	XTrain, YTrain, XVal, YVal, XTest, YTest = loadXor()
	# nn1 = nn.NeuralNetwork(lr, batchSize, epochs)
	nn1 = nn.NeuralNetwork(0.01, 100, 500)
	# Add layers to neural network corresponding to inputs and outputs of given data
	# Eg. nn1.addLayer(FullyConnectedLayer(x,y))
	nn1.addLayer(nn.FullyConnectedLayer(2,4,'relu'))
	nn1.addLayer(nn.FullyConnectedLayer(4,2,'relu'))
	#nn1.addLayer(nn.FullyConnectedLayer(2,4,'relu'))	
	
	nn1.addLayer(nn.FullyConnectedLayer(2,2,'softmax'))
	###############################################
	# TASK 3a (Marks 7) - YOUR CODE HERE
	# raise NotImplementedError
	###############################################
	# print("Ytrain &&&",YTrain)
	# exit()
	
	nn1.train(XTrain, YTrain, XVal, YVal)
	# pred, acc = nn1.validate(XTest, YTest)
	pred, acc = nn1.validate(XTrain, YTrain)
	with open("predictionsXor.csv", 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["id", "prediction"])
		for i, p in enumerate(pred):
			writer.writerow([i, p])
	print('Test Accuracy',acc)
	return nn1

def preprocessMnist(X):
	# Perform any data preprocessing that you wish to do here
	"""
	:param Input: A 2-d numpy array containing an entire train, val or test split | ``Shape: n x 28*28``
	:rtype: A 2-d numpy array of the same shape as the input (If the size is changed, you will get downstream errors)

	|

	"""
	###############################################
	# TASK 3c (Marks 0) - YOUR CODE HERE
	# raise NotImplementedError
	# print(X)
	# exit()
	
	X = np.where(X==0,1e-300,X)

	return X/256
	###############################################


def taskMnist():

	"""
	1. Create a NeuralNetwork object with optimal parameters.
		
		>>> nn1 = nn.NeuralNetwork(lr, batchSize, epochs)
	2. Add layers to neural network corresponding to inputs and outputs of given data
		
		>>> nn1.addLayer(FullyConnectedLayer(x,y))
	
	``nn1 = nn.NeuralNetwork(0.025, 13, 50)``
	``nn1.addLayer(nn.FullyConnectedLayer(784,30,'relu'))``
	|

	"""
	###############################################
	# TASK 3b (Marks 13) - YOUR CODE HERE

	XTrain, YTrain, XVal, YVal, XTest, _ = loadMnist()

	# nn1 = nn.NeuralNetwork(0.025, 13, 50)
	# nn1.addLayer(nn.FullyConnectedLayer(784,30,'relu'))
	# # nn1.addLayer(nn.FullyConnectedLayer(10,10,'relu'))
	# nn1.addLayer(nn.FullyConnectedLayer(30,10,'softmax'))

	nn1 = nn.NeuralNetwork(0.033, 13, 50)
	nn1.addLayer(nn.FullyConnectedLayer(784,25,'relu'))
	# nn1.addLayer(nn.FullyConnectedLayer(10,10,'relu'))
	nn1.addLayer(nn.FullyConnectedLayer(25,10,'softmax'))
	# raise NotImplementedError
	###############################################
	nn1.train(XTrain, YTrain, XVal, YVal)
	pred, _ = nn1.validate(XTest, None)
	with open("predictionsMnist.csv", 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["id", "prediction"])
		for i, p in enumerate(pred):
			writer.writerow([i, p])
	return nn1

################################# UTILITY FUNCTIONS ############################################
def oneHotEncodeY(Y, nb_classes):
	"""	
	Calculates one-hot encoding for a given list of labels
	:param Input:- Y : An integer or a list of labels 	
	:rtype: Output:- Coreesponding one hot encoded vector or the list of one-hot encoded vectors
	
	|

	"""
	temp =  (np.eye(nb_classes)[Y]).astype(int)
	return temp
	# print(temp)
	# exit()

def loadXor():
	"""
	* This is a toy dataset with 10k points and 2 labels.
	* The output can represented as the XOR of the input as described in the problem statement
	* There are 7k training points, 1k validation points and 2k test points
	
	|

	"""
	train = pickle.load(open("data/xor/train.pkl", 'rb'))
	test = pickle.load(open("data/xor/test.pkl", 'rb'))
	# print(train[1])
	# exit()

	testX, testY = np.array(test[0]), np.array(oneHotEncodeY(test[1],2))
	trainX, trainY = np.array(train[0][:7000]), np.array(oneHotEncodeY(train[1][:7000],2))
	valX, valY = np.array(train[0][7000:]), np.array(oneHotEncodeY(train[1][7000:],2))

	# print("^^^^^^",np.array(oneHotEncodeY(train[1][:7000],2)))
	# exit()

	return trainX, trainY, valX, valY, testX, testY

def loadMnist():
	"""
	* MNIST dataset has 50k train, 10k val, 10k test
	* The test labels have not been provided for this task
	
	|

	"""
	train = pickle.load(open("data/mnist/train.pkl", 'rb'))
	test = pickle.load(open("data/mnist/test.pkl", 'rb'))
	# print("&&&&&&&&&&&&&&&")
	# exit()
	testX = preprocessMnist(np.array(test[0]))
	# print(testX[])
	# exit()
	testY = None # For MNIST the test labels have not been provided
	# print(np.array(train[0][:5]))
	# print([np.array(train[0][:1])])
	# exit()
	
	trainX, trainY = preprocessMnist(np.array(train[0][:50000])), np.array(oneHotEncodeY(train[1][:50000],10))
	valX, valY = preprocessMnist(np.array(train[0][50000:])), np.array(oneHotEncodeY(train[1][50000:],10))
	# print([trainX[0]])
	# exit()
	return trainX, trainY, valX, valY, testX, testY
#################################################################################################

if __name__ == "__main__":
	np.random.seed(7)
	taskXor()
	# taskMnist()