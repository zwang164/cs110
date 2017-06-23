import pygame
import os
import pygame
import os
import sys

class Sprtsheet(pygame.sprite.Sprite):
        def __init__(self, imageFile,width,height):
            pygame.sprite.Sprite.__init__(self)
            #try:
            shittyImage = os.path.join("assets", imageFile)
            self.sprite = pygame.image.load(shittyImage).convert()
            self.width = width    #width of sprite clip
            self.height = height  #height of sprite clip

        #clip a portion of the spritesheet with the rectangle object
        def setImage(self,x_sprite, y_sprite):  #coordinate of sprite clip 
            self.clip_rect = pygame.Rect((x_sprite, y_sprite), (self.width,self.height))
            self.sprite.set_clip(self.clip_rect)   #clip the sprite portion
            sub_surface = self.sprite.subsurface(self.sprite.get_clip())        #get the clip
            self.image = pygame.transform.flip(sub_surface, False, False) #self.image will be called by group######will not flip horizontally and vertically
            self.rect = pygame.Rect(0,0, self.width, self.height) #self.rect will be called by group############location of screen where the clip located
     
def main():
        screen = pygame.display.set_mode((640, 360))
        screen.fill([255,255,255])
        ex = Sprtsheet("Hero.png",100,100)
        ex.setImage(100,100)  #location of a sprite sheet located
        #ex2 = Sprtsheet("Hero.png",30,30)
        sprite_group = pygame.sprite.Group(ex)
        #sprite_group.add(ex2)    
        sprite_group.draw(screen)
        pygame.display.flip()
        
main()

        #error self.spritedict[spr] = surface_blit(spr.image, spr.rect)   so we add self.image and self.rect
        #only problem is the subsurface might out of range
