import pygame
from pygame.locals import *
from time import time
pygame.init()

windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

def onFloor(entity):
    return entity['position'][1] == height - 200 - 144

def entity(rect,type):
    entity={'rect': rect,
            'speed': (0,0),
            'position': rect.topleft,
            'hp': 3,
            'weight': 294,
            'type': type
            }
    return entity
    
def changeSpeed(entity, acceleration):
    speedX, speedY = entity['speed']
    aX, aY = acceleration
    entity['speed'] = (speedX + aX, speedY + aY)

def changePosition(entity,time):
    speedX, speedY = entity['speed']
    x,y = entity['position']
    x-= speedX * time
    y-= speedY * time
    entity['position'] = (x,y)
    entity['rect'].bottomleft = entity['position']

def sonicPosRestriction(entity,zone):
    x,y = entity['position']
    h = entity['rect'].size[1]
    if y + h > zone.bottom:
        y = zone.bottom - h
        entity['speed'] = (0,0)
    entity['position'] = (x,y)
    entity['rect'].topleft = entity['position']

def enemyRestriction(entity):
    x,y = entity['position']
    w = entity['rect'].size[0]
    if x + w < 0:
        return True
    return False

def animateGif(delay, nbImages, timeGif, state):
    delayGif = time() - timeGif
    if delayGif > delay:
        state += 1
        timeGif = time()
    if state == nbImages:
        state = 0
    return timeGif, state
    

    