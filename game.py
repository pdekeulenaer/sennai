from pygame.locals import *
import pygame
import population, util
import math

WHITE = (255,255,255)
BLUE = (0,0,255	)
BLACK = (0,0,0)
PLAYERCOLOR = (150,150,150)
RED = (255,0,0)

class EllipseTrack:
	# def __init__(self):
	_WALL_CONFIG = [
				pygame.Rect(100,100,600,100),
				pygame.Rect(0,0,800,25),
				pygame.Rect(0,275,800,25),
				pygame.Rect(0,25,25,250),
				pygame.Rect(775,25,800,250)
			]

	def __init__(self):
		self.walls = pygame.sprite.Group()
		for wall in self._WALL_CONFIG:
			w = (Wall(BLUE, (wall.x, wall.y, wall.width, wall.height)))
			self.walls.add(w)
		# print pygame.mask.from_surface(w.image).outline(10)

	def draw(self, screen):
		self.walls.draw(screen)
		(outer, inner) = self.getlines()
		pygame.draw.lines(screen, RED, True, outer, 1)
		pygame.draw.lines(screen, RED, True, inner, 1)

	def collide(self, car):
		collisions = pygame.sprite.spritecollide(car, self.walls, False)
		return not(collisions is None or len(collisions) == 0)

	def collide_guides(self, car):
		# guide vectors:
		vectors = car.guidelines_centered()
		intersects = []

		(outer, inner) = self.getlines()
		outersegments = self._line_segments(outer)
		innersegments = self._line_segments(inner)

		p = []
		for v in vectors:
			vectorpoints = []
			vectorpoints += self._collide_lines(v, outersegments)
			vectorpoints += self._collide_lines(v, innersegments)

			if len(vectorpoints) >0 :
				minlength = 10000000
				point = vectorpoints[0]

				for x in vectorpoints:
					l = util.length(car.rect.center, x)
					if (l < minlength):
						minlength = l
						point = x
				
				p += [point]
		
		return p
		# for (x,y) in p:
		# 	pygame.draw.circle(screen, BLACK, (int(x), int(y)),5,5)


	def _line_segments(self, lines):
		lines1 = lines[:]
		lines2 = lines[:]

		lines1.pop(-1)
		lines2.pop(0)
		segments = zip(lines1,lines2)
		return segments

	def _collide_lines(self, vector, lines):		
		intersects = []
		for line in (lines):
			p = util.segment_intersect((vector.A,vector.B),line)
			if p is not None:
				intersects.append(p)

		return intersects

	def getlines(self):
		outer = [(25,25),(775,25),(775,275),(25,275),(25,100)]
		inner = [(100,100),(700,100),(700,200),(100,200),(100,100)]
		return (outer, inner)

class Wall(pygame.sprite.Sprite):
	def __init__(self, color, (x,y, width, height)):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		pygame.draw.rect(self.image, color, (0,0,width,height))
		self.rect = pygame.Rect(x,y,width,height)
		

class CarDisplay(pygame.sprite.Sprite):

	def initialize(self, carobj, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("./assets/car_red_sprite.png")
		self.image = pygame.transform.scale(img, (24,12))
		self._image = self.image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self._setpos(x,y)
		self.obj = carobj
		carobj.sprite = self

	def _setpos(self, x,y):
		self.rect.x = x
		self.rect.y = y

	def _rotate(self, angle):
		center = self.rect.center
		rot = pygame.transform.rotate(self._image, angle)
		rotrect = rot.get_rect()
		rotrect.center = center
		
		self.image = rot
		self.rect = rotrect

	def draw(self, screen):
		self._setpos(self.obj.x, self.obj.y)
		self._rotate(self.obj.orientation)
		screen.blit(self.image, self.rect)

		if self.obj.selected:
			self._draw_guidelines(screen)

	def _draw_guidelines(self, screen, col=RED):
		for p in self.intersectpoints:
			pygame.draw.line(screen, col, (self.rect.center), p,1)

	def guidelines_centered(self):
		vectors = self.obj.guides()
		carcenter = self.rect.center
		vectors = map(lambda l: l.translate(carcenter), vectors)
		return vectors

	# def guidelines(self, screen):
	# 	for v in self.guidelines_centered():
	# 		pygame.draw.line(screen, RED, v.A,v.B,1)


population.CarSpecimen.set_display_handler(CarDisplay)

class App:

	windowWidth = 800
	windowHeight = 600
	player = 0

	_QUITSIG = False

	loop_inputs = {}

	def __init__(self, players=[]):
		self.generation = 1
		self._running = True
		self._display_surf = None
		self._image_surf = None
		self.players = players
		if len(self.players) == 0:
			self.players = [population.CarSpecimen(50,50)]
		self.track = EllipseTrack()

		self._clicked_cars = []

	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
		pygame.display.set_caption('Pygame example')

		self._running = True
		# self._image_surf = pygame.image.load('pygame.png').convert()


	def reload(self):
		selection = self.getselection()
		self.resetselection()
		self.generation += 1
		# breed new players
		# get the brains
		parent_brains = [x.brain for x in selection]
		new_brains = population.breed(parent_brains, len(self.players), True)
		
		# generate new cars
		cars = [population.CarSpecimen(50,50, brain=new_brains[i], name="[{0}] Car {1}".format(self.generation, i)) for i in range(0,len(new_brains))]
		# # print cars
		# for b in new_brains:
		# 	print b.dimension()
		# set new cars and remove old ones
		self.players = cars



	def on_event(self, event):
		if event.type == QUIT:
			self._running = False

	def on_loop(self):
		self.check_collisions()

	def on_render(self):
		self._display_surf.fill(WHITE)
		self.track.draw(self._display_surf)
		for player in self.players:
			player.draw(self._display_surf)
		# self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
		pygame.display.flip()

		# for x in self.players:
		# 	print "{0} on {1}".format(x.name, (x.x,x.y))


	def check_collisions(self):
		for player in self.players:
			coll = self.track.collide(player.sprite)
			if (coll) : player.kill()
			points = self.track.collide_guides(player.sprite)
			player.sprite.intersectpoints = points
			self.loop_inputs[player] = [util.length(player.sprite.rect.center, x) for x in points]


	def pointinsprites(self, point):
		selected = []
		for player in self.players:
			if (player.sprite.rect.collidepoint(point)):
				selected.append(player)

		return selected

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		while (self._running) :
			pygame.event.pump()
			events = pygame.event.get()

			keys = pygame.key.get_pressed()

			if (keys[K_ESCAPE]):
				self._running = False

			if (keys[K_c]):
				# clear all cars
				self.players = []

			if (keys[K_r]):
				# clear all cars
				self.reload()

			if (keys[K_RETURN]):
				print self.getselection()

			for event in events:
				if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
					self._clicked_cars += self.pointinsprites(event.pos)
					[c.select() for c in self._clicked_cars]


			# if (keys[K_a]):
			# 	self.player.turn(1)

			# if (keys[K_d]):
			# 	self.player.turn(-1)

			self.on_loop()
			self.on_render()
			for player in self.players:
				player.act(self.loop_inputs[player])

			if self._QUITSIG: return;
		self.on_cleanup()


	def resetselection(self):
		self._clicked_cars = []

	# getters
	def getselection(self):
		return self._clicked_cars


if __name__ == '__main__' :
	theApp = App()
	theApp.on_execute()