import pygame
from pygame.locals import *
from time import time
from functions import entity, onFloor, jumpSpeed, jumpPosition, posRestriction, enemyRestriction
from random import randint,uniform
pygame.init()

#set the window
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

#timer pour obtenir les ticks
timer = pygame.time.Clock()

#variable qui maintient le while
playing = True


#personnage
statesSonic = [[0,0,0,0],[0,0]]
statesSonic[0][0] = pygame.image.load("images/sonic1.gif").convert_alpha()
sonic1Rect = entity(statesSonic[0][0].get_rect(topleft=(100,height - 200 - 144)))
statesSonic[0][1] = pygame.image.load("images/sonic2.gif").convert_alpha()
statesSonic[0][2] = pygame.image.load("images/sonic3.gif").convert_alpha()
statesSonic[0][3] = pygame.image.load("images/sonic4.gif").convert_alpha()
statesSonic[1][0] = pygame.image.load("images/sonicStanding1.gif").convert_alpha()
statesSonic[1][1] = pygame.image.load("images/sonicStanding2.gif").convert_alpha()
sonicJumpSurface = pygame.image.load("images/sonicJump.png").convert_alpha()
sonicJumpRect = entity(sonicJumpSurface.get_rect(topleft=(100,height - 200 - 144*4)))

#rect qui restreint le personnage
sonicRect = pygame.Rect((100,0), (128,height - 200))
#état qui définie quel image du gif on affiche
sonicState = 0
sonicStandingState = 0
#init du delais d'affichage du gif
timeGif = time()


#init du départ du saut
startJump = time()
#temps de saut
timeJump = 0.3
#état de saut
jumping = False
preJump = False
#init des coeurs
heart3Surface = pygame.image.load("images/damage3.png").convert_alpha()
heart3Rect = heart3Surface.get_rect(topleft=(65,65))
heart2Surface = pygame.image.load("images/damage2.png").convert_alpha()
heart2Rect = heart2Surface.get_rect(topleft=(65,65))
heart1Surface = pygame.image.load("images/damage1.png").convert_alpha()
heart1Rect = heart1Surface.get_rect(topleft=(65,65))

#init des enemies
enemySurface = pygame.image.load("images/ennemie.png").convert_alpha()
enemy2Surface = pygame.image.load("images/bird.png").convert_alpha()
enemies = []
timeEnemies = time()

