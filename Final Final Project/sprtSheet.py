import pygame
import os, sys

class SpriteSheet(object):
 
	def __init__(self, shitImage):

		'''Loads the bigass spritesheet'''
		shitterImage = os.path.join('assets', shitImage)
		self.sprite_sheet = pygame.image.load(shitterImage).convert()
 
 
	def getImage(self, x, y, width, height, colorkey=-1):

		'''Creates a new blank image for the bigass spritesheet'''
		image = pygame.Surface([width, height]).convert()
 
		'''Takes the bigass spritesheet and copies a single frame of it into the blank image'''
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
		
		'''Unless specified otherwise, the color located at the top left corner
		of the image is taken as the transparent color.'''
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey)
		
		return image
