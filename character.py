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
		if self.facing == "left":
			self.frames = self.standingFramesL
		else:
			self.frames = self.standingFramesR
		self.image = self.frames[0]
		self.rect = self.image.get_rect()
	### Starting position
		self.rect.x = x
		self.rect.y = y
	
	### Finally the stats
		self.health = 250
		self.speed = 50
		self.healthColor = (0,255,0)
		self.comboList = []
		self.timer = pygame.time.Clock()
		self.time = 0
		self.invincibility = False
		self.laser = False
		self.energyRate = 0

	
	def healthBar(self):
		if self.health <= 75 and self.health >= 30:
			self.healthColor = (255, 255, 0)
		elif self.health < 30: 
			self.healthColor = (255, 0 ,0 )
	
	def move1(self, direction):
		if(direction[pygame.K_a] and self.invincibility == False): #and self.invincibility != True):
			self.facing = "left"
			if(self.rect.x > 50):
				self.rect.x -= self.speed
				# Cassie's Additions
				self.frames = self.walkingFramesL
				
		if(direction[pygame.K_d] and self.invincibility == False): #and self.invincibility != True):
			self.facing = "right"
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
				### Cassie's Additions
				self.frames = self.walkingFramesR
			
			
	def move2(self, direction):
		if(direction[pygame.K_LEFT] and self.invincibility == False):
			self.facing = "left"
			print(self.facing)
			if(self.rect.x > 50):
				self.rect.x -= self.speed
				self.frames = self.walkingFramesL
		if(direction[pygame.K_RIGHT] and self.invincibility == False):
			self.facing = "right"
			print(self.facing)
			if(self.rect.x < 1280-280):
				self.rect.x += self.speed
				self.frames = self.walkingFramesR	
	
	def block(self):
		self.invincibility = True
		if(self.facing == "left"):
			self.frames = self.blockFramesL
		if(self.facing == "right"):
			self.frames = self.blockFramesR

	def unblock(self):
		self.invincibility = False
		## End block animation
		if(self.facing == "left"):
			self.frames = self.standingFramesL
		if(self.facing == "right"):
			self.frames = self.standingFramesR

	def hit(self, opponent, damage, knockback):
		opponent.health -= damage
		if(self.energyRate <100 and self.laser == False):
			self.energyRate += 10
		if (self.facing == "left"):
			if(opponent.rect.x > 20):
				opponent.rect.x -= knockback
		if (self.facing == "right"):
			if(opponent.rect.x < 1280-370):
				opponent.rect.x += knockback
		if (opponent.facing == "right"):
			opponent.frames = opponent.hitFramesR
		if (opponent.facing == "left"):
			opponent.frames = opponent.hitFramesL

	def fight(self, fight, opponent):
		print("Invincibility: ", self.invincibility)
		if(self.invincibility == False):
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			if(fight == "punch"):
				#Sound only takes wav files and ogg files
				pygame.mixer.Sound("../Cassie/assets/punch.wav").play()
				if(self.facing == "left"):
					self.frames = self.punchFramesL
				if(self.facing == "right"):
					self.frames = self.punchFramesR
				if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing) and opponent.laser == False):              
					self.hit(opponent, 5, 30)
			if(fight == "kick"):
				#Yeah don't try to play mp4 files
				pygame.mixer.Sound("../Cassie/assets/kick.wav").play()
				if(self.facing == "left"):
					self.frames = self.kickFramesL
				if(self.facing == "right"):
					self.frames = self.kickFramesR
				if(fight == "kick" and opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing) and opponent.laser == False):
					self.hit(opponent, 10, 60)

	def ultimate1(self, opponent, keyPressed):
		if(self.energyRate >= 10 and keyPressed[pygame.K_j]):
			## We need to save the position so that way, when we call the self.rect function
			## it won't go to the top right of the screen
			pygame.mixer.Sound("../Cassie/assets/hadouken.wav").play()
			savePosX = self.rect.x
			savePosY = self.rect.y
			self.laser = True
			self.savePos = self.rect.x
			if(self.facing == "left"):
				savePosX = self.rect.x - 2223 + 350
				self.rect.x = savePosX
				self.frames = self.laserL
				self.image = self.laserL[0]
			if(self.facing == "right"):
				self.frames = self.laserR
				self.image = self.laserR[0]
			self.rect = self.image.get_rect()
			self.rect.x = savePosX
			self.rect.y = savePosY
			## If you miss this giant laser that's your fault
			if (pygame.sprite.collide_rect(self, opponent) and opponent.health > 0):
				self.hit(opponent, 10, 0)
			self.energyRate -= 10

	def ultimate2(self, opponent, keyPressed):
		if(self.energyRate >= 10 and keyPressed[pygame.K_KP7]):
			## We need to save the position so that way, when we call the self.rect function
			## it won't go to the top right of the screen
			pygame.mixer.Sound("../Cassie/assets/hadouken.wav").play()
			savePosX = self.rect.x
			savePosY = self.rect.y
			self.laser = True
			self.savePos = self.rect.x
			if(self.facing == "left"):
				savePosX = self.rect.x - 2223 + 350
				self.rect.x = savePosX
				self.frames = self.laserL
				self.image = self.laserL[0]
			if(self.facing == "right"):
				self.frames = self.laserR
				self.image = self.laserR[0]
			self.rect = self.image.get_rect()
			self.rect.x = savePosX
			self.rect.y = savePosY
			## If you miss this giant laser that's your fault
			if (pygame.sprite.collide_rect(self, opponent) and opponent.health > 0):
                                        self.hit(opponent, 10, 0)
			self.energyRate -= 10

	def update(self):
		self.healthBar()
		if (self.laser == True):
			if(self.facing == "left"):
				#Since pygame interprets image position based on the top left pixel,
				# we need to move the cat's posiition so when the laser is replaced with a new image
				# the cat won't be off screen
				self.frames = self.standingFramesL
				self.image = self.frames[0]
				self.rect.x = self.savePos
			if(self.facing == "right"):
				self.frames = self.standingFramesR
		else:	
			self.time +=1
			savePosX = self.rect.x
			savePosY = self.rect.y
			if(self.time >= 20):
				self.time=0
			if(self.time <= 10):
				self.image = self.frames[0]
			if(self.time > 10 and len(self.frames)>1):
				self.image = self.frames[1]
			self.rect = self.image.get_rect()
			self.rect.x = savePosX
			self.rect.y = savePosY

