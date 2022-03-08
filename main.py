import pygame
from pygame.locals import *
from time import time
from functions import entity, onFloor, changeSpeed, changePosition, sonicPosRestriction, enemyRestriction, animateGif
from random import randint,uniform, choice
pygame.init()

#set the window
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

#timer pour obtenir les ticks
timer = pygame.time.Clock()

#variable qui maintient le while du jeu
playing = True

#personnage
#tableau des états de sonic : tab[0][i] -> état de saut, tab[1][i] -> état de standing
statesSonic = [[0,0,0,0],[0,0]]
statesSonic[0][0] = pygame.image.load("images/sonic1.gif").convert_alpha()
sonic1Rect = entity(statesSonic[0][0].get_rect(topleft=(100,height - 200 - 144)), "sonic")
statesSonic[0][1] = pygame.image.load("images/sonic2.gif").convert_alpha()
statesSonic[0][2] = pygame.image.load("images/sonic3.gif").convert_alpha()
statesSonic[0][3] = pygame.image.load("images/sonic4.gif").convert_alpha()
statesSonic[1][0] = pygame.image.load("images/sonicStanding1.gif").convert_alpha()
statesSonic[1][1] = pygame.image.load("images/sonicStanding2.gif").convert_alpha()
sonicJumpSurface = pygame.image.load("images/sonicJump.png").convert_alpha()
sonicJumpRect = entity(sonicJumpSurface.get_rect(topleft=(100,height - 200 - 144*4)), "sonicJumping")

#rect qui restreint le personnage
sonicRect = pygame.Rect((100,0), (128,height - 200))

#état qui définie quel image du gif on affiche
sonicState = 0
sonicStandingState = 0
#init du delais d'affichage du gif
timeGif = time()
timeGifDuck = time()
timeGifCharac = time()
#init du départ du saut
startJump = time()
#temps de saut
timeJump = 0.3
#état de saut
jumping = False
preJump = False
#init des coeurs
heart3Surface = pygame.image.load("images/damage3.png").convert_alpha()
heart2Surface = pygame.image.load("images/damage2.png").convert_alpha()
heart1Surface = pygame.image.load("images/damage1.png").convert_alpha()
heartRect = heart1Surface.get_rect(topleft=(65,65))

#init des enemies
enemySurface = pygame.image.load("images/spike.png").convert_alpha()
enemyBirdSurface = pygame.image.load("images/bird.png").convert_alpha()
enemies = []
timeSpawn = time()

statesDuck = [0,0]
statesDuck[0] = pygame.image.load("images/duck1.png").convert_alpha()
statesDuck[1] = pygame.image.load("images/duck2.png").convert_alpha()
duckState = 0

rockSurface = pygame.image.load("images/rock.png").convert_alpha()
#état de dégat pour effet visuel (fond rouge)
damage = False
damageTime = time()
#état qui définit si on a perdu ou non
lost = True

