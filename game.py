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
	walls = [
				pygame.Rect(100,100,600,100),
				pygame.Rect(0,0,800,25),
				pygame.Rect(0,275,800,25),
				pygame.Rect(0,25,25,250),
				pygame.Rect(775,25,800,250)
			]


	def draw(self, screen):
		for rect in self.walls:
			pygame.draw.rect(screen, BLUE, rect)



class CarDisplay(pygame.sprite.Sprite):
	def __init__(self, carobj):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("./car_red_sprite.png")
		self.image = pygame.transform.scale(img, (24,12))
		self._image = self.image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		self.obj = carobj

	def setpos(self, x,y):
		self.rect.x = x
		self.rect.y = y

		print self.rect.center

	def rotate(self, angle):
		center = self.rect.center
		rot = pygame.transform.rotate(self._image, angle)
		rotrect = rot.get_rect()
		rotrect.center = center
		# rot.get_rect().center = center
		# print rot.get_rect().center
		self.image = rot
		self.rect = rotrect

		# self.image = pygame.transform.rotate(self._image, angle	)
		# self.rect = self.image.get_rect()

	def draw(self, screen):
		self.setpos(self.obj.x, self.obj.y)
		self.rotate(self.obj.orientation)
		screen.blit(self.image, self.rect)

class Player:

	def __init__(self):
		carobj = population.Car(50,50)
		self.obj = carobj
		self.sprite = CarDisplay(carobj)

	def moveRight(self):
		self.obj.move(self.obj.speed,0)

	def moveLeft(self):
		self.obj.move(-self.obj.speed,0)

	def moveUp(self):
		self.obj.move(0, -self.obj.speed)

	def moveDown(self):
		self.obj.move(0, self.obj.speed)

	def draw(self, screen):
		self.sprite.draw(screen)

	def turn(self, turnradius):
		self.obj.turn(turnradius)

	def drive(self):
		self.obj.forward()

class App:

	windowWidth = 800
	windowHeight = 600
	player = 0

	def __init__(self):
		self._running = True
		self._display_surf = None
		self._image_surf = None
		self.player = Player()
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
		# rect = self.player.rect()
		# for wall in self.track.walls:
		# 	if (rect.colliderect(wall)):
		# 		self.player.color = RED
		# 		return
		# self.player.color=BLUE
		pass

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		while (self._running) :
			pygame.event.pump()
			keys = pygame.key.get_pressed()

			# if (keys[K_RIGHT]):
			# 	self.player.moveRight()

			# if (keys[K_LEFT]):
			# 	self.player.moveLeft()

			# if (keys[K_DOWN]):
			# 	self.player.moveDown()

			# if (keys[K_UP]):
			# 	self.player.moveUp()

			if (keys[K_ESCAPE]):
				self._running = False

			if (keys[K_a]):
				self.player.turn(1)

			if (keys[K_d]):
				self.player.turn(-1)

			self.on_loop()
			self.on_render()

			self.player.drive()

		self.on_cleanup()

if __name__ == '__main__' :
	theApp = App()
	theApp.on_execute()