import character
import shittyBackground
import pygame
import random
import sys
import sprtSheet

class Controller:

	def __init__(self, width=1280, height=720):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.backgroundImage = shittyBackground.fuckingBackground("Epic-Sunset.png", [0,0])
		"""Load the sprites that we need"""
		self.player1 = character.Character("Skullcrusher", 50, height-279, "Siamese-Cat.png")
		self.player2 = character.Character("Demon Slayer", width-318, height-279, "Siamese-Cat1.png")
		self.player1Controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
		self.player2Controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
		self.sprites = pygame.sprite.Group((self.player1, self.player2))
		##SPRITESHEET TEST
		##self.spriteSheet = sprtSheet.Sprtsheet("spritesheet-demo.png")
		##sprtSheet.Sprtsheet.charImg[3]
		
	def mainLoop(self):
		"""This is the Main Loop of the Game"""
		gameOn = True
		pygame.key.set_repeat(1,50)
		while gameOn == True:
			self.background.fill((250, 250, 250))
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOn = False
				if event.type == pygame.KEYDOWN:
					self.player2.move(event.key)
					self.player1.move(event.key)
					print("Event Key:" + str(event.key))
					print("P1 Position: " + str(self.player1.rect.x))
					print("P2 Position: " + str(self.player2.rect.y))
					if(pygame.sprite.collide_rect(self.player1, self.player2)):
						print("CAT COLLISION!")
						self.player2.fight(event.key, self.player1)
						print("P1 Health: " + str(self.player1.health))
					#Call Health Bar function within fight fuction later once fight gets working
					self.player1.healthBar()
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
			###SPRITE TEST
			##self.newSprite.draw(self.screen)
			####
			pygame.draw.rect(self.screen, self.player1.healthColor, [10, 10, 4*self.player1.health, 50])
			pygame.draw.rect(self.screen, self.player2.healthColor, [1270-(4*self.player2.health), 10, 4*self.player2.health, 50])
			pygame.display.flip()


def main():

	main_window = Controller()
	main_window.mainLoop()
	pygame.quit()

main()
