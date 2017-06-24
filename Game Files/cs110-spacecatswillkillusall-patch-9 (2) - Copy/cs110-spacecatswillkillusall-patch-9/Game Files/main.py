import character
import shittyBackground
import pygame
import pygame.locals
import random
import os, sys
import sprtSheet

class Controller:

	def __init__(self, width=1280, height=720):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Kitty Fight')
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.backgroundImage = shittyBackground.fuckingBackground("Epic-Sunset.png", [0,0])
		self.clock = pygame.time.Clock()
		"""Load the sprites that we need"""
		self.player1 = character.Character("Skullcrusher", 50, height-279, "spritestrip.png")
		self.player2 = character.Character("Demon Slayer", width-318, height-279, "spritestrip.png")
		self.player1Controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
		self.player2Controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
		self.sprites = pygame.sprite.Group((self.player1, self.player2))
		
	def mainLoop(self):
		"""This is the Main Loop of the Game"""
		gameOn = True
		pygame.key.set_repeat(1, 1)
		while gameOn == True:
			self.background.fill((250, 250, 250))
			#This variable is for registering simultaneous inputs
			# This way, both characters can move at the same time, instead of having
			# pygame register only one key at a time
			keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					gameOn = False
				if event.type == pygame.KEYDOWN:
					self.player1.move1(keys)
					self.player2.move2(keys)
					#Event.type is one input, so you can't block and do other stuff
					#We can't put block in our fight function, because our fight function only works once the key is up
					#We also can't put it in our move function, because you can move and fight
					#self.player1.block1(event.key)
					#print("P1 Position: " + str(self.player1.rect.x))
					#print("P2 Position: " + str(self.player2.rect.y))
					if event.key == pygame.K_h:
						self.player1.block1(event.key)
					if event.key == pygame.K_KP6:
						self.player2.block2(event.key)
					break
				if event.type == pygame.KEYUP:
					self.player1.fight1(event.key, self.player2)
					self.player2.fight2(event.key, self.player1)
					self.player1.unblock1(event.key)
					self.player1.unblock2(event.key)
					#self.player1.update()
					#self.player2.update()
	
					
					#print("P1 Health: " + str(self.player1.health))
					break
				
				
			if(self.player1.health == 0):
				self.player1.kill()
				print("KO PLAYER1")
			if(self.player2.health == 0):
				self.player2.kill()
				print("KO PLAYER2")
				#self.screen.blit(pygame.font.SysFont("monospace", 15).render("Game Over", 1, (255, 0, 0)), (100, 100))
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.backgroundImage.image, self.backgroundImage.rect)
			self.sprites.draw(self.screen)
			pygame.draw.rect(self.screen, self.player1.healthColor, [10, 10, 4*self.player1.health, 50])
			pygame.draw.rect(self.screen, self.player2.healthColor, [1270-(4*self.player2.health), 10, 4*self.player2.health, 50])
			pygame.display.flip()
			self.clock.tick(60)


def main():

	main_window = Controller()
	main_window.mainLoop()
	pygame.quit()

main()
