import pygame
from time import time

def animateGif(delay, nbImages, timeGif, state):
    delayGif = time() - timeGif
    if delayGif > delay:
        state += 1
        timeGif = time()
    if state == nbImages:
        state = 0
    return timeGif, state

def playSound(path, volume):
    Sound = pygame.mixer.Sound(path)
    Sound.play()
    Sound.set_volume(volume)


    