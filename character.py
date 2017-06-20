import pygame
import sys

def load_image(pname,ptype):
	fullname = os.path.join('assets',pname)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('cannot load image: ', pname)

	image = image.convert()
		
	return image,image.get_rect()



class Characters:
	def __init__(self, pname, ptype, px,py, defaultImage,actionImages):
		pygame.sprite.Sprite.__init__(self):
		self.screen = pygame.display.setMode(1920,1080) #Game Resolution
		self.display = pygame.display.setCaption("Title: ") #Game title
		self.FPS = 24 #Frames per second
		self.name = pname # Character Name
		self.type = ptype # Character Type

		self.image, self.rect = load_image(img_file,"chicken") 
		

		self.rect.x = px	#position move back when punched/kicked
		self.rect.y = py
		self.speed = 2

		self.defaultImage = defaultImage	
		self.actionImages = actionImages
		self.playerHealth = 100
		self.playerHealthColor = green



	def move(self, direction):
		if direction == pygame.K_LEFT or direction == pygame.K_a:
			self.rect.x -= self.speed
		elif direction == pygame.K_RIGHT or direction == pygame.K_d:
			self.rect.x += self.speed

	
	def damage(self, damage):
		self.health -= damage		
	
	
	def healthBar(self):
		
		if self.playerHealth <= 75 and self.playerHealth >= 30:
			self.playerHealthColor = yellow
		elif self.playerHealth < 30: 
			self.playerHealthColor = red
		
	

		pygame.draw.rect(gameDisplay, player1HealthColor, (680, 25, playerHealth, 25)) #health bar's rectangle
		pygame.draw.rect(gameDisplay, player2HealthColor, (20, 25, player2Health, 25)) #(screen, color, (x, y, width, height))

	
	def fight(self):
		if(direction == K_j or direction == K_KP4):
		self.currentImage = self.actionImage["punch"] #image for punch
		self.vx = 0 #initial velocity for punch
		#self.vy = 0

		elif(direction == K_k or direction == K_KP5):
		self.currentImage = self.actionImage["kick"] #image for kick
		self.vx = 0 #initial velocity for kick
		#self.vy = 0
		
		elif(direction == K_l or direction == K_KP6):
		self.currentImage = self.actionImage["block"] #image for block




