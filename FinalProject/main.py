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
		
	
		
		self.introLoop()
		self.clock = pygame.time.Clock()
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.backgroundImage = shittyBackground.fuckingBackground("Epic-Sunset.png", [0,0])
		"Load the sprites that we need"""
		self.player1 = character.Character("Skullcrusher", 50, height-279, "spritestrip.png")
		self.player2 = character.Character("Demon Slayer", width-318, height-279, "spritestrip.png")
		self.player1Controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
		self.player2Controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
		
		self.sprites = pygame.sprite.Group((self.player1, self.player2))

	def introLoop(self):
		intro = True
		self.screen.fill((255,255,255))
		pygame.mixer.music.load("../FinalProject/assets/tekken.mp3")
		pygame.mixer.music.set_volume(.5)
		pygame.mixer.music.play(-1)

		playButton = pygame.image.load(os.path.join('assets', "Play1.png")).convert()
		gameTitle = pygame.image.load(os.path.join('assets',"Title.jpg")).convert()
		instructionButton = pygame.image.load(os.path.join('assets', "Instruction.png")).convert()
		quitButton = pygame.image.load(os.path.join('assets', "Quit.jpg")).convert()
		
		self.screen.blit(gameTitle,(0,0))
		self.a = self.screen.blit(playButton,(100,400))
		self.b = self.screen.blit(instructionButton,(500,200))
		self.c = self.screen.blit(quitButton, (900,200))
		pygame.display.flip()
		
		while intro:
			#mouse = pygame.mouse.get_pressed()
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if self.a.collidepoint(pos):  #test if the point(cursor) is inside a rectangle
						#playButton2 = pygame.image.load(os.path.join('assets', "Play2.png")).convert()
						#self.screen.blit(playButton2,(100,400))
						#pygame.display.update()
				#else:
						self.screen.blit(playButton,(100,400))
						pygame.display.update()

				if self.b.collidepoint(pos): 
						#instructionButton2 = pygame.image.load(os.path.join('assets', "Instruction2.png")).convert()
						#self.screen.blit(instructionButton2,(500,200))
						#pygame.display.update()
				#else:
					
						self.screen.blit(instructionButton,(500,200))
						pygame.display.update()
						
				if self.c.collidepoint(pos):  
						#quitButton2 = pygame.image.load(os.path.join('assets', "Quit2.png")).convert()
						#self.screen.blit(quitButton2,(900,200))
						#pygame.display.update()
				#else:
						self.screen.blit(quitButton,(900,200))
						pygame.display.update()
						
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if(self.a.collidepoint(pos)):    
						intro = False    #button == 1 check if left-button pressed
					if(self.b.collidepoint(pos)):
						self.instructionMenu()
					if(self.c.collidepoint(pos)):
						pygame.quit()
						quit()
	def instructionMenu(self):
		self.screen.fill((255,255,255))
		instructionMenu = pygame.image.load(os.path.join('assets', "InstructionMenu.png")).convert()
		returnButton = pygame.image.load(os.path.join('assets', "Quit.jpg")).convert()
		self.screen.blit(instructionMenu,(0,0))
		self.c = self.screen.blit(returnButton, (900,200))
		pygame.display.flip()
		teaching = True
		
		while teaching:
			#mouse = pygame.mouse.get_pressed()
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if self.c.collidepoint(pos):  
					#quitButton2 = pygame.image.load(os.path.join('assets', "Quit2.png")).convert()
					#self.screen.blit(quitButton2,(900,200))
					#pygame.display.update()
				#else:
					self.screen.blit(returnButton,(900,200))
					pygame.display.update()
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.c.collidepoint(pos):
					self.introLoop()
		
	def mainLoop(self):
		pygame.mixer.music.stop()
		pygame.mixer.Sound("../FinalProject/assets/backgroundspy.wav").play()
		#pygame.mixer.music.set_volume(.5)
		#pygame.mixer.music.play(-1)

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
					if event.key == pygame.K_h:
						self.player1.block(event.key)
					if event.key == pygame.K_KP6:
						self.player2.block(event.key)
					if event.key == pygame.K_KP7:    
						self.player2.ultimate(self.screen,self.player1)
					if event.key == pygame.K_j:
						self.player1.ultimate(self.screen,self.player2)
	
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_f or event.key == pygame.K_g: #we cannot spam(keep pressed down) our punches and kickes
						self.player1.fight(event.key, self.player2)
					if event.key == pygame.K_KP4 or event.key == pygame.K_KP5:
						self.player2.fight(event.key, self.player1)
					self.player1.unblock(event.key)
					self.player2.unblock(event.key)
				
				
			if(self.player1.health <= 0):
				self.player1.kill()
				gameOn = False
				print("KO PLAYER1")
			if(self.player2.health <= 0):
				self.player2.kill()
				gameOn = False
				print("KO PLAYER2")
				#self.screen.blit(pygame.font.SysFont("monospace", 15).render("Game Over", 1, (255, 0, 0)), (100, 100))
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.backgroundImage.image, self.backgroundImage.rect)
			self.sprites.draw(self.screen)
			pygame.draw.rect(self.screen, self.player1.healthColor, [10, 10, 4*self.player1.health, 50])   #(Surface, color, Rect, width=0)
			pygame.draw.rect(self.screen, self.player2.healthColor, [1270-(4*self.player2.health), 10, 4*self.player2.health, 50])

			pygame.draw.rect(self.screen, (255,0,0), [10,60,4*self.player1.energyRate,50])  #energy bar
			pygame.draw.rect(self.screen, (255,0,0), [1270-4*self.player2.energyRate,60, 4*self.player2.energyRate,50])
			pygame.display.flip()
			self.clock.tick(60)


def main():

	main_window = Controller()
	pygame.mixer.music.stop()
	main_window.mainLoop()
	pygame.quit()

main()

