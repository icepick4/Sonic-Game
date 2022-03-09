from classes.Entity import Entity
import pygame
pygame.init()

height = pygame.display.get_desktop_sizes()[0][1]

class Sonic(Entity):
    def __init__(self, rect):
        Entity.__init__(self, rect)
        self.hp = 3

    def sonicPosRestriction(self,zone):
        x,y = self.position
        h = self.rect.size[1]
        if y + h > zone.bottom:
            y = zone.bottom - h
            self.speed = (0,0)
        if y < zone.top:
            y = zone.top
        self.position = (x,y)
        self.rect.topleft = self.position
    
    def onFloor(self):
        return self.position[1] == height - 200 - 144