#état de dégat pour effet visuel (fond rouge)
damage = False
damageTime = time()
#état qui définit si on a perdu ou non
lost = False
timeSpawn = time()
#affichage du score du last score et du best score
scoreTimer = time()
scoreFont = pygame.font.SysFont("Courier New", 50)
scoreSurface = scoreFont.render("Score : {0}".format(0), True, (0,0,0))
scoreRect = scoreSurface.get_rect(midtop=(width/2, 125))
lastScoreSurface = scoreFont.render("Last score : {0}".format(0), True, (0,0,0))
lastScoreRect = lastScoreSurface.get_rect(midtop=(width/2, 50))
bestScore = 0
bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (255,25,25))
bestScoreRect = bestScoreSurface.get_rect(midtop=(width/2, 0))
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
                #on peut sauter
                if onFloor(sonicJumpRect):
                    startJump = time()
                    jumping = True
                    jumpSpeed(sonicJumpRect, (0,1500))
                    jumpSound = pygame.mixer.Sound("sons/jump.mp3")
                    jumpSound.play()
                    jumpSound.set_volume(0.03)
                # else:
                #     preJump = True
                #on a perdu -> on recommence une partie
                if lost:
                    lost = False
                    scoreTimer = time()
                    score = 0           
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                sonicJumpRect['speed'] = (0,sonicJumpRect['speed'][1] - 1000)

    #si un prejump a été lancé, on fait un jump
    # if preJump:
    #     if onFloor(sonicJumpRect):
    #         startJump = time()
    #         jumping = True
    #         jumpSpeed(sonicJumpRect, (0,1450))
    #         jumpSound = pygame.mixer.Sound("sons/jump.mp3")
    #         jumpSound.play()
    #         jumpSound.set_volume(0.03)
    #         preJump = False
    
    #si on a pas perdu on affiche le score actuel, sinon le last score
    if not lost:
        score = int(round((time() - scoreTimer) * 10,0))
        scoreSurface = scoreFont.render("Score : {0}".format(score), True, (0,0,0))
    else:
        scoreSurface = scoreFont.render("Score : {0}".format(0), True, (0,0,0))

    #score et bouton close
    #remplissage des ennemies
    # if len(enemies) < 4 and delayEnemies > uniform(0.6,1.6) and not lost:
    #     randomSpawn = uniform(400,height - 200)
    #     randomMob = randint(1,2)
    #     if randomMob == 1:
    #         enemies.append(entity(enemySurface.get_rect(topleft=(width, randomSpawn))))
    #         enemies[len(enemies)-1]['hp'] = 44
    #     else:
    #         enemies.append(entity(enemy2Surface.get_rect(topleft=(width, randomSpawn))))
    #         enemies[len(enemies)-1]['hp'] = 666
    #     timeEnemies = time()

    mobsSpeed = 900 + (score * 1.5)
    randomSpawn2 = uniform(400, height - 200 - 144)
    delayMobs = 150 * 4/mobsSpeed
    if time() >= timeSpawn+delayMobs and not lost:
        rand = randint(1,2)
        if rand == 1:
            enemies.append(entity(enemySurface.get_rect(topleft=(width, height - 200))))
            enemies[len(enemies)-1]['hp'] = 44
        else:
            enemies.append(entity(enemySurface.get_rect(topleft=(width, randomSpawn2))))
            enemies[len(enemies)-1]['hp'] = 666
        timeSpawn = time()
    #tick de la frame
    jumpTime = timer.tick(120) / 1000   
    

    #on affiche l'effet visuel (fond rouge) pendant 0.25s
    damageDelay = time() - damageTime
    if damage and damageDelay < 0.25:  
        screen.fill((255,100,100))
    else:
        screen.fill((255,255,255))
        damageTime = time()
        damage = False

    #affichage du coeur en fonction des pv de sonic
    if sonic1Rect['hp'] == 3:
        screen.blit(heart3Surface,heart1Rect)
    elif sonic1Rect['hp'] == 2:
        screen.blit(heart2Surface,heart2Rect)
    else:
        screen.blit(heart1Surface,heart3Rect)

    for i in range(len(enemies)):
        if enemies[i-1]['speed'] == (0,0):
            jumpSpeed(enemies[i-1],(mobsSpeed,0))
        jumpPosition(enemies[i-1], jumpTime)
        #si un ennemie touche sonic ...
        if enemies[i-1]['rect'].colliderect(sonicJumpRect['rect']):
            damageSound = pygame.mixer.Sound("sons/damage.mp3")
            damageSound.play()
            damageSound.set_volume(0.1)
            damage = True
            sonic1Rect['hp'] -=1
            enemies.pop(i-1)
        elif enemyRestriction(enemies[i-1]):
            enemies.pop(i-1)
        if enemies[i-1]['hp'] == 44:
            screen.blit(enemySurface, enemies[i-1]['rect'])
        else:
            screen.blit(enemy2Surface,enemies[i-1]['rect'])
    
    screen.blit(endSurface,endRect)
    screen.blit(scoreSurface,scoreRect)
    screen.blit(lastScoreSurface,lastScoreRect)
    screen.blit(bestScoreSurface,bestScoreRect)
    if bestScore < score :
        bestScore = score
        bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (255,25,25))
    #on a perdu
    if sonic1Rect['hp'] == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        lost = True
        lastScore = score
        lastScoreSurface = scoreFont.render("Last score : {0}".format(lastScore), True, (0,0,0))
        sonic1Rect['hp'] = 3
        
    
    pygame.draw.rect(screen, (0,128,0), (0, height - 200, width, height - 200))
    if time() - startJump < timeJump:
        jumpPosition(sonicJumpRect, jumpTime)
    else:
        jumpSpeed(sonicJumpRect, (0,-1500))
        startJump = time()
    #on restreint les positions de sonic
    posRestriction(sonicJumpRect, sonicRect)
    #si la speed est passé à 0 -> le saut n'est plus actif
    if sonicJumpRect['speed'][1] == 0:
        jumping = False
    
    #si on saute on affiche sonicJump, sinon le gif
    if jumping:
        sonicJumpRect['speed'] = (0,sonicJumpRect['speed'][1] - 15)
        screen.blit(sonicJumpSurface, sonicJumpRect['rect'])
    elif not lost:
        #affichage du gif à la main
        screen.blit(statesSonic[0][sonicState],(100,height - 200 - 144))
        delayGif = time() - timeGif
        if delayGif > 0.03:       
            sonicState += 1
            timeGif = time()
        # elif sonicState == 1  and delayGif > 0.05:
        #     screen.blit(sonic2Surface,sonic2Rect['rect'])
        #     sonicState = 2
        #     timeGif = time()
        # elif sonicState == 2  and delayGif > 0.05:
        #     screen.blit(sonic3Surface,sonic3Rect['rect'])
        #     sonicState = 3
        #     timeGif = time()
        # elif sonicState == 3 and delayGif > 0.05:
        #     screen.blit(sonic4Surface,sonic4Rect['rect'])
        #     sonicState = 0
        #     timeGif = time()
        # else:
        #     choice = randint(1,4)
        #     if choice == 1:
        #         screen.blit(sonic1Surface,sonic1Rect['rect'])
        #         sonicState = 1
        #     elif choice == 2:
        #         screen.blit(sonic2Surface,sonic2Rect['rect'])
        #         sonicState = 2
        #     elif choice == 3:
        #         screen.blit(sonic3Surface,sonic3Rect['rect'])
        #         sonicState = 3
        #     else:
        #         screen.blit(sonic4Surface,sonic4Rect['rect'])
        #         sonicState = 4
    else:
        screen.blit(statesSonic[1][sonicStandingState],(100,height - 200 - 144))
        delayGif = time() - timeGif
        if delayGif > 0.3:
            sonicStandingState += 1
            timeGif = time()
        
                
    if sonicState == 4:
        sonicState = 0
    if sonicStandingState == 2:
        sonicStandingState = 0
    pygame.display.flip()
pygame.quit()





