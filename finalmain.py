import character
import pygame
import sys


class Controller:
	def __init__(self, width=640, height=480):
        	pygame.init()
        	self.width = width
        	self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.character1 = character.Charcter()
		self.character2 = character.Charcter()
		self.sprites = pygame.sprite.RenderPlain((self.hero,)+tuple(self.enemies))


	def gameIntro(): # Intro Screen
		intro = True
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit():  #uninitialize all pygame modules
					quit()	#close program?
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE: #Press space to play
						intro = Falsel
					elif event.key == pygame.K_q: #Press q to quit
						pygame.quit()
						quit()
		gameDisplay.fill(#image)
		messageToScreen("WELCOME!", red) # Intro message


	def mainLoop():
		pygame.key.set_repeat(1,50)
		while True:
			self.background.fill((250, 250, 250))
			for event in pygame.event.get():
		
				if event.type == pygame.Quit:
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_a or event.key == pygame.K_LEFT:
						self.character.move = -5
					elif event.key == pygame.K_d or event.key ==pygame.K_RIGHT:
						self.character.move = 5	
					elif event.key == pygame.K_p:
						pause()
					elif event.key == pygame.K_j or event.key == pygame.K_4 :	#punch
						if(pygame.sprite.collide_rect(self.character1, self.character2)
						playerdamage = 5
					elif event.key == pygame.K_k or event.key == pygame.K_5:		#kick
						if(pygame.sprite.collide_rect(self.character1, self.character2)
						playerdamage = 5
		
		self.screen.blit(self.background, (0, 0))
            	self.sprites.draw(self.screen)
		

		pygame.draw.rect(gameDisplay, player1HealthColor, (680, 25, playerHealth, 25)) #health bar's rectangle
		pygame.draw.rect(gameDisplay, player2HealthColor, (20, 25, player2Health, 25)) #(screen, color, (x, y, width, height))

		pygame.display.update()

def main():
	mainWindow = Controller()
	mainWindow.mainLoop()

main()
