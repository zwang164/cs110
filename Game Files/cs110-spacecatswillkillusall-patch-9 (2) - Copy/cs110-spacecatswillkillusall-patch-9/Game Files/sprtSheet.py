import pygame
import os, sys

class SpriteSheet(object):
 
	def __init__(self, shitImage):

		# Load the sprite sheet.
		shitterImage = os.path.join('assets', shitImage)
		self.sprite_sheet = pygame.image.load(shitterImage).convert()
 
 
	def getImage(self, x, y, width, height):

		# Create a new blank image
		image = pygame.Surface([width, height]).convert()
 
		# Takes the larger sprite sheet and copies part of it onto the blank image
		#draw clip on new blank image (source,destination: new blank iamge, area of clip)
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
		
		# Makes black transparent, because transparency is loaded black
		image.set_colorkey((0, 0, 0))
		
		return image
