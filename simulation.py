import game, population
import random

# config parameters

# Population
n_cars = 10
start = (50,50)

# Brain
layers = 10
neurons = 20	

# evolution
mutation_rate = 0.10
parents_to_keep = 0.33



# generate the brains
# brains = []
# for i in range(0, n_cars):
	# seed = random.random()
	# brains += [population.NeuronBrain(1,1,layers,neurons, seed)]
	# print seed
brains = [population.NeuronBrain(5,2,layers,neurons, random.random()) for i in range(0,n_cars)]
cars = [population.CarSpecimen(start[0],start[1], brain=brains[i], name="Car {0}".format(i)) for i in range(0,n_cars)]

# # # nparents to keep
# for b in brains:
# 	print b.dimension()
# parents = cars[1:int(n_cars * parents_to_keep)]
# parent_brains = [x.brain for x in parents]


# mutation_func = lambda l: population.mutate(l, mutation_rate, 0.5)
# nbrains = population.breed(parent_brains, n_cars, mutation_func, True)

# print nbrains
# print [x in nbrains for x in parent_brains]


# create the application
# print cars

app = game.App(players=cars)
app.on_execute()
