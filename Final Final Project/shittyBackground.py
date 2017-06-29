import os
import sys
import pygame

class fuckingBackground(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, rescale, colorkey=None):
		pygame.sprite.Sprite.__init__(self)
		try:
			'''Tries to load our background and scales it based on the
			size of the screen, so we can load large images for different resolutions.
			Doesn't set a transparent color unless specified,
			and also sets the location the background appears.'''
			shittyImage = os.path.join("assets", imageFile)
			self.image = pygame.image.load(shittyImage).convert()
			self.image = pygame.transform.scale(self.image, rescale)
			self.image.set_colorkey(colorkey)
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.top = location
			
		except pygame.error as message:
			print("This image isn't fucking loading: ", imageFile)
			raise SystemExit(message)
