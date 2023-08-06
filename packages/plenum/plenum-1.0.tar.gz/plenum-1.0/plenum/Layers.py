import numpy as np



def sigmoid(s):
	return 1/(1+np.exp(-s))

def sigmoidPrime(s):
	return (s * (1 - s))


def HypTan(s):
	return ((np.exp(s) - np.exp(-s)) / (np.exp(s) + np.exp(-s)))

def HypTanPrime(s):
	return (1 - np.power(HypTan(s), 2))


def SoftPlus(s):
	return np.log(1 + np.exp(s))

def SoftPlusPrime(s):
	return sigmoid(s)





class InputLayer:
	def __init__(self, size):
		self.size = size



class Sequential:
	def __init__(self, size, activation="sigmoid", trainable=1):
		self.size = size
		self.activation = activation


	def add_weights(self, height, width):
		self.weights = np.random.randn(height, width)


	def predict(self, X):
		o = np.dot(X, self.weights)
		if self.activation == "sigmoid":
			self.res = sigmoid(o)
		if self.activation == "hyptan":
			self.res = HypTan(o)
		if self.activation == "softplus":
			self.res = SoftPlus(o)

		return self.res


	def backwards(self, delta, res_b, training_speed=1):
		self.weights += res_b.T.dot(delta) * training_speed
		error = delta.dot(self.weights.T)
		if self.activation == "sigmoid":
			delta = error * sigmoidPrime(res_b)
		if self.activation == "hyptan":
			delta = error * HypTanPrime(res_b)
		if self.activation == "softplus":
			delta = error * SoftPlusPrime(res_b)
			
		return delta