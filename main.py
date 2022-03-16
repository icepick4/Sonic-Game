from register import *
from variables import *
from highScoresScreen import *
try:
    import pygame
    from pygame.locals import *
except:
    print("Vous n'avez pas téléchargé le module pygame ! \n Téléchargez le avec la commande ci-contre : pip install pygame")
from time import time
from random import randint,uniform
from functions import animateGif, playSound
from classes.Enemy import Enemy

while playing:
    acceleration = score / 2
    if acceleration > 666:
        acceleration = 666
    #####################
    #ACTIONS DES TOUCHES#
    #####################    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.MOUSEMOTION:
            if endRect.left < event.pos[0] < endRect.right and endRect.top < event.pos[1] < endRect.bottom and lost and time() - endTime > 3:
                endSurface = endFont.render("CLOSE", True, (255,60,60))
            else:
                endSurface = endFont.render("CLOSE", True, (0,0,0))
            if scoresScreenRect.left < event.pos[0] < scoresScreenRect.right and scoresScreenRect.top < event.pos[1] < scoresScreenRect.bottom and lost and time() - endTime > 3:
                scoresScreenSurface = endFont.render("HIGHSCORES", True, (255,60,60))
            else:
                scoresScreenSurface = endFont.render("HIGHSCORES", True, (0,0,0))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            #on presse le bouton close
            if endRect.left < event.pos[0] < endRect.right and endRect.top < event.pos[1] < endRect.bottom and lost and time() - endTime > 3: 
                playing = False
            #on presse le bouton highscores
            if scoresScreenRect.left < event.pos[0] < scoresScreenRect.right and scoresScreenRect.top < event.pos[1] < scoresScreenRect.bottom and lost and time() - endTime > 3:
                
                playing = ScreenScores(True)
                
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
                if acceleration > 500:
                    fallingSpeed = 500
                else:
                    fallingSpeed = acceleration
                sonicJumpRect.changeSpeed((0,-500 - fallingSpeed / 1.3))
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
            randomHeart = randint(1,25)
            easterEgg = randint(1,1000)
        elif sonic1Rect.hp == 2:
            randomHeart = randint(1,55)
        elif sonic1Rect.hp == 3:
            randomHeart = randint(1,100)
        elif sonic1Rect.hp == 4:
            randomHeart = randint(1,200)
        if rand <= 7:
            if 0 < rand <= 2: 
                enemies.append(Enemy(rockSurface.get_rect(topleft=(width, height - 200)), rockSurface, "littleMob"))
            elif 2 < rand <= 4:
                enemies.append(Enemy(statesDuck[duckState].get_rect(topleft=(width, height - 200)), statesDuck[duckState], "mediumMob"))
            else:
                enemies.append(Enemy(enemySpikeSurface.get_rect(topleft=(width, height - 200)), enemySpikeSurface,  "bigMob"))
        else:
            enemies.append(Enemy(enemyBirdSurface.get_rect(topleft=(width, 300)), enemyBirdSurface, "flyingMob"))
        if randomHeart == 1 and enemies[len(enemies)-1].type != "heart" and enemies[len(enemies)-2].type != "heart":
            enemies.append(Enemy(heartSurface.get_rect(topleft=(width, height - randint(200,700))), heartSurface, "heart"))
        if easterEgg == 1:
            for i in range(4):
                enemies.append(Enemy(heartSurface.get_rect(topleft=(width, height - randint(200,700))), heartSurface, "heart"))
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
    ##################
    #j'essaye de mettre un grass en fond constamment pour cacher le trou du défilement, c'est moche
    #screen.blit(grassSurface,(0,height - 200))

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
        scores[name] = bestScore
        with open ("bestScore.pickle", "wb") as f:
            pickle.dump(scores, f)

    ############
    #LES DECORS#
    ############
    if not lost:
        grassRect.animate(mobsSpeed, 0, tick, screen)
        grass2Rect.animate(mobsSpeed, 0, tick, screen)
        cloudRect.animate(620,0, tick, screen)
        cloud2Rect.animate(550,0, tick, screen)
        palmRect.animate(475,0, tick, screen)
        palm2Rect.animate(475,0, tick, screen)
    else:
        cloudRect.animate(160,0, tick, screen)
        cloud2Rect.animate(70,0, tick, screen)
        palmRect.position = (width / 4, height - 200)
        palm2Rect.position = (width / 1.3, height - 200)
        palmRect.animate(0,0, tick, screen)
        palm2Rect.animate(0,0, tick, screen)

    ##############
    #LES ENNEMIES#
    ##############
    enemiesToPop = []
    for i in range(len(enemies)):
        if not enemies[i].moving():
            enemies[i].run(mobsSpeed)
        
        enemies[i].changePosition(tick)
        #si un coeur touche sonic
        if enemies[i].rect.colliderect(sonicJumpRect.rect) and enemies[i].type == "heart":
            if time() - bestScoreTime > 0.5:
                playSound(healingPath, 0.1)
            if sonic1Rect.hp < 6:
                sonic1Rect.hp +=1
            healing = True
            enemiesToPop.append(i)
        #si un ennemie touche sonic ...
        elif enemies[i].rect.colliderect(sonicJumpRect.rect):
            if time() - bestScoreTime > 0.5:
                playSound(damagePath, 0.1)
            damage = True
            sonic1Rect.hp -=1
            enemiesToPop.append(i)
        #si un ennemie atteind le mur
        elif enemies[i].enemyRestriction():
            enemiesToPop.append(i)

        ####################
        #AFFICHAGE DES MOBS#
        ####################  
        if enemies[i].type != "mediumMob":
            enemies[i].display(screen)
        else:
            screen.blit(statesDuck[duckState],enemies[i].rect)
            delayGif = time() - timeGifDuck
            timeGifDuck, duckState = animateGif(0.08,2,timeGifDuck, duckState)
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
    
    ############
    #LES TEXTES#
    ############
    if lost:
        screen.blit(endSurface,endRect)
        screen.blit(scoresScreenSurface, scoresScreenRect)
        screen.blit(lastScoreSurface,lastScoreRect)
        screen.blit(bestScoreSurface,bestScoreRect)
        screen.blit(pseudoSurface, pseudoRect)
        #playMusic(mainMusic)
    elif not lost:
        scoreRect = scoreSurface.get_rect(topright=(width,10))
        screen.blit(scoreSurface,scoreRect)
        
        
    if score%100 == 0 and score !=0 and score%1000 != 0 and time() - timeScoreSound > 0.2:
        playSound(scorePath,0.03)
        timeScoreSound = time()
    elif score%1000 == 0 and score != 0 and time() - timeScoreSound > 0.2:
        playSound(score1000Path, 0.05)
        timeScoreSound = time()

    ########
    #LES PV#
    ########
    #affichage du coeur en fonction des pv de sonic
    if not lost:
        for i in range(sonic1Rect.hp):
            screen.blit(heartSurface,(heartRect[0] + i*100,heartRect[1]))


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
        timeGif, sonicState = animateGif(0.2 - acceleration / 2000 if acceleration<300 else 0.07,4,timeGif, sonicState)
    #sinon on affiche sonic standing
    else:
        if time() - endTime < 3:
            screen.fill((255,255,255))
            screen.blit(gameOverSurface,gameOverRect)
        else:
            screen.blit(statesSonic[1][sonicStandingState],(100,height - 200 - statesSonic[1][0].get_height()))
            screen.blit(restartSurface,restartRect)
            timeGif, sonicStandingState = animateGif(0.3,2,timeGif, sonicStandingState)
            screen.blit(grassSurface,grassSurface.get_rect(topright=(width,height - 200)))

    pygame.display.flip()
pygame.quit()





