try:
    import pygame
    from pygame.locals import *
except:
    print("Vous n'avez pas téléchargé le module pygame ! \n Téléchargez le avec la commande ci-contre : pip install pygame")
from time import time
from random import randint,uniform, choice

from Functions import animateGif, playSound
from variables import *
from classes.Enemy import Enemy

pygame.init()

#set the window
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

#timer pour obtenir les ticks
timer = pygame.time.Clock()

enemies = []

#init du score, du bestscore, et du lastscore
score = 0
with open("bestScore.txt") as f:
    bestScore = int(f.readline())
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

#sons paths
healingPath = "sounds/healing.wav"
jumpPath = "sounds/jump.mp3"
damagePath = "sounds/damage.wav"

#bouton pour fermer la fenetre
endFont = pygame.font.SysFont("Courier New", 50)
endSurface = endFont.render("CLOSE", True, (0,0,0))
endRect = endSurface.get_rect(topleft=(windowSize[0]-180,10))

while playing:

    #####################
    #ACTIONS DES TOUCHES#
    #####################
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
                if sonicJumpRect.onFloor():
                    startJump = time()
                    jumping = True
                    sonicJumpRect.changeSpeed((0,1300 + score / 4))
                    playSound(jumpPath, 0.03)
                    # jumpSound = pygame.mixer.Sound("sons/jump.mp3")
                    # jumpSound.play()
                    # jumpSound.set_volume(0.03)
                # else:
                #     preJump = True
                # if jumping:
                #     changeSpeed(sonicJumpRect, (0,-50))
                #on a perdu -> on recommence une partie
                if lost:
                    lost = False
                    scoreTimer = time()
                    score = 0   
                
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                #sonicJumpRect.speed = (0,sonicJumpRect.speed[1] - 500)
                sonicJumpRect.changeSpeed((0,-500 - score / 2))

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
    mobsSpeed = 900 + (score / 2)
    randomSpawn2 = uniform(400, height - 200 - 144)
    delayMobs = 150 * 4.5/mobsSpeed
    if time() >= timeSpawn+delayMobs+uniform(-0.05,0.5) and not lost:
        rand = randint(1,10)
        if sonic1Rect.hp == 1:
            randomHeart = randint(1,10)
        elif sonic1Rect.hp == 2:
            randomHeart = randint(1,30)
        elif sonic1Rect.hp == 3:
            randomHeart = randint(1,50)

        if rand <= 6:
            if 0 < rand <= 2: 
                enemies.append(Enemy(rockSurface.get_rect(topleft=(width, height - 200)), "littleMob"))
            elif 2 < rand <= 4:
                enemies.append(Enemy(statesDuck[duckState].get_rect(topleft=(width, height - 200)), "mediumMob"))
            else:
                enemies.append(Enemy(enemySpikeSurface.get_rect(topleft=(width, height - 200)), "bigMob"))
        else:
            enemies.append(Enemy(enemyBirdSurface.get_rect(topleft=(width, 300)), "flyingMob"))
        if randomHeart == 1 and enemies[len(enemies)-1].type != "heart" and enemies[len(enemies)-2].type != "heart":
            enemies.append(Enemy(heartSurface.get_rect(topleft=(width, height - randint(200,700))), "heart"))
        timeSpawn = time()

    #tick de la frame 
    tick = timer.tick(120) / 1000   
    
    ###################################
    #LES FONDS --> LES DEGATS ET HEALS#
    ###################################
    #on affiche l'effet visuel de dégats(fond rouge) pendant 0.25s, et de healing (fond vert) (default : blanc)
    effectDelay = time() - effectTime
    if damage and effectDelay < 0.25:  
        screen.fill((255,100,100))
    elif healing and effectDelay < 0.25:
        screen.fill((100,255,100))
    else:
        screen.fill((255,255,255))
        effectTime = time()
        damage = False
        healing = False

    ########
    #LES PV#
    ########
    #affichage du coeur en fonction des pv de sonic
    if sonic1Rect.hp == 4:
        for i in range(4):
            screen.blit(heartSurface,(heartRect[0] + i*100,heartRect[1]))
    elif sonic1Rect.hp == 3:
        for i in range(3):
            screen.blit(heartSurface,(heartRect[0] + i*100,heartRect[1]))
    elif sonic1Rect.hp == 2:
        for i in range(2):
            screen.blit(heartSurface,(heartRect[0] + i*100,heartRect[1]))
    else:
        screen.blit(heartSurface,(heartRect[0],heartRect[1]))

    ##############
    #LES ENNEMIES#
    ##############
    for i in range(len(enemies)):
        if enemies[i-1].speed == (0,0):
            if enemies[i-1].type == "flyingMob":
                enemies[i-1].changeSpeed((mobsSpeed,choice([randint(-400, -300),randint(-120,100)])))   
            elif enemies[i-1].type == "heart":
                enemies[i-1].changeSpeed((mobsSpeed + randint(0,500),0))
            else:
                enemies[i-1].changeSpeed((mobsSpeed,0))
        enemies[i-1].changePosition(tick)
        #si un ennemie touche sonic ...
        if enemies[i-1].rect.colliderect(sonicJumpRect.rect) and enemies[i-1].type == "heart":
            playSound(healingPath, 0.1)
            sonic1Rect.hp +=1
            healing = True
            enemies.pop(i-1)
            break
        #si un ennemie atteind le mur
        elif enemies[i-1].rect.colliderect(sonicJumpRect.rect):
            playSound(damagePath, 0.1)
            damage = True
            sonic1Rect.hp -=1
            enemies.pop(i-1)
        elif enemies[i-1].enemyRestriction():
            enemies.pop(i-1)

        ####################
        #AFFICHAGE DES MOBS#
        ####################       
        #on blit les bonnes image en fonction du type de mob
        if enemies[i-1].type == "littleMob":
            screen.blit(rockSurface,enemies[i-1].rect)   
        elif enemies[i-1].type == "mediumMob":
            screen.blit(statesDuck[duckState],enemies[i-1].rect)
            delayGif = time() - timeGifDuck
            timeGifDuck, duckState = animateGif(0.08,2,timeGifDuck, duckState)
        elif enemies[i-1].type == "bigMob":
            screen.blit(enemySpikeSurface,enemies[i-1].rect)
        elif enemies[i-1].type == "flyingMob":
            screen.blit(enemyBirdSurface,enemies[i-1].rect)
        else:
            screen.blit(heartSurface,enemies[i-1].rect)
    
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
    if sonic1Rect.hp == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        lost = True
        lastScore = score
        lastScoreSurface = scoreFont.render("Last score : {0}".format(lastScore), True, (0,0,0))
        sonic1Rect.hp = 3
        
    #herbe
    pygame.draw.rect(screen, (0,128,0), (0, height - 200, width, height - 200))

    #################
    #GESTION DU SAUT#
    #################
    #si on est en cours de saut -> on change la position, sinon on redescend
    if time() - startJump < timeJump:
        sonicJumpRect.changePosition(tick)
    else:
        sonicJumpRect.changeSpeed((0,-1300 - score / 2))
        startJump = time()
    
    ####################
    #AFFICHAGE DU PERSO#
    ####################
    #on restreint les positions de sonic
    sonicJumpRect.sonicPosRestriction(sonicRect)
    #si la speed est passé à 0 -> le saut n'est plus actif
    if sonicJumpRect.speed[1] == 0:
        jumping = False

    #si on saute on affiche sonicJump
    if jumping:
        sonicJumpRect.changeSpeed((0,-13))
        screen.blit(sonicJumpSurface, sonicJumpRect.rect)
    #si on a pas perdu on affiche le gif sonic qui court
    elif not lost:
        #affichage du gif à la main
        screen.blit(statesSonic[0][sonicState],(100,height - 200 - 144))
        timeGif, sonicState = animateGif(0.1,4,timeGif, sonicState)
    #sinon on affiche sonic standing
    else:
        screen.blit(statesSonic[1][sonicStandingState],(100,height - 200 - 144))
        screen.blit(restartSurface,restartRect)
        timeGif, sonicStandingState = animateGif(0.3,2,timeGif, sonicStandingState)

    pygame.display.flip()
pygame.quit()

with open('bestScore.txt', 'w') as f:
    f.write(str(bestScore))





