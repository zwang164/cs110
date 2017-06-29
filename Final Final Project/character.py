import os, sys, random
import pygame

''' This loads an image from the assets folder, converts the image, sets the top
left pixel to be the transparent color, and then returns the image.
In pygame transparancy is loaded all wonky, so we need to set the top left
pixel as transparent. '''
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

''' Our character class creates our character sprites with stats.'''
class Character(pygame.sprite.Sprite):

	''' The initiallizer takes the character's name, starting x and y positions,
	and the direction the sprite first faces, so we can load two players
	and have them stare each other down.'''
	def __init__(self, name, x, y, startFacing):
		self.name = name
		pygame.sprite.Sprite.__init__(self)

		''' Loads the images and puts them in a list for both
		the right and left facing frames so we don't have to call flip a bajillion times or something.
		We used invididual images instead of a sprite sheet because there are only like ten images,
		so we don't need to overcomplicate things.'''
		self.framesR = []
		self.framesL = []
		for i in range(11):
			string = str(i) + ".png"
			image = load_image(string, -1)
			self.framesR.append(image)
			image = pygame.transform.flip(image, True, False)
			self.framesL.append(image)

		'''Put the images into a list, so we can cycle through the animations
		Also if we need to add more frames we can do it quickly'''
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

		'''Starting frame and referencing the rect'''
		self.facing = startFacing
		if self.facing == "left":
			self.frames = self.standingFramesL
		else:
			self.frames = self.standingFramesR
		self.image = self.frames[0]
		self.rect = self.image.get_rect()

		'''Set the starting position'''
		self.rect.x = x
		self.rect.y = y
	
		'''NOW we set the player's stats '''
		self.health = 250
		self.speed = 50
		self.healthColor = (0,255,0)
		self.comboList = []
		self.timer = pygame.time.Clock()
		self.time = 0
		self.invincibility = False
		self.laser = False
		self.energyRate = 0
		self.score = 0

	'''The healthBar function checks to see where the player's health is, then sets the player's health color
	depending on how low their health is. We'll call this function in the update() later.'''
	def healthBar(self):
		if self.health <= 75 and self.health >= 30:
			self.healthColor = (255, 255, 0)
		elif self.health < 30: 
			self.healthColor = (255, 0 ,0 )
	''' The move function checks to see what key is pressed, and if the keys a and d are pressed,
	it moves left and right. It also changes the frames list to cycle through, so when we call our update()
	function, it'll cycle through those frames. We'll call this function in the main for player1.'''
	def move1(self, direction):
		if(direction[pygame.K_a] and self.invincibility == False):
			'''The move key also sets the direction the character is facing. This is important for setting
			out animations both here and throughout our code.'''
			self.facing = "left"
			if(self.rect.x > 50):
				self.rect.x -= self.speed
				self.frames = self.walkingFramesL				
		if(direction[pygame.K_d] and self.invincibility == False):
			self.facing = "right"
			if(self.rect.x < 1280-318):
				self.rect.x += self.speed
				self.frames = self.walkingFramesR
			
	''' This is the same as the move1 fuction, but we call this for player two. We need to seperate these
	functions for each player, so that way the main can check to see if both players are pressing keys and
	thus allow both players to move simulatneously, and makes sure their specific key inputs only moves their own character.'''		
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

	''' The block functions sets the player's state to invincible. When we call the fight function, the fight function
	only passes the damage function if the player is not invincible.'''
	def block(self):
		self.invincibility = True
		if(self.facing == "left"):
			self.frames = self.blockFramesL
		if(self.facing == "right"):
			self.frames = self.blockFramesR

	'''In our main, as soon as the player stops blocking, the invincibility is set to false and the frames are rest.'''
	def unblock(self):
		self.invincibility = False
		## End block animation
		if(self.facing == "left"):
			self.frames = self.standingFramesL
		if(self.facing == "right"):
			self.frames = self.standingFramesR

	'''The hit function takes the sprite's self, the opponent, damage, knockback, and addedScore variables to do
	each of those respectfully. Damage takes away opponent's health, knockback pushes the opponent back based
	on the direction that the character is facing, and addedScore adds to the player's score, and SP is added based on
	damage dealt, but if you're using your ULTIMATE ATTACK, you can only lose SP and not gain it.
	When the opponent is hit, this changes the opponent's frames to cycle through the hit frames, so the cats have
	this cute little 'Noooo I'm being hit' face.'''
	def hit(self, opponent, damage, knockback, addedScore):
		opponent.health -= damage
		self.score += addedScore
		if(self.energyRate <100 and self.laser == False):
			self.energyRate += damage
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

	'''Fight takes both the player and the opponent, and the type of fight, such as whether the player executed a punch or
	a kick. Depending on whether the player either punched or kicked, a different sound is played, and the hit function is passed
	with a different ammount of damage, knockback, and score. Kicks do more damage than punches but they have a much larger knockback,
	risking pushing the opponent out of the player's range. If the opponent is invincible, the hit function is not passed.
	However, if the player runs behind the opponent and hits from behind, the opponent's block is negated. This is
	how we encourage strategy.'''
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
					self.hit(opponent, 5, 30, 500)
			if(fight == "kick"):
				#Yeah don't try to play mp4 files
				pygame.mixer.Sound("../Cassie/assets/kick.wav").play()
				if(self.facing == "left"):
					self.frames = self.kickFramesL
				if(self.facing == "right"):
					self.frames = self.kickFramesR
				if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing) and opponent.laser == False):
					self.hit(opponent, 10, 60, 1000)
	''' The ultimate attack takes the opponent and the keyPressed. If the player has charged up enough SP from fighting,
	they can fire their laser! This replaces the cat's frames with their laser frames and decreases their SP and deals damage based on how
	long the player keeps the key pressed.'''
	def ultimate1(self, opponent, keyPressed):
		if(self.energyRate >= 10 and keyPressed[pygame.K_j]):
			'''We need to save the position so that way, when we call the self.rect function
			the cat won't teleport to the top right of the screen as the self.rect resets the position.'''
			pygame.mixer.Sound("../Cassie/assets/hadouken.wav").play()
			savePosX = self.rect.x
			savePosY = self.rect.y
			self.laser = True
			self.savePos = self.rect.x
			'''We need to modified the saved position because pygame interprets the image position based on the top left corner of the image.
			Since the cat frames include both the cat and the laser, and the laser image has this ridiculously large width,
			if we don't modify the saved position, the the cat will be pushed off screen and the top left corner of the end of the laser
			will take the place of the cat.'''
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
				self.hit(opponent, 10, 0, 1500)
			self.energyRate -= 10

	''' The ultimate functions are seperated for the same reason that the move functions are seperated for each player.'''
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
					self.hit(opponent, 10, 0, 150)
			self.energyRate -= 10

	'''This updates our player's frame and the rect. Since the laser needs to be updated a little differently based
	on the laser's image width, that's a seperated within the update. This function updates the cat based on the
	game's frame rate. We initiallized a time at 0 in the beginning so that way, whenever we update this function,
	it adds to that time and changes the cat's image based on the current frame list it's cycling through.'''
	def update(self):
		self.healthBar()
		if (self.laser == True):
			if(self.facing == "left"):
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

