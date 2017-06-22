import os, sys, random
import pygame

def load_image(name, colorkey=None):
	fullname = os.path.join('assets', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('Cannot load image:', name)
		raise SystemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)
	return image, image.get_rect()

class Character(pygame.sprite.Sprite):

	def __init__(self, name, x, y, img_file):
		#super().__init__(self)
		self.name = name
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(img_file,-1)
		self.health = 100
		self.speed = 50
		self.rect.x = x
		self.rect.y = y
		self.healthColor = (0,255,0)
		self.jumpSpeed = 100
		self.isJumping = False

	def healthBar(self):
		if self.health <= 75 and self.health >= 30:
			self.healthColor = (255, 255, 0)
		elif self.health < 30: 
			self.healthColor = (255, 0 ,0 )

	def jump(self):
		if(self.isJumping == True):
			self.rect.y -= self.jumpSpeed
			self.isJumping = False
		
	def move(self, direction):
		if(direction == pygame.K_UP or direction == pygame.K_w):
			if(self.rect.y > 10):
				self.isJumping = True
				self.jump()
				
		elif(direction == pygame.K_LEFT or direction == pygame.K_a):
			if(self.rect.x > 50):
				self.rect.x -= self.speed
		elif(direction == pygame.K_RIGHT or direction == pygame.K_d):
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
		elif(direction == pygame.K_DOWN or direction == pygame.K_s):
			self.rect.y += self.speed
			
	
	def fight(self, eventKey, opponent):
		#pygame.key.set_repeat(0,50)
		if (opponent.health > 0 and (eventKey == pygame.K_f or eventKey == pygame.K_KP4)):
			opponent.health -= 10
			print("PUNCH OF DEATH!")
		elif (opponent.health > 0 and (eventKey == pygame.K_g or eventKey == pygame.K_KP5)):
			opponent.health -= 10
			print("KICK OF PAIN!")
		if (eventKey == pygame.K_h or eventKey == pygame.K_KP6):
			self.invincibility = 1
			print("MANLY BLOCK!")
		

	def update(self):
		print("updating position")