#init du score, du bestscore, et du lastscore
score = 0
bestScore = 0
scoreTimer = time()
scoreFont = pygame.font.SysFont("Courier New", 50)
restartFont = pygame.font.SysFont("Courier New", 75)
scoreSurface = scoreFont.render("Score : {0}".format(0), True, (0,0,0))
scoreRect = scoreSurface.get_rect(midtop=(width/2, 125))
lastScoreSurface = scoreFont.render("Last score : {0}".format(0), True, (0,0,0))
lastScoreRect = lastScoreSurface.get_rect(midtop=(width/2, 50))
bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (0,0,0))
bestScoreRect = bestScoreSurface.get_rect(midtop=(width/2, 0))
restartSurface = restartFont.render("PRESS SPACE TO START", True, (255,10,10))
restartRect = restartSurface.get_rect(midtop=(width/2,height/2))


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
                    changeSpeed(sonicJumpRect, (0,1300))
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
                #sonicJumpRect['speed'] = (0,sonicJumpRect['speed'][1] - 500)
                changeSpeed(sonicJumpRect, (0,-400))

    #si un prejump a été lancé, on fait un jump
    # if preJump:
    #     if onFloor(sonicJumpRect):
    #         startJump = time()
    #         jumping = True
    #         changeSpeed(sonicJumpRect, (0,1450))
    #         jumpSound = pygame.mixer.Sound("sons/jump.mp3")
    #         jumpSound.play()
    #         jumpSound.set_volume(0.03)
    #         preJump = False

    ################
    #SPAWN DES MOBS#
    ################
    #on fait spawn les mobs, avec un délais qui empêche les situations impossibles
    mobsSpeed = 800 + (score * 1.2)
    randomSpawn2 = uniform(400, height - 200 - 144)
    delayMobs = 150 * 6/mobsSpeed
    if time() >= timeSpawn+delayMobs and not lost:
        rand = randint(1,10)
        if rand <= 6:
            if 0 < rand <= 2: 
                enemies.append(entity(rockSurface.get_rect(topleft=(width, height - 200)), "littleMob"))
            elif 2 < rand <= 4:
                enemies.append(entity(statesDuck[duckState].get_rect(topleft=(width, height - 200)), "mediumMob"))
            else:
                enemies.append(entity(enemySurface.get_rect(topleft=(width, height - 200)), "bigMob"))
        else:
            enemies.append(entity(enemyBirdSurface.get_rect(topleft=(width, 300)), "flyingMob"))
        timeSpawn = time()

    #tick de la frame
    tick = timer.tick(120) / 1000   
    
    ############
    #LES DEGATS#
    ############
    #on affiche l'effet visuel de dégats(fond rouge) pendant 0.25s
    damageDelay = time() - damageTime
    if damage and damageDelay < 0.25:  
        screen.fill((255,100,100))
    else:
        screen.fill((255,255,255))
        damageTime = time()
        damage = False
    #affichage du coeur en fonction des pv de sonic
    if sonic1Rect['hp'] == 3:
        screen.blit(heart3Surface,heartRect)
    elif sonic1Rect['hp'] == 2:
        screen.blit(heart2Surface,heartRect)
    else:
        screen.blit(heart1Surface,heartRect)

    ##############
    #LES ENNEMIES#
    ##############
    for i in range(len(enemies)):
        if enemies[i-1]['speed'] == (0,0):
            if enemies[i-1]['type'] != "flyingMob":
                changeSpeed(enemies[i-1],(mobsSpeed,0))
            else:
                changeSpeed(enemies[i-1],(mobsSpeed,choice([randint(-380, -280),randint(-120,-20)])))
        changePosition(enemies[i-1], tick)
        #si un ennemie touche sonic ...
        if enemies[i-1]['rect'].colliderect(sonicJumpRect['rect']):
            damageSound = pygame.mixer.Sound("sons/damage.mp3")
            damageSound.play()
            damageSound.set_volume(0.1)
            damage = True
            sonic1Rect['hp'] -=1
            enemies.pop(i-1)
        #si un ennemie atteind le mur
        elif enemyRestriction(enemies[i-1]):
            enemies.pop(i-1)
        if enemies[i-1]['type'] == "littleMob":
            screen.blit(rockSurface,enemies[i-1]['rect'])   
        elif enemies[i-1]['type'] == "mediumMob":
            screen.blit(statesDuck[duckState],enemies[i-1]['rect'])
            delayGif = time() - timeGifDuck
            timeGifDuck, duckState = animateGif(0.08,2,timeGifDuck, duckState)
        elif enemies[i-1]['type'] == "bigMob":
            screen.blit(enemySurface,enemies[i-1]['rect'])
        else:
            screen.blit(enemyBirdSurface,enemies[i-1]['rect'])
    
    ############
    #LES TEXTES#
    ############
    screen.blit(endSurface,endRect)
    screen.blit(scoreSurface,scoreRect)
    screen.blit(lastScoreSurface,lastScoreRect)
    screen.blit(bestScoreSurface,bestScoreRect)

    ############
    #LES SCORES#
    ############
    #si on a pas perdu on affiche le score actuel, sinon le last score
    if not lost:
        score = int(round((time() - scoreTimer) * 10,0))
        scoreSurface = scoreFont.render("Score : {0}".format(score), True, (0,0,0))
    else:
        scoreSurface = scoreFont.render("Score : {0}".format(0), True, (0,0,0))
    if bestScore < score :
        bestScore = score
        bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (255,25,25))


    ############
    #ON A PERDU#
    ############
    if sonic1Rect['hp'] == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        lost = True
        lastScore = score
        lastScoreSurface = scoreFont.render("Last score : {0}".format(lastScore), True, (0,0,0))
        sonic1Rect['hp'] = 3
        
    #herbe
    pygame.draw.rect(screen, (0,128,0), (0, height - 200, width, height - 200))

    #################
    #GESTION DU SAUT#
    #################
    #si on est en cours de saut -> on change la position, sinon on redescend
    if time() - startJump < timeJump:
        changePosition(sonicJumpRect, tick)
    else:
        changeSpeed(sonicJumpRect, (0,-1500))
        startJump = time()
    
    ####################
    #AFFICHAGE DU PERSO#
    ####################

    #on restreint les positions de sonic
    sonicPosRestriction(sonicJumpRect, sonicRect)
    #si la speed est passé à 0 -> le saut n'est plus actif
    if sonicJumpRect['speed'][1] == 0:
        jumping = False

    #si on saute on affiche sonicJump
    if jumping:
        changeSpeed(sonicJumpRect, (0,-15))
        screen.blit(sonicJumpSurface, sonicJumpRect['rect'])
    #si on a pas perdu on affiche le gif sonic qui court
    elif not lost:
        #affichage du gif à la main
        screen.blit(statesSonic[0][sonicState],(100,height - 200 - 144))
        timeGif, sonicState = animateGif(0.08,2,timeGif, sonicState)
    #sinon on affiche sonic standing
    else:
        screen.blit(statesSonic[1][sonicStandingState],(100,height - 200 - 144))
        screen.blit(restartSurface,restartRect)
        timeGif, sonicStandingState = animateGif(0.3,2,timeGif, sonicStandingState)

    pygame.display.flip()
pygame.quit()





