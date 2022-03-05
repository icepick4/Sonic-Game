import pygame
from pygame.locals import *
from time import time
pygame.init()

#set the window
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

playing = True

#personnage
sonic1Surface = pygame.image.load("images/sonic1.gif").convert_alpha()
sonic1Rect = sonic1Surface.get_rect(bottomleft=(100,height - 200))
sonic2Surface = pygame.image.load("images/sonic2.gif").convert_alpha()
sonic2Rect = sonic2Surface.get_rect(bottomleft=(100,height - 200))
sonic3Surface = pygame.image.load("images/sonic3.gif").convert_alpha()
sonic3Rect = sonic3Surface.get_rect(bottomleft=(100,height - 200))
sonic4Surface = pygame.image.load("images/sonic4.gif").convert_alpha()
sonic4Rect = sonic4Surface.get_rect(bottomleft=(100,height - 200))
sonicState = 0
delay = time()

#grass
#grassSurface = pygame.image.load("images/grass.png").convert_alpha()
#grassRect = grassSurface.get_rect(topleft=(0,0))
#bouton pour fermer la fenetre
endFont = pygame.font.SysFont("Courier New", 50)
endSurface = endFont.render("CLOSE", True, (0,0,0))
endRect = endSurface.get_rect(topright=(windowSize[0]-10,10))

while playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            #on presse le bouton close
            if windowSize[0]-190 < event.pos[0] < windowSize[0] and 10 < event.pos[1] < 60:
                playing = False
    screen.fill((255,255,0))
    screen.blit(endSurface,endRect)
    pygame.draw.rect(screen, (0,128,0), (0, height - 200, width, height - 200))
    #affichage du gif à la main
    gifDelay = time() - delay
    if sonicState == 0 and gifDelay > 0.02:
        screen.blit(sonic1Surface,sonic1Rect)
        sonicState = 1
        delay = time()
    elif sonicState == 1  and gifDelay > 0.02:
        screen.blit(sonic2Surface,sonic2Rect)
        sonicState = 2
        delay = time()
    elif sonicState == 2  and gifDelay > 0.02:
        screen.blit(sonic3Surface,sonic3Rect)
        sonicState = 3
        delay = time()
    elif sonicState == 3 and gifDelay > 0.02:
        screen.blit(sonic4Surface,sonic4Rect)
        sonicState = 0
        delay = time()
    else:
        screen.blit(sonic1Surface,sonic1Rect)
    pygame.display.flip()
pygame.quit()





