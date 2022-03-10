try:
    import pygame
    from pygame.locals import *
except:
    print("Vous n'avez pas téléchargé le module pygame ! \n Téléchargez le avec la commande ci-contre : pip install pygame")
from time import time,sleep
from random import randint,uniform, choice

from functions import animateGif, playSound
from variables import *
from classes.Enemy import Enemy

pygame.init()

while playing:
    acceleration = score / 2
    if acceleration > 375:
        acceleration = 375
    #####################
    #ACTIONS DES TOUCHES#
    #####################
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            #on presse le bouton close
            if windowSize[0]-180 < event.pos[0] < windowSize[0] and 10 < event.pos[1] < 60 and lost and time() - endTime() > 3:
                playing = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and time() - endTime > 3:
                #on peut sauter
                if sonicJumpRect.onFloor():
                    startJump = time()
                    jumping = True
                    sonicJumpRect.changeSpeed((0,1300 - acceleration / 2.5))
                    if time() - bestScoreTime > 0.5:
                        playSound(jumpPath, 0.02)
                if lost:
                    lost = False
                    scoreTimer = time()
                    score = 0    
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                sonicJumpRect.changeSpeed((0,-500 - acceleration / 1.3))
    ################
    #SPAWN DES MOBS#
    ################
    #on fait spawn les mobs, avec un délais qui empêche les situations impossibles
    mobsSpeed = 850 + acceleration
    randomSpawn2 = uniform(400, height - 200 - 144)
    delayMobs = 150 * 4.8/mobsSpeed
    if time() >= timeSpawn+delayMobs+uniform(-0.05,0.7) and not lost:
        rand = randint(1,10)
        easterEgg = -1
        if sonic1Rect.hp == 1:
            randomHeart = randint(1,8)
            easterEgg = randint(1,1000)
        elif sonic1Rect.hp == 2:
            randomHeart = randint(1,25)
        elif sonic1Rect.hp == 3:
            randomHeart = randint(1,50)
        elif sonic1Rect.hp == 4:
            randomHeart = randint(1,200)
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
        if easterEgg == 1:
            for i in range(4):
                enemies.append(Enemy(heartSurface.get_rect(topleft=(width, height - randint(200,700))), "heart"))
        timeSpawn = time()

    #tick de la frame 
    tick = timer.tick(200) / 1000 
    
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
        screen.fill((135,206,235))
        effectTime = time()
        damage = False
        healing = False

    ########
    #LES PV#
    ########
    #affichage du coeur en fonction des pv de sonic
    for i in range(sonic1Rect.hp):
        screen.blit(heartSurface,(heartRect[0] + i*100,heartRect[1]))

    ############
    #LES SCORES#
    ############
    #si on a pas perdu on affiche le score actuel, sinon le last score
    if not lost:
        score = int(round((time() - scoreTimer) * 10,0))
        if bestScoreBeaten:
            scoreSurface = scoreLiveFont.render("{0}".format(score), True, (255,195,36))
        else:
            scoreSurface = scoreLiveFont.render("{0}".format(score), True, (0,0,0))
    if bestScore < score :
        bestScore = score
        if not bestScoreBeaten:
            playSound(bestScorePath, 0.05)
            bestScoreTime = time()
        bestScoreBeaten = True
        
    ############
    #LES TEXTES#
    ############
    if lost:
        screen.blit(endSurface,endRect)
        screen.blit(lastScoreSurface,lastScoreRect)
        screen.blit(bestScoreSurface,bestScoreRect)
    elif not lost:
        scoreRect = scoreSurface.get_rect(topright=(width,10))
        screen.blit(scoreSurface,scoreRect)
        
    if score%100 == 0 and score !=0 and score%1000 != 0 and time() - timeScoreSound > 0.2:
        playSound(scorePath,0.03)
        timeScoreSound = time()
    elif score%1000 == 0 and score != 0 and time() - timeScoreSound > 0.2:
        playSound(score1000Path, 0.05)
        timeScoreSound = time()

    ############
    #ON A PERDU#
    ############
    if sonic1Rect.hp == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        lost = True
        bestScoreBeaten = False
        lastScore = score
        lastScoreSurface = scoreFont.render("Last score : {0}".format(lastScore), True, (0,0,0))
        bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (0,0,0))
        sonic1Rect.hp = 3
        playSound(lostPath,0.06)
        endTime = time()
        
    #herbe
    #pygame.draw.rect(screen, (72,15,4), (0, height - 200, width, height - 200))
    #pygame.draw.rect(screen, (103,196,12), (0, height - 200, width, 50))
    ############
    #LES DECORS#
    ############
    if not lost:
        grassRect.speed = (mobsSpeed,0)
        grassRect2.speed = (mobsSpeed,0)

        if grassRect.loop():
            grassRect.position = (width,height)
        if grassRect2.loop():
            grassRect2.position = (width,height)

        grassRect.changePosition(tick)
        grassRect2.changePosition(tick) 
        screen.blit(grassSurface,grassRect)
        screen.blit(grassSurface,grassRect2)

    
    if cloudRect.loop():
        cloudRect.position = (width,randint(200,height / 2))
    if cloud2Rect.loop():
        cloud2Rect.position = (width + randint(500,2000),randint(200,height / 2))
    
    cloudRect.changePosition(tick)
    cloud2Rect.changePosition(tick)
    screen.blit(cloudSurface,cloudRect) 
    screen.blit(cloudSurface,cloud2Rect)

    if palmRect.loop():
        palmRect.position = (width + randint(0,500),height - 200)
    if palm2Rect.loop():
        palm2Rect.position = (width + randint(500,2000),height - 200)
    palmRect.changePosition(tick)
    palm2Rect.changePosition(tick)
    screen.blit(palmSurface,palmRect) 
    screen.blit(palm2Surface,palm2Rect)
         
    ##############
    #LES ENNEMIES#
    ##############
    enemiesToPop = []
    for i in range(len(enemies)):
        if enemies[i].speed == (0,0):
            if enemies[i].type == "flyingMob":
                enemies[i].changeSpeed((mobsSpeed + mobsSpeed*0.05,choice([randint(-400, -300),randint(-120,100)])))   
            elif enemies[i].type == "heart":
                enemies[i].changeSpeed((mobsSpeed + randint(0,500),0))
            elif enemies[i].type == "mediumMob":
                enemies[i].changeSpeed((mobsSpeed + mobsSpeed*0.05,0))
            else:
                enemies[i].changeSpeed((mobsSpeed,0))
        enemies[i].changePosition(tick)
        #si un ennemie touche sonic ...
        if enemies[i].rect.colliderect(sonicJumpRect.rect) and enemies[i].type == "heart":
            if time() - bestScoreTime > 0.5:
                playSound(healingPath, 0.1)
            if sonic1Rect.hp < 6:
                sonic1Rect.hp +=1
            healing = True
            enemiesToPop.append(i)
        #si un ennemie atteind le mur
        elif enemies[i].rect.colliderect(sonicJumpRect.rect):
            if time() - bestScoreTime > 0.5:
                playSound(damagePath, 0.1)
            damage = True
            sonic1Rect.hp -=1
            enemiesToPop.append(i)
        elif enemies[i].enemyRestriction():
            enemiesToPop.append(i)

        ####################
        #AFFICHAGE DES MOBS#
        ####################       
        #on blit les bonnes image en fonction du type de mob
        if enemies[i].type == "littleMob":
            screen.blit(rockSurface,enemies[i].rect)   
        elif enemies[i].type == "mediumMob":
            screen.blit(statesDuck[duckState],enemies[i].rect)
            delayGif = time() - timeGifDuck
            timeGifDuck, duckState = animateGif(0.08,2,timeGifDuck, duckState)
        elif enemies[i].type == "bigMob":
            screen.blit(enemySpikeSurface,enemies[i].rect)
        elif enemies[i].type == "flyingMob":
            screen.blit(enemyBirdSurface,enemies[i].rect)
        else:
            screen.blit(heartSurface,enemies[i].rect)
    for i in enemiesToPop:
        enemies.pop(i)
    #################
    #GESTION DU SAUT#
    #################
    #si on est en cours de saut -> on change la position, sinon on redescend
    if time() - startJump < timeJump:
        sonicJumpRect.changePosition(tick)
    else:
        sonicJumpRect.changeSpeed((0,-1300 - acceleration))
        startJump = time()
    
    ####################
    #AFFICHAGE DU PERSO#
    ####################
    #on restreint les positions de sonic
    sonicJumpRect.sonicPosRestriction(sonicRect)
    #si la speed est passé à 0 -> le saut n'est plus actif
    if sonicJumpRect.speed[1] == 0:
        jumping = False
    
    if sonicJumpRect.speed[1] < 0:
        sonicJumpRect.changeSpeed((0,-50))

    #si on saute on affiche sonicJump
    if jumping and not lost:
        sonicJumpRect.changeSpeed((0,-3))
        screen.blit(sonicJumpSurface, sonicJumpRect.rect)
    #si on a pas perdu on affiche le gif sonic qui court
    elif not lost:
        #affichage du gif à la main
        screen.blit(statesSonic[0][sonicState],(100,height - 200 - 144))
        timeGif, sonicState = animateGif(0.1,4,timeGif, sonicState)
    #sinon on affiche sonic standing
    else:
        if time() - endTime < 3:
            screen.blit(gameOverSurface,gameOverRect)
        else:
            screen.blit(statesSonic[1][sonicStandingState],(100,height - 200 - statesSonic[1][0].get_height()))
            screen.blit(restartSurface,restartRect)
            timeGif, sonicStandingState = animateGif(0.3,2,timeGif, sonicStandingState)
            screen.blit(grassSurface,grassSurface.get_rect(topright=(width,height - 200)))

    pygame.display.flip()
pygame.quit()

with open('bestScore.txt', 'w') as f:
    f.write(str(bestScore))





