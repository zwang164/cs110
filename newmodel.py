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

	def healthBar(self):
		if self.playerHealth <= 75 and self.playerHealth >= 30:
			self.playerHealthColor = yellow
		elif self.playerHealth < 30: 
			self.playerHealthColor = red

	def move(self, direction):
		if(direction == pygame.K_UP or direction == pygame.K_w):
			self.rect.y -= self.speed
		elif(direction == pygame.K_LEFT or direction == pygame.K_a):
			if(self.rect.x > 50):
				self.rect.x -= self.speed
		elif(direction == pygame.K_RIGHT or direction == pygame.K_d):
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
		elif(direction == pygame.K_DOWN or direction == pygame.K_s):
			self.rect.y += self.speed
		print(self.rect.x, self.rect.y)

	def fight(self, opponent):
		if(random.randrange(3)):
			self.health -= 1
			print("attack failed")
			return False
		else:
			print("successful attack")
			return True

	def update(self):
		print("updating position")
