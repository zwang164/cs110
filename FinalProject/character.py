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
	return image, image.get_rect()

class Character(pygame.sprite.Sprite):

	def __init__(self, name, x, y, img_file):
		#super().__init__(self)
		#super().__init__()
		self.name = name
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_image(img_file,-1)
	### SPRITESHEET STUFF
		spriteSheet = sprtSheet.SpriteSheet(img_file)
	### Spritesheet walking list
		self.walkingFramesL = []
		self.walkingFramesR = []
	### Puts each individual spritesheet frame into a list
		image = spriteSheet.getImage(0, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(256, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(521, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(786, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(1024, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(1280, 0, 256, 256)
		self.walkingFramesR.append(image)
		image = spriteSheet.getImage(1536, 0, 256, 256)
		self.walkingFramesR.append(image)
		
	### HOLY SHIT THIS ONE'S FACEIN LEFT DIDN'T EVEN KNOW YOU COULD FLIP IMAGES LIKE THAT
		image = spriteSheet.getImage(0, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)  #flip horizontally not vertically
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(256, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(521, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(786, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(1024, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(1280, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
		image = spriteSheet.getImage(1536, 0, 256, 256)
		image = pygame.transform.flip(image, True, False)
		self.walkingFramesL.append(image)
	
		
	### Starting frame and referencing the rect
		### Cassie's Additions
		self.frames = self.walkingFramesR
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
		#Might remove this l8
		self.timer = pygame.time.Clock()
		### Cassie's addition
		self.time = 0
		###
		self.invincibility = False
		self.energyRate = 0
		self.facing = "None"
	
	#laser
		laserImage = sprtSheet.SpriteSheet("Laser.png")
		#self.laserClip =[]
		self.laserClip = laserImage.getImage(0, 230, 100, 100)
		#self.laserClip.append(laserImage.getImage(0, 230, 100, 100))
		#self.laserClip.append(laserImage.getImage(100, 230, 100, 100))
		#self.laserClip.append(laserImage.getImage(200, 230, 100, 100))
		#self.laserClip.append(laserImage.getImage(300, 230, 100, 100))
		#self.laserClip.append(laserImage.getImage(400, 230, 100, 100))
		self.laserRect = self.laserClip.get_rect()
		
	
	def ultimate(self,screen,opponent):
		if(self.energyRate == 100):
			if(self.facing == "Left"):
				print(1)
				#self.laserRect.x += self.speed
				#self.rect.x += self.speed
				self.laser_x = self.rect.x-100   #to look smoothier
				self.laser_y = self.rect.y+100
				for i in range(10):
					pygame.time.delay(10)
					self.bs = screen.blit(self.laserClip, (self.laser_x,self.laser_y))
					#we can do self.image = "imageplusbeam shooting out in a single image
					if(self.bs.colliderect(opponent.rect)):
						opponent.health -= 5
						if(opponent.rect.x > 50):     #not outside of screen
							opponent.rect.x -= 50
						   
					pygame.display.flip()
					self.laser_x -= 100
							
			else:
				self.laser_x = self.rect.x+100   #to look smoothier
				self.laser_y = self.rect.y+100
				for i in range(10):
					pygame.time.delay(10)
					self.bs = screen.blit(self.laserClip, (self.laser_x,self.laser_y))
					#we can do self.image = "image-plus-beam" shooting out in a single image
					if(self.bs.colliderect(opponent.rect)):
						opponent.health -=5
						if(opponent.rect.x < 1280-280):  
							opponent.rect.x += 50
						  
					pygame.display.flip()
					self.laser_x += 100
			
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
		if (self.facing == "Left"):
			if(opponent.rect.x > 50):
				opponent.rect.x -= knockback
		if (self.facing == "Right"):
			if(self.rect.x < 1280-280):
				opponent.rect.x += knockback

	def fight(self, eventKey, opponent):
		print("Invincibility: ", self.invincibility)
		if(self.invincibility == False):
			if(self.energyRate <100):
				self.energyRate += 10
			#Run the punch animation even if you're nowhere close to other player
			# as if you're some kind of twat who spams attacks
			if(opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing)):              
				self.hit(opponent, 10, 20)
		if(self.invincibility == False):
			if(self.energyRate <100):
				self.energyRate += 10
			#Run the kick animation even without collision
			# because you could be stupid and miss your kick
			if (opponent.health > 0 and pygame.sprite.collide_rect(self, opponent) and (opponent.invincibility == False or self.facing == opponent.facing)):
				self.hit(opponent, 10, 20)

	def update(self):
		###Cassie's Additions
		self.time +=1
		if self.time >= len(self.frames):
			self.time=0
		self.image = self.frames[self.time]

