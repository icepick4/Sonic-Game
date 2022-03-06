import pygame
from pygame.locals import *
pygame.init()

windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

def onFloor(entity):
    #check si position de base de sonic
    return entity['position'][1] == height - 200 - 144

def entity(rect):
    entity={'rect': rect,
            'speed': 0,
            'position': rect.topleft,
            'hp': 3
            }
    return entity
    
def jumpSpeed(entity, jump):
    entity['speed'] += jump

def jumpPosition(entity,time):
    speedY = entity['speed']
    x,y = entity['position']
    y-= speedY * time
    entity['position'] = (x,y)
    entity['rect'].bottomleft = entity['position']

def posRestriction(entity,zone):
    x,y = entity['position']
    h = entity['rect'].size[1]
    if y + h > zone.bottom:
        y = zone.bottom - h
        entity['speed'] = 0
    entity['position'] = (x,y)
    entity['rect'].topleft = entity['position']

    