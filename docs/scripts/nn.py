import numpy as np

class NeuralNetwork:
	"""
	Neural network implementating class methods.
	
	>>> nn1 = nn.NeuralNetwork(0.01, 100, 500)
	
	>>> nn1.addLayer(FullyConnectedLayer(x,y))
	
	>>> nn1.addLayer(nn.FullyConnectedLayer(2,4,'relu'))

	Initializes a Neural Network Object
	
	:param: lr: learning rate
	:param: batchSize: Mini batch size
	:param: epochs: Number of epochs for training
	
	|

	"""

	def __init__(self, lr, batchSize, epochs):
		self.lr = lr
		self.batchSize = batchSize
		self.epochs = epochs
		self.layers = []
		self.i = 0

	def addLayer(self, layer):
		""" Method to add layers to the Neural Network 
		
		|

		"""
		self.layers.append(layer)

	def train(self, trainX, trainY, validX=None, validY=None):
		"""
		:param trainX: A list of training input data to the neural network
		:param trainY: Corresponding list of training data labels
		:param validX: A list of validation input data to the neural network
		:param validY: Corresponding list of validation data labels

		:rtype: Loss gradient
		
		We run the following training algorithm for epoch number of times

		1. Divide the data into batches
			``trainX[i*batchSize:i*batchSize+batchSize]``
		2. For each batch run the ``forwardpass()`` for the network
		3. Now calculate the loss and use the ``backpropogate()`` function
		4. Update weights

		|

		"""

		batchSize = self.batchSize # Get the batch size from self variables 

		superData = np.append(trainX,trainY,axis=1)
		tshape = trainX.shape[1]


		for epoch in range(self.epochs):
			self.i = epoch
			np.random.shuffle(superData)
			# print(superData[:5])
			trainX = superData[:,:tshape]
			# print(traiX[:5])
			trainY = superData[:,tshape:]
			# print(traiY[:5])
			# print(trainX.shape[0]//batchSize)
			# exit()
			for i in range(trainX.shape[0]//batchSize):
				
				dataX = trainX[i*batchSize:i*batchSize+batchSize]
				dataY = trainY[i*batchSize:i*batchSize+batchSize]
				# print(data.shape)
				# exit()
				# dataX = trainX
				# dataY = trainY

				# print(dataY)


				# print(self.layers)

				for layer in self.layers:
					dataX = layer.forwardpass(dataX)
					# print("######")
					# print([dataX[1]])
					# print("######")
				# print("######")
				# exit()
				# loss = self.crossEntropyLoss(dataY,dataX)
				lossGrad = self.crossEntropyDelta(dataY,dataX)
				# print(loss)

				for j in range(len(self.layers)-1,0,-1):
					lossGrad = self.layers[j].backwardpass(self.layers[j-1].data,lossGrad)
					self.layers[j].updateWeights(self.lr)

				dataX = trainX[i*batchSize:i*batchSize+batchSize]

				lossGrad = self.layers[0].backwardpass(dataX, lossGrad)
				self.layers[0].updateWeights(self.lr)
			# print(epoch,self.computeAccuracy(validY,self.predict(validX)))
		return lossGrad
		# raise NotImplementedError
		###############################################
		
	def crossEntropyLoss(self, Y, predictions):
		"""
		:param Y: Ground truth labels (encoded as 1-hot vectors) | ``shape = batchSize x number of output labels``
		:param predictions: Predictions of the model | ``shape = batchSize x number of output labels``
		
		:rtype: The cross-entropy loss between the predictions and the ground truth labels | ``shape = scalar``
		
		|

		"""
		###############################################
		# TASK 2a (Marks 3) - YOUR CODE HERE

		# print(Y)
		# print(predictions)
		# exit()

		# BEGIN

		# print([predictions[0]])

		temp = np.sum(np.multiply(Y,np.log(predictions+1e-300)))
		temp = temp * -1
		return temp
		# END

		# raise NotImplementedError
		###############################################

	def crossEntropyDelta(self, Y, predictions):
		# Input 
		"""
		:param Y: Ground truth labels (encoded as 1-hot vectors) | ``shape = batchSize x number of output labels``
		:param predictions: Predictions of the model | ``shape = batchSize x number of output labels``
		:rtype: Returns the derivative of the loss with respect to the last layer outputs, ie ``dL/dp_i`` where ``p_i`` is the ith output of the last layer of the network | ``shape = batchSize x number of output labels``
		
		|
		
		"""
		###############################################
		# TASK 2b (Marks 3) - YOUR CODE HERE
		
		# BEGIN
		# print("Iter ",self.i,"Predic ",predictions)

		temp = np.divide(Y,predictions+1e-300)
		# numer = np.where(numer==0,1e-300,numer)
		temp = temp * -1

		# print(temp)

		return temp
		# END

		# raise NotImplementedError
		###############################################
		
	def computeAccuracy(self, Y, predictions):
		"""
		:rtype: The accuracy given the true labels Y and final output of the model
		
		|

		"""
		correct = 0
		for i in range(len(Y)):
			if np.argmax(Y[i]) == np.argmax(predictions[i]):
				correct += 1
		accuracy = (float(correct) / len(Y)) * 100
		return accuracy

	def validate(self, validX, validY):
		# Input 
		"""
		:param: validX : Validation Input Data
		:param: validY : Validation Labels
		:rtype: The predictions and validation accuracy evaluated over the current neural network model
		
		|
		
		"""
		valActivations = self.predict(validX)
		pred = np.argmax(valActivations, axis=1)
		if validY is not None:
			valAcc = self.computeAccuracy(validY, valActivations)
			return pred, valAcc
		else:
			return pred, None

	def predict(self, X):
		# Input
		"""
		:param: X : Current Batch of Input Data as an nparray
		
		:rtype: The predictions made by the model (which are the activations output by the last layer)
		
		::

			Note: Activations at the first layer(input layer) is X itself		
		
		|
		
		"""
		activations = X
		for l in self.layers:
			activations = l.forwardpass(activations)
		return activations







class FullyConnectedLayer:
	def __init__(self, in_nodes, out_nodes, activation):
		# Method to initialize a Fully Connected Layer
		# Parameters
		# in_nodes - number of input nodes of this layer
		# out_nodes - number of output nodes of this layer
		self.in_nodes = in_nodes
		self.out_nodes = out_nodes
		self.activation = activation
		# Stores a quantity that is computed in the forward pass but actually used in the backward pass. Try to identify
		# this quantity to avoid recomputing it in the backward pass and hence, speed up computation
		self.data = None
		self.i = 0

		# Create np arrays of appropriate sizes for weights and biases and initialise them as you see fit
		###############################################
		# TASK 1a (Marks 0) - YOUR CODE HERE
		# raise NotImplementedError
		# self.weights = None

		# Store the gradients with respect to the weights and biases in these variables during the backward pass
		self.weightsGrad = None
		self.biasesGrad = None

		#SWACH CODE
		self.biases = np.random.uniform(size=(1,out_nodes))
		self.weights = np.random.uniform(size=(in_nodes,out_nodes))
		#SWACH CODE

		# print(self.weights)
		# print(self.biases)
		# exit()

		# print(out_nodes.shape)
		# exit()
		# self.biases = None
		###############################################
		# NOTE: You must NOT change the above code but you can add extra variables if necessary

	def relu_of_X(self, X):
		# Input
		"""
		:param X: Output from current layer/input for Activation | ``shape: batchSize x self.out_nodes``
		:rtype: Activations after one forward pass through this relu layer | ``shape: batchSize x self.out_nodes``
		
		::
		
			This will only be called for layers with activation relu
		
		|
		
		"""
		###############################################
		# TASK 1b (Marks 1) - YOUR CODE HERE
		# print("&&&&&&&&&&&&&&&",X)
		X=X.astype(float)

		return np.maximum(X,0)

		# sh= np.shape(X)
		# Y=np.zeros(np.shape(X))
		# for i in range(sh[0]):
		# 	for j in range(sh[1]):
		# 		if X[i,j]>0:
		# 			Y[i,j]=X[i,j]
		# self.data=Y
		# return Y


		# raise NotImplementedError
		###############################################

	def gradient_relu_of_X(self, X, delta):
		# Input
		"""
		:param X: Output from next layer/input | ``shape: batchSize x self.out_nodes``
		:param delta: del_Error/ del_activation_curr | ``shape: batchSize x self.out_nodes``
		:rtype: Current del_Error to pass to current layer in backward pass through relu layer | ``shape: batchSize x self.out_nodes``
		
		::
		
			This will only be called for layers with activation relu amd during backwardpass
		
		|
		
		"""
		###############################################
		# TASK 1e (Marks 1) - YOUR CODE HERE
		# print(X.shape)
		# print(delta.shape)
		# exit()

		# print(X)

		temp = np.where(X>0,delta,0)
		return temp.astype(float)
		# print(temp.shape)
		# exit()
		# raise NotImplementedError
		###############################################

	def softmax_of_X(self, X):
		# Input
		"""
		:param data: Output from current layer/input for Activation | ``shape: batchSize x self.out_nodes``
		:rtype: Activations after one forward pass through this softmax layer | ``shape: batchSize x self.out_nodes``
		
		|
		
		"""
		###############################################
		# TASK 1c (Marks 3) - YOUR CODE HERE
		# raise NotImplementedError
		# print(X)
		# exit()
		# print(np.exp(X))
		# print(sum(np.exp(X)))
		# exit()
		# print(np.exp(X)/sum(np.exp(X)))
		val = np.max(X, axis=1)
		# print(val)
		# exit()

		# print("I am val",val)
		# print("In Softmax",self.i,val)
		# self.i += 1
		numer = np.exp(X-val[:,None])
		numer = np.where(numer==0,1e-300,numer)
		# print(numer)
		# exit()
		denomir = (np.sum(numer,axis=1)[:,None])
		temp = numer/denomir
		# temp = np.where(temp==0,1e-300,temp)
		# print(temp)
		return temp
		# print(temp)
		# print(X)
		# exit()

		###############################################

	def gradient_softmax_of_X(self, X, delta):
		# Input
		"""
		:param data: Output from next layer/input | ``shape: batchSize x self.out_nodes``
		:param delta: ``del_Error/ del_activation_curr`` | ``shape: batchSize x self.out_nodes``
		:rtype: Current del_Error to pass to current layer in backward pass through softmax layer | ``shape: batchSize x self.out_nodes``
		
		::
		
			This will only be called for layers with activation softmax amd during backwardpass
			Hint: You might need to compute Jacobian first
		
		|

		"""
		###############################################
		# TASK 1f (Marks 7) - YOUR CODE HERE
		# print(X.shape)
		# BEGIN
		# X=np.array(X)
		# print(X)
		# print(delta.shape)
		# exit()

		# softMaxJac = []

		# shape=X.shape
		# # print(shape[0])
		# jacobian_m = []
		# # print(X)
		# for i in range(shape[0]):
		# 	temp=X[i].reshape(-1,1)
		# 	#print(temp.shape)
		# 	# print(temp)
		# 	# print(temp.T)
		# 	jac=np.diagflat(temp)
		# 	# print(jac)
		# 	jac= jac- np.dot(temp, temp.T)
		# 	jac=np.dot(jac, delta[i])
		# 	jacobian_m.append(jac)
		# # print(jacobian_m)
		# jacobian_m= np.asarray(jacobian_m)
		# return jacobian_m

		# print(X.shape)
		# exit()
		ls=[]

		count = 0

		for data in X:
			# print(data)
			data = np.array([data])
			# print("data",data)
			# exit()
			jacob = -1*(np.dot(data.T,data))
			
			offset = np.eye(jacob.shape[0])
			diagIndex = np.diag_indices_from(offset)
			offset[diagIndex] *= data.reshape(jacob.shape[0],)
			jacob = jacob + offset
			ls.append(np.dot(delta[count],jacob))
			count = count + 1
			# print("jacob",jacob)
			# diag = np.diag_indices_from(jacob)
			# print(diag)
			# exit()
			# print("jacob[diag]",jacob[diag])
			# print("jacob",jacob)
			# print("data",data)
			# print("data.reshape(jacob.shape[0],)",data.reshape(jacob.shape[0],))

			# jacob[diag] += data.reshape(jacob.shape[0],)
			
			# print("jacob[diag]",jacob[diag])
			# print("jacob",jacob)
			# exit()
			
			# temp=np.dot(delta[j],jacob)
			# ls.append(temp)
	#	print(np.array(ls).shape)
		
		# print(np.array(ls).shape)
		# exit()

		return np.array(ls)
		# END
		# exit()

		# raise NotImplementedError
		###############################################

	def forwardpass(self, X):
		# Input
		"""
		:param activations: Activations from previous layer/input | ``shape: batchSize x self.in_nodes``
		:rtype: Activations after one forward pass through this layer | ``shape: batchSize x self.out_nodes``
		
		|

		"""
		###############################################
		# TASK 1d (Marks 4) - YOUR CODE HERE

		# print([X[0]])
		# exit()

		if self.activation == 'relu':
			# print(X.shape)
			# print(self.weights.shape)
			# print(self.biases.shape)
			# exit()
			prod = np.dot(X,self.weights)
			# print("^^^^^^^^^^^^^^^",prod)
			# exit()
			self.data = self.relu_of_X(prod+self.biases)
			# print("*******")
			# print("relu",self.data)
			# print("*******")
			# exit()
			return self.data
			# raise NotImplementedError
		elif self.activation == 'softmax':
			prod = np.dot(X,self.weights)
			# print(self.biases)
			self.data = self.softmax_of_X(prod+self.biases)
			# print("softmax",self.data)
			# exit()
			return self.data
			# raise NotImplementedError
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()
		###############################################

	def backwardpass(self, activation_prev, delta):
		# Input
		"""
		:param activation_prev: Output from next layer/input | ``shape: batchSize x self.out_nodes``
		:param delta: ``del_Error/ del_activation_curr`` | ``shape: self.out_nodes``
		:rtype: new_delta: ``del_Error/ del_activation_prev`` | ``shape: self.in_nodes``
		
		|

		"""
		###############################################
		# TASK 1g (Marks 6) - YOUR CODE HERE

		# print(delta)
		# print(self.activation)
		if self.activation == 'relu':
			inp_delta = self.gradient_relu_of_X(self.data, delta)
		elif self.activation == 'softmax':
			inp_delta = self.gradient_softmax_of_X(self.data, delta)
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()

		# BEGIN
		rows = activation_prev.shape[0]
		self.weightsGrad =  np.dot(activation_prev.T,inp_delta)/rows
		self.biasesGrad = np.sum(inp_delta, axis=0)/rows

		# print(self.activation,inp_delta)


		# print(inp_delta.shape)
		# print(self.weights.shape)
		# exit()
		temp = np.dot(inp_delta,self.weights.T)
		
		return temp
		# END

		###############################################
		
	def updateWeights(self, lr):
		# Input
		"""
		:param lr: Learning rate being used
		:rtype: None
		
		|

		"""
		###############################################
		# TASK 1h (Marks 2) - YOUR CODE HERE
	

		# print(self.weightsGrad)
		# print(self.biasesGrad)

		# BEGIN
		self.weights -= lr*self.weightsGrad
		self.biases -= lr*self.biasesGrad
		# END
		
		# raise NotImplementedError
		###############################################
		