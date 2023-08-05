import numpy as np

class ANN(object):
	"""
	The (simple) Artificial Neural Network class features a simple neural network which consists
	of at least one input and one output layer. It can thereby utilize 5 hidden layers to do the
	calculations
	"""
	def __init__(self, inputSize=0, outputSize=0, hiddenSize1 = 0, 
		hiddenSize2 = 0, hiddenSize3 = 0, hiddenSize4 = 0, hiddenSize5 = 0):

		# test_layers(inputSize, outputSize, hiddenSize1, hiddenSize2, hiddenSize3, hiddenSize4, hiddenSize5)

		# Get the data
		self.inputSize = inputSize
		self.outputSize = outputSize
		self.hiddenSize1 = hiddenSize1
		self.hiddenSize2 = hiddenSize2
		self.hiddenSize3 = hiddenSize3
		self.hiddenSize4 = hiddenSize4
		self.hiddenSize5 = hiddenSize5

		# Create the weight matrices (depending on how many hidden layers there are)
		if self.hiddenSize1 == 0:
			self.W1 = np.random.randn(self.inputSize, self.outputSize)
		if self.hiddenSize1 != 0:
			self.W1 = np.random.randn(self.inputSize, self.hiddenSize1)
			if self.hiddenSize2 == 0:
				self.W2 = np.random.randn(self.hiddenSize1, self.outputSize)
			if self.hiddenSize2 != 0:
				self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)
				if hiddenSize3 == 0:
					self.W3 = np.random.randn(self.hiddenSize2, self.outputSize)
				if hiddenSize3 != 0:
					self.W3 = np.random.randn(self.hiddenSize2, self.hiddenSize3)
					if hiddenSize4 == 0:
						self.W4 = np.random.randn(self.hiddenSize3, self.outputSize)
					if hiddenSize4 != 0:
						self.W4 = np.random.randn(self.hiddenSize3, self.hiddenSize4)
						if hiddenSize5 == 0:
							self.W5 = np.random.randn(self.hiddenSize4, self.outputSize)
						if hiddenSize5 != 0:
							self.W5 = np.random.randn(self.hiddenSize4, self.hiddenSize5)
							self.W6 = np.random.randn(self.hiddenSize5, self.outputSize)



	def forward(self, X):
		"""
		The forward function propagates an input X to the network. It returns an output o.
		"""
		self.z = np.dot(X, self.W1)

		if self.hiddenSize1 == 0:
			o = self.sigmoid(self.z)
			return o
		if self.hiddenSize1 != 0:
			self.z2 = self.sigmoid(self.z)
			self.z3 = np.dot(self.z2, self.W2)

			if self.hiddenSize2 == 0:
				o = self.sigmoid(self.z3)
				return o
			if self.hiddenSize2 != 0:
				self.z4 = self.sigmoid(self.z3)
				self.z5 = np.dot(self.z4, self.W3)

				if self.hiddenSize3 == 0:
					o = self.sigmoid(self.z5)
					return o
				if self.hiddenSize3 != 0:
					self.z6 = self.sigmoid(self.z5)
					self.z7 = np.dot(self.z6, self.W4)

					if self.hiddenSize4 == 0:
						o = self.sigmoid(self.z7)
						return o
					if self.hiddenSize4 != 0:
						self.z8 = self.sigmoid(self.z7)
						self.z9 = np.dot(self.z8, self.W5)

						if self.hiddenSize5 == 0:
							o = self.sigmoid(self.z9)
							return o
						if self.hiddenSize5 != 0:
							self.z10 = self.sigmoid(self.z9)
							self.z11 = np.dot(self.z10, self.W6)
							o = self.sigmoid(self.z11)
							return o


	def backward(self, X, y, o, training_speed = 1):
		"""
		This function trains the network, based on an input X, the correct answer y and
		the calculated answer o. It also features a training_speed variable that can
		regulate how precise the network can be trained. Default is 1
		"""
		# training the network
		if self.hiddenSize1 == 0:
			self.o_error = y - o
			self.o_delta = self.o_error * self.sigmoidPrime(o)
			self.W1 += X.T.dot(self.o_delta) * training_speed
		if self.hiddenSize1 != 0:
			if self.hiddenSize2 == 0:
				self.o_error = y - o
				self.o_delta = self.o_error * self.sigmoidPrime(o)

				self.z2_error = self.o_delta.dot(self.W2.T)
				self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2)

				self.W1 += X.T.dot(self.z2_delta) * training_speed
				self.W2 += self.z2.T.dot(self.o_delta) * training_speed

			if self.hiddenSize2 != 0:
				if self.hiddenSize3 == 0:
					self.o_error = y - o
					self.o_delta = self.o_error * self.sigmoidPrime(o)

					self.z4_error = self.o_delta.dot(self.W3.T)
					self.z4_delta = self.z4_error * self.sigmoidPrime(self.z4)

					self.z2_error = self.z4_delta.dot(self.W2.T)
					self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

					self.W1 += X.T.dot(self.z2_delta) * training_speed
					self.W2 += self.z2.T.dot(self.z4_delta) * training_speed
					self.W3 += self.z4.T.dot(self.o_delta) * training_speed

				if self.hiddenSize3 != 0:
					if self.hiddenSize4 == 0:
						self.o_error = y - o
						self.o_delta = self.o_error * self.sigmoidPrime(o)

						self.z6_error = self.o_delta.dot(self.W4.T)
						self.z6_delta = self.z6_error * self.sigmoidPrime(self.z6) 

						self.z4_error = self.z6_delta.dot(self.W3.T)
						self.z4_delta = self.z4_error * self.sigmoidPrime(self.z4)

						self.z2_error = self.z4_delta.dot(self.W2.T)
						self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

						self.W1 += X.T.dot(self.z2_delta) * training_speed
						self.W2 += self.z2.T.dot(self.z4_delta) * training_speed
						self.W3 += self.z4.T.dot(self.z6_delta) * training_speed
						self.W4 += self.z6.T.dot(self.o_delta) * training_speed

					if self.hiddenSize4 != 0:
						if self.hiddenSize5 == 0:
							self.o_error = y - o
							self.o_delta = self.o_error * self.sigmoidPrime(o)

							self.z8_error = self.o_delta.dot(self.W5.T)
							self.z8_delta = self.z8_error * self.sigmoidPrime(self.z8)

							self.z6_error = self.z8_delta.dot(self.W4.T)
							self.z6_delta = self.z6_error * self.sigmoidPrime(self.z6) 

							self.z4_error = self.z6_delta.dot(self.W3.T)
							self.z4_delta = self.z4_error * self.sigmoidPrime(self.z4)

							self.z2_error = self.z4_delta.dot(self.W2.T)
							self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

							self.W1 += X.T.dot(self.z2_delta) * training_speed
							self.W2 += self.z2.T.dot(self.z4_delta) * training_speed
							self.W3 += self.z4.T.dot(self.z6_delta) * training_speed
							self.W4 += self.z6.T.dot(self.z8_delta) * training_speed
							self.W5 += self.z8.T.dot(self.o_delta) * training_speed

						if self.hiddenSize5 != 0:
							self.o_error = y - o
							self.o_delta = self.o_error * self.sigmoidPrime(o)

							self.z10_error = self.o_delta.dot(self.W6.T)
							self.z10_delta = self.z10_error * self.sigmoidPrime(self.z10)

							self.z8_error = self.z10_delta.dot(self.W5.T)
							self.z8_delta = self.z8_error * self.sigmoidPrime(self.z8)

							self.z6_error = self.z8_delta.dot(self.W4.T)
							self.z6_delta = self.z6_error * self.sigmoidPrime(self.z6) 

							self.z4_error = self.z6_delta.dot(self.W3.T)
							self.z4_delta = self.z4_error * self.sigmoidPrime(self.z4)

							self.z2_error = self.z4_delta.dot(self.W2.T)
							self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

							self.W1 += X.T.dot(self.z2_delta) * training_speed
							self.W2 += self.z2.T.dot(self.z4_delta) * training_speed
							self.W3 += self.z4.T.dot(self.z6_delta) * training_speed
							self.W4 += self.z6.T.dot(self.z8_delta) * training_speed
							self.W5 += self.z8.T.dot(self.z10_delta) * training_speed
							self.W6 += self.z10.T.dot(self.o_delta) * training_speed



	def train(self, X, y, training_speed = 1):
		o = self.forward(X)
		self.backward(X, y, o, training_speed)


	def predict(self, xPredicted):
		return self.forward(xPredicted)


	def sigmoid(self, s):
		return 1/(1+np.exp(-s))


	def sigmoidPrime(self, s):
		# derivative of sigmoid function
		return (s * (1 - s))


	# some extra goofy functions:
	def save_weights(self):
		np.savetxt("w1.txt", self.W1, fmt="%s")
		if self.hiddenSize1 != 0: np.savetxt("w2.txt", self.W2, fmt="%s")
		if self.hiddenSize2 != 0: np.savetxt("w3.txt", self.W3, fmt="%s")
		if self.hiddenSize3 != 0: np.savetxt("w4.txt", self.W4, fmt="%s")
		if self.hiddenSize4 != 0: np.savetxt("w5.txt", self.W5, fmt="%s")
		if self.hiddenSize5 != 0: np.savetxt("w6.txt", self.W6, fmt="%s")