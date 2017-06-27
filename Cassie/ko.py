import os, sys
import sprtSheet
import animationFrames
import animation
import pygame

class KO(pygame.sprite.Sprite):

	def __init__(self, spriteSheetFile, mode=0): #0 is for loop, 1 is for once
		pygame.sprite.Sprite.__init__(self)
		##SPRITESHEET
		self.anim = animationFrames.AnimationFrames(spriteSheetFile, 1280, 720, 7, 6)

		self.image = self.anim.frames[0]
		self.rect = self.image.get_rect()
		##Starting position
		self.rect.x=0
		self.rect.y=0
		##Time
		self.index = 0
		
	def update(self):
                self.index +=1
                if self.index  >= len(self.anim.frames):
                        self.index = len(self.anim.frames) -1
                        return 1 ### Return once finished
                self.image = self.anim.frames[self.index]
