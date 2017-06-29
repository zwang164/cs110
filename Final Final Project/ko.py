import os, sys
import sprtSheet
import animationFrames
import pygame

class KO(pygame.sprite.Sprite):

	def __init__(self, spriteSheetFile, mode=0):
		pygame.sprite.Sprite.__init__(self)
		'''Loads our spritesheet and cycles through it applying each frame to a list so we can access it later.'''
		self.anim = animationFrames.AnimationFrames(spriteSheetFile, 1280, 720, 7, 6)

		'''Sets the starting image'''
		self.image = self.anim.frames[0]
		self.rect = self.image.get_rect()

		'''Sets the starting position'''
		self.rect.x=0
		self.rect.y=0

		'''Initializes a timer'''
		self.index = 0
		
	def update(self):

		'''Cycles through the frames based on the timer. The timer times based on the game's frate rate.
		if the timer is greater than the length of the list, the timer stops.'''
		self.index +=1
		if self.index  >= len(self.anim.frames):
			self.index = len(self.anim.frames) -1
			return 1
		self.image = self.anim.frames[self.index]
