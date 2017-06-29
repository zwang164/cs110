import pygame
import sprtSheet
import os, sys

''' This takes an entire spritesheet and puts each spritesheet image into a list of all the animation
    frames so that way we can access those frames later and cycle through an animation.'''

class AnimationFrames:

	def __init__(self, spriteSheetFile, width, height, rows, columns, mode=0): #0 is for loops, 1 is for once

		spriteSheet = sprtSheet.SpriteSheet(spriteSheetFile)
		self.frames = []

		'''Row first, then columns'''
		for i in range(columns):
			for j in range(rows):
				image = spriteSheet.getImage(j*width, i*height, width, height)
				self.frames.append(image)
