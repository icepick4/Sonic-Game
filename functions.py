import pygame
from pygame.locals import *
from time import time
pygame.init()

def animateGif(delay, nbImages, timeGif, state):
    delayGif = time() - timeGif
    if delayGif > delay:
        state += 1
        timeGif = time()
    if state == nbImages:
        state = 0
    return timeGif, state

def playSound(path, volume):
    voice = pygame.mixer.Channel(5)
    Sound = pygame.mixer.Sound(path)
    voice.play(Sound)
    Sound.set_volume(volume)
    return voice


    