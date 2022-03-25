"""file containing functions"""
from time import time
import pygame

def animate_gif(delay, nb_images, time_gif, state):
    """animate the gif"""
    delay_gif = time() - time_gif
    if delay_gif > delay:
        state += 1
        time_gif = time()
    if state == nb_images:
        state = 0
    return time_gif, state

def play_sound(path, volume):
    """play a sound"""
    sound = pygame.mixer.Sound(path)
    sound.play()
    sound.set_volume(volume)
