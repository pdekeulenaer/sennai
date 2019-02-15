from pygame.locals import *
import pygame
import population
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
			print w.rect
			self.walls.add(w)

	def draw(self, screen):
		self.walls.draw(screen)

	def collide(self, car):
		collisions = pygame.sprite.spritecollide(car, self.walls, False)
		return not(collisions is None or len(collisions) == 0)

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


population.CarSpecimen.set_display_handler(CarDisplay)

class App:

	windowWidth = 800
	windowHeight = 600
	player = 0

	_QUITSIG = False

	def __init__(self):
		self._running = True
		self._display_surf = None
		self._image_surf = None
		self.player = population.CarSpecimen(50,50)
		self.track = EllipseTrack()

	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
		pygame.display.set_caption('Pygame example')

		self._running = True
		# self._image_surf = pygame.image.load('pygame.png').convert()

	def on_event(self, event):
		if event.type == QUIT:
			self._running = False

	def on_loop(self):
		self.check_collisions()

	def on_render(self):
		self._display_surf.fill(WHITE)
		self.track.draw(self._display_surf)
		self.player.draw(self._display_surf)
		# self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
		pygame.display.flip()

	def check_collisions(self):
		coll = self.track.collide(self.player.sprite)
		print coll
		if (coll) : self._QUITSIG = True
		

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		while (self._running) :
			pygame.event.pump()
			keys = pygame.key.get_pressed()

			if (keys[K_ESCAPE]):
				self._running = False

			if (keys[K_a]):
				self.player.turn(1)

			if (keys[K_d]):
				self.player.turn(-1)

			self.on_loop()
			self.on_render()
			self.player.forward()

			if self._QUITSIG: return;
		self.on_cleanup()

if __name__ == '__main__' :
	theApp = App()
	theApp.on_execute()