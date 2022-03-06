import pygame
from pygame.locals import *
from time import time
from functions import entity, onFloor, jumpSpeed, jumpPosition, posRestriction
from random import randint
pygame.init()

#set the window
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

timer = pygame.time.Clock()
playing = True
#personnage
sonic1Surface = pygame.image.load("images/sonic1.gif").convert_alpha()
sonic1Rect = entity(sonic1Surface.get_rect(topleft=(100,height - 200 - 144)))
sonic2Surface = pygame.image.load("images/sonic2.gif").convert_alpha()
sonic2Rect = entity(sonic2Surface.get_rect(topleft=(100,height - 200 - 144)))
sonic3Surface = pygame.image.load("images/sonic3.gif").convert_alpha()
sonic3Rect = entity(sonic3Surface.get_rect(topleft=(100,height - 200 - 144)))
sonic4Surface = pygame.image.load("images/sonic4.gif").convert_alpha()
sonic4Rect = entity(sonic4Surface.get_rect(topleft=(100,height - 200 - 144)))
sonicJumpSurface = pygame.image.load("images/sonicJump.png").convert_alpha()
sonicJumpRect = entity(sonicJumpSurface.get_rect(topleft=(100,height - 200 - 144)))
sonicState = 0
#init du delais d'affichage du gif
delay = time()
#init du départ du saut
startJump = time()
#temps de saut
timeJump = 0.3
#état de saut
jumping = False
#rect qui restreint le personnage
sonicRect = pygame.Rect((100,0), (128,height - 200))

#score
scoreTimer = time()
scoreFont = pygame.font.SysFont("Courier New", 50)
scoreSurface = scoreFont.render("Score : {0}".format(0), True, (0,0,0))
scoreRect = scoreSurface.get_rect(midtop=(width/2, 100))
#bouton pour fermer la fenetre
endFont = pygame.font.SysFont("Courier New", 50)
endSurface = endFont.render("CLOSE", True, (0,0,0))
endRect = endSurface.get_rect(topleft=(windowSize[0]-180,10))

while playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            #on presse le bouton close
            if windowSize[0]-180 < event.pos[0] < windowSize[0] and 10 < event.pos[1] < 60:
                playing = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if onFloor(sonicJumpRect):
                    startJump = time()
                    jumping = True
                    jumpSpeed(sonicJumpRect, 1200)
    score = int(round((time() - scoreTimer) * 10,0))
    scoreSurface = scoreFont.render("Score : {0}".format(score), True, (0,0,0))               
    screen.fill((255,255,255))
    screen.blit(endSurface,endRect)
    screen.blit(scoreSurface,scoreRect)
    jumpTime = timer.tick(120) / 1000
    pygame.draw.rect(screen, (0,128,0), (0, height - 200, width, height - 200))
    if time() - startJump < timeJump:
        jumpPosition(sonicJumpRect, jumpTime)
    else:
        jumpSpeed(sonicJumpRect, -1200)
        startJump = time()
    posRestriction(sonicJumpRect, sonicRect)
    if sonicJumpRect['speed'] == 0:
        jumping = False
    if jumping:
        sonicJumpRect['speed'] -= 2
        screen.blit(sonicJumpSurface, sonicJumpRect['rect'])
    else:
        #affichage du gif à la main
        gifDelay = time() - delay
        if sonicState == 0 and gifDelay > 0.05:
            screen.blit(sonic1Surface,sonic1Rect['rect'])
            sonicState = 1
            delay = time()
        elif sonicState == 1  and gifDelay > 0.05:
            screen.blit(sonic2Surface,sonic2Rect['rect'])
            sonicState = 2
            delay = time()
        elif sonicState == 2  and gifDelay > 0.05:
            screen.blit(sonic3Surface,sonic3Rect['rect'])
            sonicState = 3
            delay = time()
        elif sonicState == 3 and gifDelay > 0.05:
            screen.blit(sonic4Surface,sonic4Rect['rect'])
            sonicState = 0
            delay = time()
        else:
            choice = randint(1,4)
            if choice == 1:
                screen.blit(sonic1Surface,sonic1Rect['rect'])
                sonicState = 1
            elif choice == 2:
                screen.blit(sonic2Surface,sonic2Rect['rect'])
                sonicState = 2
            elif choice == 3:
                screen.blit(sonic3Surface,sonic3Rect['rect'])
                sonicState = 3
            else:
                screen.blit(sonic4Surface,sonic4Rect['rect'])
                sonicState = 4
    pygame.display.flip()
pygame.quit()





