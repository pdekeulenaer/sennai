import math
import random
import util
import time

class CarSpecimen:

	ACCEL_MAX = 5
	ACCEL_MIN = -5

	MAX_SPEED = 1	
	MAX_ANG_SPEED = 5

	_DISPLAY_HANDLER = None

	_GUIDES = [util.Vector(0,1), util.Vector(0,-1), util.Vector(1,1), util.Vector(1,-1), util.Vector(1,0)]
	# _GUIDES = [util.Vector(0,1)]

	@classmethod
	def set_display_handler(cls, handler):
		cls._DISPLAY_HANDLER = handler

	def __init__(self, x,y, orientation=0, speed=5, ang_speed=3, brain=None, name="Anon Car"):
		self.x = x
		self.y = y
		self.orientation = orientation		# in radians
		self.speed = speed
		self.ang_speed = ang_speed
		self._DISPLAY_HANDLER = self._DISPLAY_HANDLER()
		self._DISPLAY_HANDLER.initialize(self, x, y)
		self._ALIVE = True
		self.brain = brain
		self.name = name
		self.selected = False


	def select(self):
		self.selected = True

	def unselect(self):
		self.selected = False

	def act(self, inputs):
		# inputs
		if not self._ALIVE: return None

		out = self.brain.instruction(inputs)

		# print "{0}: Angle {1}, accel {2} - pos: ({3},{4})" .format(self.name, out[0], out[1], self.x, self.y)

		angle = out[0]
		accel = out[1]

		# TODO set controls on max angle and accel
		self.speed = min(self.speed + accel, self.MAX_SPEED)
		self.orientation += (angle * self.ang_speed)

		self.drive()


	def drive(self):
		self.x += math.cos(math.radians(self.orientation)) * self.speed
		self.y -= math.sin(math.radians(self.orientation)) * self.speed
		
	def turn(self, r):
		self.orientation += r*self.ang_speed

	def guides(self):
		return map(lambda l: l.normalize(1000).rotate(-self.orientation), self._GUIDES)

	def draw(self, params=None):
		self._DISPLAY_HANDLER.draw(params)

	def set_inputs(self, distances):
		self.distances = distances

	def kill(self):
		self._ALIVE = False

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

	def instruction(self):
		angle = 0
		accel = 0.5
		return (angle, accel)


# class DumbBrain(Brain):
# 	def instruction(self):
# 		return (0,0.5)

def mutate(parent, mutation_rate, BIAS=-0.5):
	random.seed(time.time())
	print time.time()

	mutant = parent.copy()
	mutated_weights = []
	for layer in mutant.weights:
		new_layer = []
		for node in layer:
			x = []
			for weight in node:
				# print node
				
				if (random.random() > mutation_rate):
					x.append(weight)
					# print "KEEPING weight"
				else:
					w = (random.random() + BIAS)
					# print w
					x.append(w)
				# print x
			# w = map(lambda l: l if (random.random() < mutation_rate) else (random.random() + BIAS), x)
			new_layer.append(x)
		mutated_weights.append(new_layer)

	mutant.weights = mutated_weights
	# print mutant.weights
	# print "OLD"
	# print parent.weights
	# print "NEW"
	# print mutated_weights

	return mutant


def breed(parents, n_children, include_parents=True,):
	population = []

	if include_parents: population += parents
	for i in range (0, n_children - len(population)):
		newbrain = mutate(random.choice(parents), 0.20, -0.5)
		population.append(newbrain)

	return population

class NeuronBrain(Brain):
	def __init__(self, n_in, n_out, layers, nodes, seed=None):
		Brain.__init__(self)

		self.weights = []
		self.BIAS = -0.5

		self.n_layers = layers
		self.n_nodes_per_layer = nodes
		self.n_in = n_in
		self.n_out = n_out

		# random.seed(seed)

		self._generate_weights()
		self.activation_func = ActivationFunctions.sigmoid

		self.inputs = [0]*n_in

	def copy(self):
		brain = NeuronBrain(self.n_in, self.n_out, self.n_layers, self.n_nodes_per_layer, "NO SEED")
		brain.weights = self.weights 
		return brain

	# helper function to see the dimension
	def dimension(self):
		sizes = []
		for layer in self.weights:
			sizes.append((len(layer[0]), len(layer)))

		print sizes

	def instruction(self, inputs):
		print inputs
		return self._forward_propagate(map(lambda l: l/100.0, inputs))

	def _generate_weights(self):
		if (self.n_layers > 0):
			self.weights.append([[random.random() + self.BIAS for p in range (0, self.n_in)] for x in range(0, self.n_nodes_per_layer)])
		for i in range(1,self.n_layers):
			self.weights.append([[random.random()  + self.BIAS for p in range (0, self.n_nodes_per_layer)] for x in range(0, self.n_nodes_per_layer)])
		self.weights.append([[random.random()  + self.BIAS for p in range (0, self.n_nodes_per_layer)] for x in range(0, self.n_out)])

	def _forward_propagate(self, inputs):
		# input to layer 1
		if len(inputs) != self.n_in:
			inputs = self.inputs

		self.inputs = inputs

		# process input layer
		if (self.n_layers > 0):
			inputs = self._process_layer(inputs, self.weights[0])

		for i in range(1, self.n_layers):
			inputs = self._process_layer(inputs, self.weights[i])

		# out = self._process_layer(inputs, self.weights[self.n_layers])
		finalweights = self.weights[self.n_layers]
		out = []
		for node in range (0, len(finalweights)):
			out.append(util.lincomb(inputs, finalweights[node]))

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
		


brain = NeuronBrain(2,2,1,1,random.random())
w = brain.weights[0]
inputs = [-4,5]
output = brain._forward_propagate(inputs)

print output