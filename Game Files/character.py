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
		self.comboList = []
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
		if(direction[pygame.K_UP] or direction[pygame.K_w]):
			if(self.rect.y > 10):
				self.isJumping = True
				self.jump()
		if(direction[pygame.K_DOWN] or direction[pygame.K_s]):
				self.rect.y += self.speed
		if(direction[pygame.K_LEFT] or direction[pygame.K_a]):
			if(self.rect.x > 50):
				self.rect.x -= self.speed
		if(direction[pygame.K_RIGHT] or direction[pygame.K_d]):
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
	##Delete these l8
	def move1(self, direction):
		if(direction[pygame.K_w]):
			if(self.rect.y > 10):
				self.isJumping = True
				self.jump()
		if(direction[pygame.K_s]):
			self.rect.y += self.speed
		if(direction[pygame.K_a]):
			if(self.rect.x > 50):
				self.rect.x -= self.speed
		if(direction[pygame.K_d]):
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
		#You can move in all directions at once, but you can't move and block
		#elif(direction[pygame.K_h]):
		#        self.invincibility = 1
		#        print("MANLY BLOCK!")
			
			

	def move2(self, direction):
		self.invincibility = 0
		print("Invincibility: ", self.invincibility)
		if(direction[pygame.K_UP]):
			if(self.rect.y > 10):
				self.isJumping = True
				self.jump()
		if(direction[pygame.K_DOWN]):
			self.rect.y += self.speed
		if(direction[pygame.K_LEFT]):
			self.facing = "Left"
			if(self.rect.x > 50):
				self.rect.x -= self.speed
		if(direction[pygame.K_RIGHT]):
			self.facing = "Right"
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
		#You can move in all directions at once, but you can't move AND block
		#elif(direction[pygame.K_KP6]):
		#        self.invincibility = 1
		#        print("MANLY BLOCK!")
			
	def block0(self, eventKey):
		if (eventKey[pygame.K_h] or eventKey[pygame.K_KP6]):
			self.invincibility = 1
			print("MANLY BLOCK")
	#DELETE DELETE
	def block(self, eventKey):
		if (eventKey == pygame.K_h or eventKey == pygame.K_KP6):
			self.invincibility = 1
			print("Invincibility: ", self.invincibility)
	def block1(self, eventKey):
		if (eventKey == pygame.K_h):
			self.invincibility = 1
			print("Invincibility: ", self.invincibility)
	def block2(self, eventKey):
		if (eventKey == pygame.K_KP6):
			self.invincibility = 1
			print("Invincibility: ", self.invincibility)

	def hit(self, opponent, damage, knockback):
		opponent.health -= damage
		if (self.direction == "Left"):
			opponent.rect.x -= knockback
		if (self.direction == "Right"):
			opponent.rect.x += knockback

	def fight(self, eventKey, opponent):
		self.invincibility = 0
		print("Invincibility: ", self.invincibility)
		if(eventKey == pygame.K_f or eventKey == pygame.K_KP4):
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			print("PUNCH OF DEATH!")
			if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):              
				self.hit(opponent, 10, 20)
		if(eventKey == pygame.K_g or eventKey == pygame.K_KP5):
			#Run the kick animation even without collision
			# because you could be stupid and miss your kick
			print("KICK OF DOOM!")
			if (opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):
				self.hit(opponent, 10, 200)

	#Delete this dumbass shit l8
	def fight1(self, eventKey, opponent):
		if(eventKey == pygame.K_f):
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			print("PUNCH OF DEATH!")
			if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):              
				opponent.health -= 10
		if(eventKey == pygame.K_g):
			#Run the kick animation even without collision
			# because you could be stupid and miss your kick
			print("KICK OF DOOM!")
			if (opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):
				opponent.health -= 10
		opponent.healthBar()
		
	def fight2(self, eventKey, opponent):
		if(eventKey == pygame.K_KP4):
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			print("PUNCH OF DEEEAAAATH!")
			if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):              
				opponent.health -= 10
		if(eventKey == pygame.K_KP5):
			#Run the kick animation even without collision
			# because you could be stupid and miss your kick
			print("KICK OF DOOOOOOOOOM!")
			if (opponent.health > 0 and pygame.sprite.collide_rect(self, opponent)):
				opponent.health -= 10
		opponent.healthBar()


	def update(self):
		print("updating position")
