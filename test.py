import pygame
from pygame.locals import *

class CarDisplay(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = pygame.image.load("red_car.svg")
		self.mask = pygame.mask.from_surface(self.image)


pygame.display.init()
pygame.font.init()