import character
import shittyBackground
import ko
import pygame
import random
import os, sys
import sprtSheet

class Controller:

        def __init__(self, width=1280, height=720):
                pygame.init()
                self.width = width
                self.height = height
                self.screen = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption('Kitty Fight')
                self.introLoop()
                self.clock = pygame.time.Clock()
                self.background = pygame.Surface(self.screen.get_size()).convert()
                self.backgroundImage = shittyBackground.fuckingBackground("Epic-Sunset.png", [0,0], (width, height))
                ### Cassie's additions
                self.KO = ko.KO("KOspritesheet.png")
                self.KOsprite = pygame.sprite.Group(self.KO)

                "Load the sprites that we need"""
                self.player1 = character.Character("Skullcrusher", 50, height-370, "spritestrip.png")
                self.player2 = character.Character("Demon Slayer", width-400, height-370, "spritestrip.png")
                self.player1Controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
                self.player2Controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
                
                self.sprites = pygame.sprite.Group((self.player1, self.player2))


        def defButton(self,img,width,height):
                button = pygame.transform.scale(pygame.image.load(os.path.join('assets',img)).convert(),(width,height))    #resize the image(image surface,(width,height))
                colorkey = button.get_at((0,0))
                button.set_colorkey(colorkey)
                return button

        def drawFont(self,text,x,y):
                f = pygame.font.Font(None,50)  #Creates a font object of size 32 using the default font
                for i in range(8):
                        surf = f.render(text, 1, (255,0,255))  #(text,antialis, color,background=None);
                        #antialis: true the characters will have smooth edges; background = none make it transparent
                        self.screen.blit(surf,(x,y))
                return surf
        
        def mouseCollision(self,mouse,img,pos,w,h,x,y):
                if(mouse.collidepoint(pos)):
                        button = self.defButton(img,w,h)
                        self.screen.blit(button,(x,y))
                        pygame.display.update()
                        return True
                return False
            
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
        def instructionMenu(self):
                self.screen.fill((0,0,0))
                instruction1 = self.drawFont("Player1  :  a / d --- move left / move right",200,100)
                instruction2 = self.drawFont("Player1  :  f / g / h / j --- punch / kick / block / ultimate",200,200)
                instruction3 = self.drawFont("Player2  :  leftarrow / rightarrow --- move left / move right",200,300)
                instruction4 = self.drawFont("Player2  :  4 / 5 / 6 / 7 --- punch / kick / block / ultimate",200,400)
                
                
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
                
        def mainLoop(self):
                pygame.mixer.music.stop()
                pygame.mixer.Sound("../Cassie/assets/backgroundspy.wav").play()

        #'''This is the Main Loop of the Game'''
                self.gameOn = True
                pygame.key.set_repeat(1, 1)
                while self.gameOn == True:
                        self.background.fill((250, 250, 250))
                        #This variable is for registering simultaneous inputs
                        # This way, both characters can move at the same time, instead of having
                        # pygame register only one key at a time
                        keys = pygame.key.get_pressed()
                        for event in pygame.event.get():
                                #print(event)
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                                if event.type == pygame.KEYDOWN:
                                        self.player1.move1(keys)
                                        self.player2.move2(keys)
                                        print("Invincibility1: ", self.player1.invincibility)
                                        print("Invincibiliy2: ", self.player2.invincibility)
                                        #Event.type is one input, so you can't block and do other stuff
                                        #We can't put block in our fight function, because our fight function only works once the key is up
                                        #We also can't put it in our move function, because you can move and fight
                                        if event.key == pygame.K_h:
                                                self.player1.block(event.key)
                                        if event.key == pygame.K_KP6:
                                                self.player2.block(event.key)
                                        if event.key == pygame.K_KP7:    
                                                self.player2.ultimate(self.screen,self.player1)
                                        if event.key == pygame.K_j:
                                                self.player1.ultimate(self.screen,self.player2)
        
                                if event.type == pygame.KEYUP:
                                        if event.key == pygame.K_f or event.key == pygame.K_g: #we cannot spam(keep pressed down) our punches and kickes
                                                self.player1.fight("Punch", self.player2)
                                        if event.key == pygame.K_KP4 or event.key == pygame.K_KP5:
                                                self.player2.fight("Kick", self.player1)
                                        self.player1.unblock(event.key)
                                        print("Invincibility1: ", self.player1.invincibility)
                                        self.player2.unblock(event.key)

                        
                        self.gameOver = False   
                        ### Cassie's additions  
                        if(self.player1.health <= 0 or self.player2.health <= 0):
                                print("KO PLAYER1")
                                print(self.player1.health)
                                self.gameOver = True

                                #self.screen.blit(pygame.font.SysFont("monospace", 15).render("Game Over", 1, (255, 0, 0)), (100, 100))
                        self.screen.blit(self.background, (0, 0))
                        self.screen.blit(self.backgroundImage.image, self.backgroundImage.rect)
                        self.sprites.draw(self.screen)
                        pygame.draw.rect(self.screen, self.player1.healthColor, [10, 10, 4*self.player1.health, 50])   #(Surface, color, Rect, width=0)
                        pygame.draw.rect(self.screen, self.player2.healthColor, [1270-(4*self.player2.health), 10, 4*self.player2.health, 50])

                        pygame.draw.rect(self.screen, (255,0,0), [10,60,4*self.player1.energyRate,50])  #energy bar
                        pygame.draw.rect(self.screen, (255,0,0), [1270-4*self.player2.energyRate,60, 4*self.player2.energyRate,50])

                         ##Cassie's Additions
                        self.player1.update()
                        self.player2.update()
                        
                        #####
                        self.endScreen = False
                        self.startOver = False
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
                                print(6)
                                self.screen.blit(self.background, (0, 0))
                                self.screen.blit(self.backgroundImage.image, self.backgroundImage.rect)
                                f = pygame.font.Font(None,50)
                                surf = f.render("Press c to go to main screen or q to quit", 1, (255,0,255)) 
                                collision = self.screen.blit(surf,(300,300))
                                pygame.display.update()
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
                        
                        pygame.display.flip()
                        self.clock.tick(30)
                print(self.startOver)
                return self.startOver


def main():

        main_window = Controller()
        startOver = main_window.mainLoop()
        while(startOver == True):
                main_window = Controller()
                startOver = main_window.mainLoop()
        pygame.quit()

main()


