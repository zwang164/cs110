import pygame
import os
import sys

class Sprtsheet(pygame.sprite.Sprite):
		def __init__(self, imageFile):
			pygame.sprite.Sprite.__init__(self)
			try:
				shittyImage = os.path.join("assets", imageFile)
				self.sheet = pygame.image.load(shittyImage) 	#load the sheet 	

				self.sheet_rect_x=0
				self.sheet_rect_y=0
				self.sheet_len_rect_x=1
				self.sheet_len_rect_y=1

				self.charImg = []
				for row in range(5):
					for i in range(10):		
						#locate the sprite
						self.sheet.set_clip(pygame.Rect(self.sheet_rect_x,self.sheet_rect_y,self.sheet_len_rect_x,self.sheet_len_rect_y)) 
						self.sprite = self.sheet.subsurface(self.sheet.get_clip())   #extract sprite
						self.charImg.append(self.sprite)
						self.sheet_rect_x += 1
					self.sheet_rect_y += 1
	
			except pygame.error as message:
				print("This image isn't loading: ", imageFile)
				raise SystemExit(message)
	

