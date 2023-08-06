import numpy as np
import os, shutil
from Layers import InputLayer, Sequential
import glob




class Network:
	def __init__(self, inputLayer = None, hiddenLayers = []):

		# Store some variables
		self.inputLayer = inputLayer
		self.hiddenLayers = hiddenLayers



	def build(self):
		# This is a list of the total network; easier to iterate through
		self.total_network = []
		self.total_network.append(self.inputLayer)
		for layer in range(len(self.hiddenLayers)):
			self.total_network.append(self.hiddenLayers[layer])

		# print(str(self.total_network))

		# Apply weights to all layers (stored in their respective layer class)
		for layer in range(len(self.total_network)):
			if layer != 0:
				self.total_network[layer].add_weights(self.total_network[layer-1].size, self.total_network[layer].size)




	def predict(self, X):
		for layer in range(len(self.total_network)):
			if layer != 0:
				#print(str(self.total_network[layer].size))
				X = self.total_network[layer].predict(X)

		return X



	def backwards(self, X, y, o, training_speed=1):
		error = y - o
		delta = error * (o * (1 - o))

		for layer in range(len(self.total_network)-1, 1, -1):
			delta = self.total_network[layer].backwards(delta, self.total_network[layer-1].res, training_speed)

		self.total_network[1].weights += X.T.dot(delta) * training_speed




	def train(self, X, y, training_speed=1):
		o = self.predict(X)
		self.backwards(X, y, o, training_speed)



	def loss(self, X, y):
		return np.mean(np.square(y - self.predict(X)))



	"""
	TODO: revise this function
	"""
	def detailed_training(self, X, y, epochs, training_speed=1, metrics="limited"):
		# build a function so the training is autonomous
		for i in range(epochs):
			self.train(X, y, training_speed)
			
			if metrics == "full":
				print(str(i) + " epochs completed. Training status: " + str(round((i / epochs) * 100)) + "%")
				print("Loss: " + str(self.loss(X, y)))
			if metrics == "limited" and i%1000 == 0:
				print(str(i) + " epochs completed. Training status: " + str(round((i / epochs) * 100)) + "%")
				print("Loss: " + str(self.loss(X, y)))



	def save_network(self, name, path="\\"):
		# save the network
		if path == "\\":
			path = os.getcwd() + "\\"

		loc = path + name + "\\"
		if os.path.isdir(loc) == False:
			os.mkdir(path + name)
		else:
			shutil.rmtree(loc)
			if os.path.isdir(loc) == False:
				os.mkdir(path + name)


		for layer in range(1, len(self.total_network), 1):
			w_loc = loc + str(layer) + "_" + str(self.total_network[layer].__class__.__name__) + "__" + str(self.total_network[layer].size) + ".txt"
			np.savetxt(w_loc, self.total_network[layer].weights, fmt="%s")