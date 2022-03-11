import pygame
pygame.init()
from classes.Entity import Entity
from random import randint
height = pygame.display.get_desktop_sizes()[0][1]
width = pygame.display.get_desktop_sizes()[0][0]
class Environment (Entity):
    def __init__(self,rect, surface, type):
        Entity.__init__(self, rect)
        self.surface = surface
        self.type = type
    def loop(self):
        x,y = self.position
        w = self.rect.size[0]
        if x + w < 0:
            return True
        return False
    
    def getRand(self):

        if self.type == "cloud1" or self.type == "palm1":
            self.randX = randint(0,500)
            if self.type == "palm1":
                self.randY = height - 200
            else:
                self.randY = randint(200,height / 2)
        elif self.type == "cloud2" or self.type == "palm2":
            self.randX = randint(1000,2500)
            if self.type == "palm2":
                self.randY = height - 200
            else:
                self.randY = randint(200,height / 2)
        else:
            self.randX = 0
            self.randY = 0
        return self.randX, self.randY
    def animate(self,speedX, speedY, tick, screen):
        self.speed = (speedX,speedY)
        if self.loop():
            if self.type == "grass":
                self.position = (width,height)
            else:
                self.position = (width + self.getRand()[0],self.getRand()[1])
        self.changePosition(tick)
        screen.blit(self.surface,self.rect)
