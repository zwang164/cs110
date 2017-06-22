import os
import sys
import pygame

class fuckingBackground(pygame.sprite.Sprite):
	def __init__(self, imageFile, location):
		pygame.sprite.Sprite.__init__(self)
		try:
			shittyImage = os.path.join("assets", imageFile)
			self.image = pygame.image.load(shittyImage)
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.top = location
			
		except pygame.error as message:
			print("This image isn't fucking loading: ", imageFile)
			raise SystemExit(message)
