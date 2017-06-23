import pygame
import os
import pygame

class Sprtsheet(pygame.sprite.Sprite):
        def __init__(self, imageFile, width, height):
            pygame.sprite.Sprite.__init__(self)
            #try:
            shittyImage = os.path.join("assets", imageFile)
            self.sprite = pygame.image.load(shittyImage).convert()
            self.width = width    #width of sprite clip
            self.height = height  #height of sprite clip

        #clip a portion of the spritesheet with the rectangle object
        def setImage(self,char_x, char_y, x_sprite, y_sprite):  
            self.clip_rect = pygame.Rect((x_sprite, y_sprite), (self.width,self.height)) # coordinate of sprite clip and its dimension
            self.sprite.set_clip(self.clip_rect)   #clip the sprite portion
            sub_surface = self.sprite.subsurface(self.sprite.get_clip())        #get the clip
            self.image = pygame.transform.flip(sub_surface, False, False) #self.image will be called by group######will not flip horizontally and vertically
            self.rect = pygame.Rect(char_x, char_y, self.width, self.height) #self.rect will be called by group############location of character where the clip will locate
     
def main():
        #waring : testing only
        screen = pygame.display.set_mode((640, 360))
        screen.fill([255,255,255])
        #location of chararacter
        x = 0
        y = 0   
        #location of sprite clip
        x2 = 0
        y2 = 0
        for row in range(5):
                for col in range(5):
                        ex = Sprtsheet("Hero.png",50,50)
                        ex.setImage(x,y,x2,y2)  #locates a sprite clip and situates it at character's location
                        #ex2 = Sprtsheet("Hero.png",30,30)
                        sprite_group = pygame.sprite.Group(ex)
                        #sprite_group.add(ex2)    
                        sprite_group.draw(screen)
                        pygame.display.flip()
                        x += 50
                        x2 += 50
                x = 0   #want next row start at (0,50) and so on
                y += 50
                x2 = 0   #same for sprite sheet
                y2 += 50
                
        
main()

        #error self.spritedict[spr] = surface_blit(spr.image, spr.rect)   so we add self.image and self.rect
        #only problem is the subsurface might out of range
