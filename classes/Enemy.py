from classes.Entity import Entity
from random import randint, choice
from time import time
from functions import animateGif
class Enemy(Entity):
    def __init__(self, rect, surface, type):
        Entity.__init__(self, rect)
        self.type = type 
        self.surface = surface

    def enemyRestriction(self):
        x,y = self.position
        w = self.rect.size[0]
        if self.type == "grass":
            if x + w < 0:
                return True
        else:
            if x + w < 0:
                return True
        return False
    
    def display(self, screen):
        screen.blit(self.surface, self.rect)
          
    def moving(self):
        return self.speed != (0,0)
    
    def run(self ,speed):
        if self.type == "flyingMob":
                self.changeSpeed((speed + speed*0.05,choice([randint(int(-400+speed * 0.3),int(-300+speed * 0.3)),randint(int(-120+speed * 0.1),int(100+speed * 0.1))])))   
        elif self.type == "heart":
            self.changeSpeed((speed + randint(0,500),0))
        elif self.type == "mediumMob":
            self.changeSpeed((speed + speed*0.05,0))
        else:
            self.changeSpeed((speed,0))
    