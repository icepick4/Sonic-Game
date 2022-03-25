"""environment class"""
from random import randint
import pygame
from classes.entity import Entity
height = pygame.display.get_desktop_sizes()[0][1]
width = pygame.display.get_desktop_sizes()[0][0]


class Environment (Entity):
    """init an environment entity"""
    def __init__(self,rect, surface, category):
        Entity.__init__(self, rect)
        self.surface = surface
        self.category = category
        self.speed = (0,0)
        self.position = self.rect.topleft

    def loop(self):
        """reset width pos when reaching end of the screen"""
        pos_x,_ = self.position
        width_entity = self.rect.size[0]
        if pos_x + width_entity < 0:
            return True
        return False

    def get_rand_pos(self):
        """return a random pos"""
        if self.category in ("cloud1","palm1"):
            rand_x = randint(0,500)
            if self.category == "palm1":
                rand_y = height - 200
            else:
                rand_y = randint(200,height / 2)
        elif self.category in ("cloud2","palm2"):
            rand_x = randint(1000,2500)
            if self.category == "palm2":
                rand_y = height - 200
            else:
                rand_y = randint(200,height / 2)
        else:
            rand_x = 0
            rand_y = 0
        return rand_x, rand_y

    def animate(self,speed_x, speed_y, tick, screen):
        """moving the entity"""
        self.speed = (speed_x,speed_y)
        if self.loop():
            if self.category == "grass":
                self.position = (width,height)
            else:
                self.position = (width + self.get_rand_pos()[0],self.get_rand_pos()[1])
        self.change_position(tick)
        screen.blit(self.surface,self.rect)
