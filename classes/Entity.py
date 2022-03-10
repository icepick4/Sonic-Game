import pygame
pygame.init()

height = pygame.display.get_desktop_sizes()[0][1]
width = pygame.display.get_desktop_sizes()[0][0]
class Entity:
    def __init__(self,rect):
        self.rect = rect
        self.speed = (0,0)
        self.position = self.rect.topleft 
    
    def changeSpeed(self, acceleration):
        speedX, speedY = self.speed
        aX, aY = acceleration
        self.speed = (speedX + aX, speedY + aY)

    def changePosition(self,time):
        speedX, speedY = self.speed
        x,y = self.position
        x -= speedX * time
        y -= speedY * time
        self.position = (x,y)
        self.rect.bottomleft = self.position

    def loop(self):
        x,y = self.position
        w = self.rect.size[0]
        if x + w < 0:
            return True
        return False
        
        
    

