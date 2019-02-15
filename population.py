import math
import random
import util

class CarSpecimen:

	ACCEL_MAX = 5
	ACCEL_MIN = -5

	MAX_SPEED = 5
	MAX_ANG_SPEED = 5

	_DISPLAY_HANDLER = None

	@classmethod
	def set_display_handler(cls, handler):
		cls._DISPLAY_HANDLER = handler()

	def __init__(self, x,y, orientation=0, speed=1, ang_speed=1):
		self.x = x
		self.y = y
		self.orientation = orientation		# in radians
		self.speed = speed
		self.ang_speed = ang_speed
		self._DISPLAY_HANDLER.initialize(self, x, y)

	def move(self, x, y):
		self.x += x
		self.y += y

	def forward(self):
		self.x += math.cos(math.radians(self.orientation)) * self.speed
		self.y -= math.sin(math.radians(self.orientation)) * self.speed
		# print self.speed

	def turn(self, r):
		self.orientation += r*self.ang_speed

	def draw(self, params=None):
		self._DISPLAY_HANDLER.draw(params)

# car = Car(0,0,math.radians(45))
# bounds = car.bounds()
# print car.orientation

# for b in bounds:
# 	print b

class Brain:
	
	n_in = 0
	n_out = 0

	def __init__(self):
		pass

	def compute(self, input):
		pass

class NeuronBrain(Brain):
	n_layers = 0
	n_nodes_per_layer = 0
	weights = []
	BIAS = -0.5

	def __init__(self, n_in, n_out, layers, nodes):
		Brain.__init__(self)
		self.n_layers = layers
		self.n_nodes_per_layer = nodes
		self.n_in = n_in
		self.n_out = n_out
		self._generate_weights()
		self.activation_func = ActivationFunctions.sigmoid

	def _generate_weights(self):
		if (self.n_layers > 0):
			self.weights.append([[random.random() + self.BIAS for p in range (0, self.n_in)] for x in range(0, self.n_nodes_per_layer)])
		for i in range(1,self.n_layers):
			self.weights.append([[random.random()  + self.BIAS for p in range (0, self.n_nodes_per_layer)] for x in range(0, self.n_nodes_per_layer)])
		self.weights.append([[random.random()  + self.BIAS for p in range (0, self.n_nodes_per_layer)] for x in range(0, self.n_out)])

	def _forward_propagate(self, inputs):
		# input to layer 1
		assert len(inputs) == self.n_in


		# process input layer
		if (self.n_layers > 0):
			print "IN: " + str(inputs)
			inputs = self._process_layer(inputs, self.weights[0])
			print "OUT: " + str(inputs)

		for i in range(1, self.n_layers):
			inputs = self._process_layer(inputs, self.weights[i])
			print "OUT: " + str(inputs)
		out = self._process_layer(inputs, self.weights[self.n_layers])
		print "OUT: " + str(out)
		return out

	def _process_layer(self, inputs, weights):
		output = []
		for node in range (0, len(weights)):
			x = util.lincomb(inputs, weights[node])
			output.append(self.activation_func(x))

		return output


class ActivationFunctions:
	@staticmethod
	def sigmoid(i):
		return (1.0)/(1.0 + math.exp(-i))
		


# brain = NeuronBrain(2,2,10,100)
# w = brain.weights[0]
# inputs = [-4,5]
# output = brain._forward_propagate(inputs)

# print output