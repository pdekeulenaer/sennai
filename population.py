import math



class Car:

	ACCEL_MAX = 5
	ACCEL_MIN = -5

	MAX_SPEED = 5
	MAX_ANG_SPEED = 5

	QUART = math.radians(90)

	def __init__(self, x,y, orientation=0, speed=1, ang_speed=1):
		self.x = x
		self.y = y
		self.orientation = orientation		# in radians
		self.speed = speed
		self.ang_speed = ang_speed

	# def bounds(self):
	# 	points = [(self.LENGTH/2, self.WIDTH/2), (self.LENGTH/2, -self.WIDTH/2), (-self.LENGTH/2, -self.WIDTH/2), (-self.LENGTH/2, self.WIDTH/2)]
	# 	rotated = map(lambda l: self.rotate(self.orientation, l), points)

	# 	translated = map(lambda (x,y): (self.x_center + x, self.y_center + y), rotated)
	# 	return translated

	# def rotate(self, theta, (x,y)):
	# 	return ((x * math.cos(theta) - y* math.sin(theta)),(x*math.sin(theta)+y*math.cos(theta)))

	def move(self, x, y):
		self.x += x
		self.y += y

	def forward(self):
		self.x += math.cos(math.radians(self.orientation)) * self.speed
		self.y -= math.sin(math.radians(self.orientation)) * self.speed

	def turn(self, r):
		self.orientation += r*self.ang_speed


# car = Car(0,0,math.radians(45))
# bounds = car.bounds()
# print car.orientation

# for b in bounds:
# 	print b
