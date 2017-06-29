import character
import shittyBackground
import ko
import pygame
import os, sys
import json

class Controller:

	def __init__(self, width=1280, height=720):
		''' Initializes the screen and the introloop'''
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Kitty Fight')
		self.introLoop()
		'''Sets the clock so we can control the frame rate later'''
		self.clock = pygame.time.Clock()
		'''Did we check the high score yet? No we didn't, we just started!'''
		self.weCheckedHighScore = False
		'''Loads our AMAZING, NOT SHIT backgrounds'''
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.backgroundImage = shittyBackground.fuckingBackground("Epic-Sunset.png", [0,0], (width, height))

		'''This loads the KO animation we'll play later and groups it with itself so we can draw it later.'''
		self.KO = ko.KO("KOspritesheet.png")
		self.KOsprite = pygame.sprite.Group(self.KO)

		'''This load both of the players'''
		self.player1 = character.Character("Skullcrusher", 50, height-370,"right")
		self.player2 = character.Character("Demon Slayer", width-400, height-370, "left")
		self.sprites = pygame.sprite.Group((self.player1, self.player2))

	'''Allows us to create buttons'''
	def defButton(self,img,width,height):
		button = pygame.transform.scale(pygame.image.load(os.path.join('assets',img)).convert(),(width,height))    #resize the image(image surface,(width,height))
		colorkey = button.get_at((0,0))
		button.set_colorkey(colorkey)
		return button
	'''Call this to create text to draw to the screen'''
	def drawFont(self,text,x,y):
		f = pygame.font.Font(None,50)  #Creates a font object of size 32 using the default font
		for i in range(8):
			surf = f.render(text, 1, (255,0,255))  #(text,antialis, color,background=None);
			#antialis: true the characters will have smooth edges; background = none make it transparent
			self.screen.blit(surf,(x,y))
		return surf

	'''IF we want mouseover animations for our buttons, we call this function'''
	def mouseCollision(self,mouse,img,pos,w,h,x,y):
		if(mouse.collidepoint(pos)):
			button = self.defButton(img,w,h)
			self.screen.blit(button,(x,y))
			pygame.display.update()
			return True
		return False

	'''Starts the introscreen, loads the music, and loads the titlescreen and start, instructions,
	and quite menu.'''
	def introLoop(self):
		self.intro = True
		self.gameOver = False
		self.screen.fill((0,0,0))
		pygame.mixer.music.load("../Cassie/assets/tekken.mp3")
		pygame.mixer.music.set_volume(.5)
		pygame.mixer.music.play(-1)
		
		gameTitle = self.defButton("Title.png",700,400)
		
		playButton = self.defButton("Play.png",300,150)
		instructionButton = self.defButton("Instruction.png",300,150)
		quitButton = self.defButton("Quit.png",300,140)
		
		
		self.screen.blit(gameTitle,(300,0))
		self.mouse1 = self.screen.blit(playButton,(100,500))
		self.mouse2 = self.screen.blit(instructionButton,(500,500))
		self.mouse3 = self.screen.blit(quitButton, (900,500))
		pygame.display.flip()
		'''This is how we navigate the startscreen. If the player mouses over or clicks certain buttons,
		new things occur.'''
		while self.intro == True:
			#mouse = pygame.mouse.get_pressed()
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if self.mouseCollision(self.mouse1,"Play2.png",pos,300,150,100,500) != True:
						self.screen.blit(playButton,(100,500))
						pygame.display.update()
						
				if self.mouseCollision(self.mouse2,"Instruction2.png",pos,300,150,500,500) != True:
						self.screen.blit(instructionButton,(500,500))
						pygame.display.update()
						
				if self.mouseCollision(self.mouse3,"Quit2.png",pos,300,150,900,500) != True:
						self.screen.blit(quitButton,(900,500))
						pygame.display.update()
						
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if(self.mouse1.collidepoint(pos)):    
						self.intro = False #button == 1 check if left-button pressed
						break
					elif(self.mouse2.collidepoint(pos)):
						self.instructionMenu()
					elif(self.mouse3.collidepoint(pos)):
						pygame.quit()
						quit()

	'''This is what our instructions menu looks like.'''
	def instructionMenu(self):
		self.screen.fill((0,0,0))
		instruction1 = self.drawFont("Player1  :  a / d --- move left / move right",200,50)
		instruction2 = self.drawFont("Player1  :  f / g / h / j --- punch / kick / block / ultimate",200,100)
		instruction3 = self.drawFont("Player2  :  leftarrow / rightarrow --- move left / move right",200,150)
		instruction4 = self.drawFont("Player2  :  KP4 / KP5 / KP6 / KP7 --- punch / kick / block / ultimate",200,200)
		instruction5 = self.drawFont("Build up SP by fighting and hold down j or KP7 to fire laser!", 200, 250)
		
		
		returnButton = self.defButton("Return.png",150,150)
		self.mouse4 = self.screen.blit(returnButton, (550,500))
		pygame.display.flip()
		teaching = True
		
		while teaching:
			#mouse = pygame.mouse.get_pressed()
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if self.mouseCollision(self.mouse4,"Return2.png",pos,150,150,550,500) != True:
						self.screen.blit(returnButton,(550,500))
						pygame.display.update()
			
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mouse4.collidepoint(pos):
					self.introLoop()
					teaching = False

	'''This is where the main game occurs. This is where we get all of our badass action. Also, new music'''	
	def mainLoop(self):
		pygame.mixer.music.stop()
		pygame.mixer.Sound("../Cassie/assets/backgroundspy.wav").play()
		self.gameOn = True
		pygame.key.set_repeat(1, 1)
		while self.gameOn == True:
			self.background.fill((250, 250, 250))

			'''This variable is for registering simultaneous inputs
			This way, both characters can move at the same time, instead of having
			pygame register only one key at a time'''
			keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					'''Only chickens quit now!'''
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					self.player1.move1(keys)
					self.player2.move2(keys)
					'''Player is invincible while using ultimate'''
					self.player1.ultimate1(self.player2, keys)
					self.player2.ultimate2(self.player1, keys)
					'''Event.type is one input, so you can't block and do other stuff
					We can't put block in our fight function, because we want to hold down block but
					we don't wanna spam fight. We also can't put it in our move function, because you can kinda
					spazz move and fight and we want people to use strategy when they block.'''
					if event.key == pygame.K_h:
						self.player1.block()
					if event.key == pygame.K_KP6:
						self.player2.block()

				'''The fight function is only execute when the key goes up, so you can't hold down fight and spam punches.
				As soon as you lift the ultimate key or the block key, the character stops their ultimate or stops blocking.'''
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_f:
						self.player1.fight("punch", self.player2)
					if event.key == pygame.K_g: 
						self.player1.fight("kick", self.player2)
					if event.key == pygame.K_KP4:
						self.player2.fight("punch", self.player1)
					if event.key == pygame.K_KP5:
						self.player2.fight("kick", self.player1)
					if event.key == pygame.K_h:
						self.player1.unblock()
					if event.key == pygame.K_KP6:
						self.player2.unblock()
					if event.key == pygame.K_KP7:
						self.player2.laser = False
					if event.key == pygame.K_j:
						self.player1.laser = False

			
			self.gameOver = False

			'''If a player dies, it's game over! Score is added to to winner based on how much health they have left.'''
			if(self.player1.health <= 0):
				self.player2.score += self.player2.health * 1.5 ## Add health bonus to the score once
				self.gameOver = True
			elif(self.player2.health <= 0):
				print("KO PLAYER1")
				print(self.player1.health)
				self.player1.score += self.player1.health * 1.5 ## Add health bonus to the score once
				self.gameOver = True

			'''This is where we finally draw everything down and call our update function to update the player.'''
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.backgroundImage.image, self.backgroundImage.rect)
			self.sprites.draw(self.screen)
			pygame.draw.rect(self.screen, self.player1.healthColor, [10, 10, 2*self.player1.health, 50])   #(Surface, color, Rect, width=0)
			pygame.draw.rect(self.screen, self.player2.healthColor, [1270-(2*self.player2.health), 10, 2*self.player2.health, 50])

			pygame.draw.rect(self.screen, (238,130,238), [10,60,4*self.player1.energyRate,50])  #energy bar
			pygame.draw.rect(self.screen, (238,130,238), [1270-4*self.player2.energyRate,60, 4*self.player2.energyRate,50])

			self.player1.update()
			self.player2.update()
			
			self.endScreen = False
			self.startOver = False

			'''When the game ends, run the KO animation'''
			if self.gameOver == True:
				self.KOsprite.draw(self.screen)
				self.KO.update()
				print(self.KO.index)
				print(len(self.KO.anim.frames))
				pygame.mixer.Sound("../Cassie/assets/KO.wav").play()
				if self.KO.index  >= len(self.KO.anim.frames)-1:
					pygame.time.delay(2000)
					self.endScreen = True
					self.gameOver = False   #so can go to ending screen
			while self.endScreen == True:
				'''Shows a victory screen based on who won'''
				self.screen.fill((0,0,0))
				if(self.player1.health <= 0):
					player2Sign = self.defButton("Player2.png",300,150)  #resize the player sign
					self.screen.blit(player2Sign,(500,100))
					'''Saves Score'''
					self.playerScore = self.player2.score
				else:
					player1Sign = self.defButton("Player1.png",300,150)
					self.playerScore = self.player1.score
					self.screen.blit(player1Sign,(500,100))
				victorySign = self.defButton("Victory.png",500,250)
				self.screen.blit(victorySign,(400,250))
				f = pygame.font.Font(None,50)
				surf = f.render("Press c to go to main screen or q to quit", 1, (255,0,255)) 
				collision = self.screen.blit(surf,(350,500))

				'''Display Player's Score'''
				playerScoreText = f.render("Player's Score: " + str(self.playerScore), 1, (255, 0, 255))
				self.screen.blit(playerScoreText, (350, 550))

				'''Loads the highscores list'''
				with open('highScores.json') as jsonFile:  
					data = json.load(jsonFile)

				'''Checks to see if player made the leaderboards'''
				if self.weCheckedHighScore == False: #So that way we don't spam this loop
					for i in range(len(data)):
						if self.playerScore > data[i]:
							data.insert(i, self.playerScore)
							self.weCheckedHighScore = True 
							break #This breaks out of the for loop, but not the overall loop
				with open('highScores.json', 'w') as outfile:  
					json.dump(data[0:5], outfile)
				
				scoreString = ""
				for i in range(len(data)):
					scoreString += str(data[i]) + ", "
				highScoreText = f.render("Highscores: " + scoreString, 1, (255, 0, 255))
				self.screen.blit(highScoreText, (350, 600))
				pygame.display.update()

				'''The player can now quit without their chicken status being called into question. They have proved themselves.
				Or they can prove themselves even more by continuing the match.'''
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						quit()
					if event.type == pygame.KEYUP:
						if(event.key == pygame.K_c):
							self.startOver = True
							self.endScreen = False
							self.gameOn = False
							break
						if(event.key == pygame.K_q):
							pygame.quit()
							quit()
			'''Refreshes the screen and sets the frame rate'''
			pygame.display.flip()
			self.clock.tick(30)
		return self.startOver


def main():

	'''And it's all executed here! Wow!'''
	main_window = Controller()
	startOver = main_window.mainLoop()
	while(startOver == True):
		main_window = Controller()
		startOver = main_window.mainLoop()
	pygame.quit()

main()


