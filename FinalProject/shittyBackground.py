import os
import sys
import pygame

class fuckingBackground(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, rescale, colorkey=None):
		pygame.sprite.Sprite.__init__(self)
		try:
			shittyImage = os.path.join("assets", imageFile)
			self.image = pygame.image.load(shittyImage).convert()
			self.image = pygame.transform.scale(self.image, rescale)
			self.image.set_colorkey(colorkey)
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.top = location
			
		except pygame.error as message:
			print("This image isn't fucking loading: ", imageFile)
			raise SystemExit(message)
