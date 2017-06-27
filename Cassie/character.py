import os, sys, random
import sprtSheet
import pygame

### Might want to delete this later
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
	return image

class Character(pygame.sprite.Sprite):

	def __init__(self, name, x, y, startFacing):
		#super().__init__(self)
		#super().__init__()
		self.name = name
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_image(img_file,-1)

	### Spritestuff
	## Loads the images and puts them in a list for both
	# the right and left facing frames so we don't have to call flip a bajillion times or something
	## also I used invididual images instead of a sprite sheet because there are only ten images
		self.framesR = []
		self.framesL = []
		for i in range(11):
			string = str(i) + ".png"
			image = load_image(string, -1)
			self.framesR.append(image)
			image = pygame.transform.flip(image, True, False)
			self.framesL.append(image)
	### Put the images into a list, so we can cycle through the animations
	## Also if we need to add more frames we can do it quickly
		self.standingFramesR = [self.framesR[0], self.framesR[1]]
		self.hitFramesR = [self.framesR[2]]
		self.kickFramesR = [self.framesR[3], self.framesR[4]]
		self.punchFramesR = [self.framesR[5], self.framesR[6]]
		self.blockFramesR = [self.framesR[7]]
		self.walkingFramesR = [self.framesR[8], self.framesR[9]]
		self.laserR = [self.framesR[10]]

		self.standingFramesL = [self.framesL[0], self.framesL[1]]
		self.hitFramesL = [self.framesL[2]]
		self.kickFramesL = [self.framesL[3], self.framesL[4]]
		self.punchFramesL = [self.framesL[5], self.framesL[6]]
		self.blockFramesL = [self.framesL[7]]
		self.walkingFramesL = [self.framesL[8], self.framesL[9]]
		self.laserL = [self.framesL[10]]

	### Starting frame and referencing the rect
		self.facing = startFacing
		if self.facing == "Left":
			self.frames = self.standingFramesL
		else:
			self.frames = self.standingFramesR
		self.image = self.frames[0]
		self.rect = self.image.get_rect()
	### Starting position
		self.rect.x = x
		self.rect.y = y
	
	### Finally the stats
		self.health = 100
		self.speed = 50
		self.healthColor = (0,255,0)
		self.comboList = []
		self.timer = pygame.time.Clock()
		self.time = 0
		self.invincibility = False
		self.energyRate = 0

	
	def healthBar(self):
		if self.health <= 75 and self.health >= 30:
			self.healthColor = (255, 255, 0)
		elif self.health < 30: 
			self.healthColor = (255, 0 ,0 )
	
	def move1(self, direction):
		if(direction[pygame.K_a] and self.invincibility == False): #and self.invincibility != True):
			self.facing = "Left"
			if(self.rect.x > 50):
				self.rect.x -= self.speed
				# Cassie's Additions
				self.frames = self.walkingFramesL
				
		if(direction[pygame.K_d] and self.invincibility == False): #and self.invincibility != True):
			self.facing = "Right"
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
				### Cassie's Additions
				self.frames = self.walkingFramesR
			
			
	def move2(self, direction):
		if(direction[pygame.K_LEFT] and self.invincibility == False):
			self.facing = "Left"
			print(self.facing)
			if(self.rect.x > 50):
				self.rect.x -= self.speed
				self.frames = self.walkingFramesL
		if(direction[pygame.K_RIGHT] and self.invincibility == False):
			self.facing = "Right"
			print(self.facing)
			if(self.rect.x < 1280-280):
				self.rect.x += self.speed
				self.frames = self.walkingFramesR	
	
	def block(self, eventKey):
		if (eventKey == pygame.K_h or eventKey == pygame.K_KP6):
			self.invincibility = True

	def unblock(self, eventKey):
		if (eventKey == pygame.K_h or eventKey == pygame.K_KP6):
			self.invincibility = False
			
	def hit(self, opponent, damage, knockback):
		opponent.health -= damage
		if(self.energyRate <100):
			self.energyRate += 10
		if (self.facing == "Left"):
			if(opponent.rect.x > 50):
				opponent.rect.x -= knockback
		if (self.facing == "Right"):
			if(self.rect.x < 1280-280):
				opponent.rect.x += knockback

	def fight(self, fight, opponent):
		print("Invincibility: ", self.invincibility)
		if(self.invincibility == False):
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			if(fight == "punch"):
				#Sound only takes wav files and ogg files
				pygame.mixer.Sound("..assets/punch.wav").play()
				if(self.facing == "Left"):
					self.frames = self.punchFramesL
				if(self.facing == "Right"):
					self.frames = self.punchFramesR
				if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing)):              
					self.hit(opponent, 10, 30)
			if(fight == "kick"):
				#Yeah don't try to play mp4 files
				pygame.mixer.Sound("../Cassie/assets/kick.wav").play()
				if(self.facing == "Left"):
					self.frames = self.kickFramesL
				if(self.facing == "Right"):
					self.frames = self.kickFramesR
				if(fight == "kick" and opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing)):
					self.hit(opponent, 15, 60)

	def ultimate(self,screen,opponent):
		if(self.energyRate == 100):
			pygame.mixer.Sound("..assets/hadouken.wav").play()
			if(self.facing == "Left"):
				image, rect = load_image('10.png')
				pygame.transform.flip(image, True, False)
				self.image, self.rect = image, rect
							
			else:
				self.image, self.rect = load_image('10.png')
			## If you miss this giant laser that's your fault
			if (pygame.sprite.collide_rect(self, opponent)):
				self.hit(opponent, 1000, 500)
			self.energyRate = 0
			

	def update(self):
		###Cassie's Additions
		self.time +=1
		if self.time >= len(self.frames):
			self.time=0
		self.image = self.frames[self.time]

