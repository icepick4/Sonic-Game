"""main page"""
from time import time
from random import randint,uniform
from register import (
                        width,
                        height,
                        NAMEID,
                        BESTSCORE,
                        pickle,
                        screen,
                        PLAYING,
                        SCORE,
                        scores
)
from variables import (
                        end_rect,
                        scores_screen_rect,
                        end_font,
                        sonic_jump_rect,
                        JUMPPATH,
                        sonic_1_rect,
                        enemies,
                        rock_surface,
                        states_duck,
                        enemy_bird_surface,
                        enemy_spike_surface,
                        heart_surface,
                        timer,
                        score_live_font,
                        BESTSCOREPATH,
                        LOSTPATH,
                        score_font,
                        grass_2_rect,
                        grass_rect,
                        cloud_2_rect,
                        cloud_rect,
                        palm_2_rect,
                        palm_rect,
                        HEALINGPATH,
                        DAMAGEPATH,
                        DAMAGE,
                        last_score_rect,
                        best_score_rect,
                        pseudo_surface,
                        pseudo_rect,
                        TIMEJUMP,
                        SCOREPATH,
                        SCORE1000PATH,
                        sonic_rect,
                        sonic_jump_surface,
                        heart_rect,
                        states_sonic,
                        game_over_rect,
                        game_over_surface,
                        restart_rect,
                        restart_surface,
                        grass_surface,
                        HEALING,
                        best_score_time,
                        end_time,
                        DUCKSTATE,
                        effect_time,
                        BESTSCOREBEATEN,
                        SONICSTATE,
                        time_gif,
                        SONICSTANDINGSTATE,
                        LOST,
                        time_spawn,
                        start_jump,
                        end_surface,
                        scores_screen_surface,
                        last_score_surface,
                        best_score_surface,
                        JUMPING,
                        time_gif_duck,
                        time_score_sound

)
from high_scores_screen import screen_scores
try:
    import pygame
except ModuleNotFoundError:
    print("""Vous n'avez pas téléchargé le module pygame ! \n
        Téléchargez le avec la commande ci-contre : pip install pygame""")
from functions import animate_gif, play_sound
from classes.enemy import Enemy

while PLAYING:
    ACCELERATION = SCORE / 2
    ACCELERATION = min(ACCELERATION, 666)
    #####################
    #ACTIONS DES TOUCHES#
    #####################
    for event in pygame.event.get():
        state_game = LOST and time() - end_time > 3
        if event.type == 256:
            PLAYING = False
        elif event.type == 1024:
            width_restrict = end_rect.left < event.pos[0] < end_rect.right
            height_restrict = end_rect.top < event.pos[1] < end_rect.bottom
            score_w_restrict = scores_screen_rect.left < event.pos[0] < scores_screen_rect.right
            score_h_restrict = scores_screen_rect.top < event.pos[1] < scores_screen_rect.bottom
            if width_restrict and height_restrict and state_game:
                end_surface = end_font.render("CLOSE", True, (255,60,60))
            else:
                end_surface = end_font.render("CLOSE", True, (0,0,0))
            if score_w_restrict and score_h_restrict and state_game:
                scores_screen_surface = end_font.render("HIGHSCORES", True, (255,60,60))
            else:
                scores_screen_surface = end_font.render("HIGHSCORES", True, (0,0,0))
        elif event.type == 1025 and event.button == 1 :
            #on presse le bouton close
            if width_restrict and height_restrict and state_game:
                PLAYING = False
            #on presse le bouton highscores
            if score_w_restrict and score_h_restrict and state_game:
                PLAYING = screen_scores(True)
        elif event.type == 768:
            if event.key == 32 and time() - end_time > 3:
                #on peut sauter
                if sonic_jump_rect.on_floor():
                    start_jump = time()
                    JUMPING = True
                    sonic_jump_rect.change_speed((0,1300 - ACCELERATION / 2.5))
                    if time() - best_score_time > 0.5:
                        play_sound(JUMPPATH, 0.02)
                if LOST:
                    LOST = False
                    score_timer = time()
                    SCORE = 0
        elif event.type == 769:
            if event.key == 32:
                if ACCELERATION > 500:
                    FALLINGSPEED = 500
                else:
                    FALLINGSPEED = ACCELERATION
                sonic_jump_rect.change_speed((0,-500 - FALLINGSPEED / 1.3))
    ################
    #SPAWN DES MOBS#
    ################
    #on fait spawn les mobs, avec un délais qui empêche les situations impossibles
    mobs_speed = 850 + ACCELERATION
    delay_mobs = 150 * 4.8/mobs_speed
    if time() >= time_spawn+delay_mobs+uniform(-0.05,0.7) and not LOST:
        rand = randint(1,10)
        EASTEREGG = -1
        try:
            CHECKHEART = enemies[len(enemies)-1].category != "heart"
            CHECKHEART2 = enemies[len(enemies)-2].category != "heart"
        except IndexError:
            CHECKHEART = False
        if sonic_1_rect.health == 1:
            random_heart = randint(1,25)
            EASTEREGG = randint(1,1000)
        elif sonic_1_rect.health == 2:
            random_heart = randint(1,55)
        elif sonic_1_rect.health == 3:
            random_heart = randint(1,100)
        if sonic_1_rect.health == 4:
            random_heart = randint(1,200)
        if rand <= 7:
            if 0 < rand <= 2:
                enemies.append(Enemy(
                                    rock_surface.get_rect(topleft=(
                                                                    width,
                                                                    height - 200)
                                                                ),
                                    rock_surface, "littleMob")
                                )
            elif 2 < rand <= 4:
                print(type(states_duck[DUCKSTATE]))
                enemies.append(Enemy(
                                    states_duck[DUCKSTATE].get_rect(topleft=(
                                                                        width,
                                                                        height - 200)
                                                                        ),
                                    states_duck[DUCKSTATE], "mediumMob")
                                )
            else:
                enemies.append(Enemy(
                                    enemy_spike_surface.get_rect(topleft=(
                                                                        width,
                                                                        height - 200)
                                                                        ),
                                    enemy_spike_surface,  "bigMob")
                                )
        else:
            enemies.append(Enemy(
                                enemy_bird_surface.get_rect(topleft=(
                                                                    width,
                                                                    300
                                                                    )
                                                                ),
                                enemy_bird_surface, "flyingMob")
                            )
        if random_heart == 1 and CHECKHEART and CHECKHEART2:
            enemies.append(Enemy(
                                heart_surface.get_rect(topleft=(
                                                                width,
                                                                height - randint(200,700)
                                                                )
                                                            ),
                                heart_surface, "heart")
                            )
        if EASTEREGG == 1:
            for i in range(4):
                enemies.append(Enemy(heart_surface.get_rect(topleft=(
                                                                    width,
                                                                    height - randint(200,700)
                                                                    )
                                                            ),
                                    heart_surface, "heart")
                                )
        time_spawn = time()

    #tick de la frame
    tick = timer.tick(200) / 1000
    ###################################
    #LES FONDS --> LES DEGATS ET HEALS#
    ###################################
    #on affiche l'effet visuel de dégats(fond rouge)
    #pendant 0.25s, et de HEALING (fond vert) (default : blanc)
    effect_delay = time() - effect_time
    if DAMAGE and effect_delay < 0.25:
        screen.fill((255,100,100))
    elif HEALING and effect_delay < 0.25:
        screen.fill((100,255,100))
    else:
        screen.fill((135,206,235))
        effect_time = time()
        DAMAGE = False
        HEALING = False
    ##################
    #j'essaye de mettre un grass en fond constamment pour cacher le trou du défilement, c'est moche
    #screen.blit(grassSurface,(0,height - 200))

    ############
    #LES SCORES#
    ############
    #si on a pas perdu on affiche le score actuel, sinon le last score
    if not LOST:
        SCORE = int(round((time() - score_timer) * 10,0))
        if BESTSCOREBEATEN:
            score_surface = score_live_font.render(f"{SCORE}", True, (255,195,36))
        else:
            score_surface = score_live_font.render(f"{SCORE}", True, (0,0,0))
    if BESTSCORE < SCORE :
        BESTSCORE = SCORE
        if not BESTSCOREBEATEN:
            play_sound(BESTSCOREPATH, 0.05)
            best_score_time = time()
        BESTSCOREBEATEN = True
    ############
    #ON A PERDU#
    ############
    if sonic_1_rect.health == 0:
        for i in range(len(enemies)):
            enemies.pop(0)
        LOST = True
        BESTSCOREBEATEN = False
        LASTSCORE = SCORE
        last_score_surface = score_font.render(f"Last score : {LASTSCORE}", True, (0,0,0))
        best_score_surface = score_font.render(f"Best score : {BESTSCORE}", True, (0,0,0))
        sonic_1_rect.health = 3
        play_sound(LOSTPATH,0.06)
        end_time = time()
        scores[NAMEID] = BESTSCORE
        with open ("best_score.pickle", "wb") as f:
            pickle.dump(scores, f)

    ############
    #LES DECORS#
    ############
    if not LOST:
        grass_rect.animate(mobs_speed, 0, tick, screen)
        grass_2_rect.animate(mobs_speed, 0, tick, screen)
        cloud_rect.animate(620,0, tick, screen)
        cloud_2_rect.animate(550,0, tick, screen)
        palm_rect.animate(475,0, tick, screen)
        palm_2_rect.animate(475,0, tick, screen)
    else:
        cloud_rect.animate(160,0, tick, screen)
        cloud_2_rect.animate(70,0, tick, screen)
        palm_rect.position = (width / 4, height - 200)
        palm_2_rect.position = (width / 1.3, height - 200)
        palm_rect.animate(0,0, tick, screen)
        palm_2_rect.animate(0,0, tick, screen)

    ##############
    #LES ENNEMIES#
    ##############
    enemies_to_pop = []
    for enemy in enemies:
        if not enemy.moving():
            enemy.run(mobs_speed)
        enemy.change_position(tick)
        #si un coeur touche sonic
        if enemy.rect.colliderect(sonic_jump_rect.rect) and enemy.category == "heart":
            if time() - best_score_time > 0.5:
                play_sound(HEALINGPATH, 0.1)
            if sonic_1_rect.health < 6:
                sonic_1_rect.health +=1
            HEALING = True
            enemies_to_pop.append(enemies.index(enemy))
        #si un ennemie touche sonic ...
        elif enemy.rect.colliderect(sonic_jump_rect.rect):
            if time() - best_score_time > 0.5:
                play_sound(DAMAGEPATH, 0.1)
            DAMAGE = True
            sonic_1_rect.health -=1
            enemies_to_pop.append(enemies.index(enemy))
        #si un ennemie atteind le mur
        elif enemy.enemy_restriction():
            enemies_to_pop.append(enemies.index(enemy))

        ####################
        #AFFICHAGE DES MOBS#
        ####################
        if enemy.category != "mediumMob":
            enemy.display(screen)
        else:
            screen.blit(states_duck[DUCKSTATE],enemy.rect)
            delay_gif = time() - time_gif_duck
            time_gif_duck, DUCKSTATE = animate_gif(0.08,2,time_gif_duck, DUCKSTATE)
    for i in enemies_to_pop:
        enemies.pop(i)

    #################
    #GESTION DU SAUT#
    #################
    #si on est en cours de saut -> on change la position, sinon on redescend
    if time() - start_jump < TIMEJUMP:
        sonic_jump_rect.change_position(tick)
    else:
        sonic_jump_rect.change_speed((0,-1300 - ACCELERATION))
        start_jump = time()
    ############
    #LES TEXTES#
    ############
    if LOST:
        screen.blit(end_surface,end_rect)
        screen.blit(scores_screen_surface, scores_screen_rect)
        screen.blit(last_score_surface,last_score_rect)
        screen.blit(best_score_surface,best_score_rect)
        screen.blit(pseudo_surface, pseudo_rect)
        #playMusic(mainMusic)
    elif not LOST:
        score_rect = score_surface.get_rect(topright=(width,10))
        screen.blit(score_surface,score_rect)

    if SCORE%100 == 0 and SCORE !=0 and SCORE%1000 != 0 and time() - time_score_sound > 0.2:
        play_sound(SCOREPATH,0.03)
        time_score_sound = time()
    elif SCORE%1000 == 0 and SCORE != 0 and time() - time_score_sound > 0.2:
        play_sound(SCORE1000PATH, 0.05)
        time_score_sound = time()

    ########
    #LES PV#
    ########
    #affichage du coeur en fonction des pv de sonic
    if not LOST:
        for i in range(sonic_1_rect.health):
            screen.blit(heart_surface,(heart_rect[0] + i*100,heart_rect[1]))


    ####################
    #AFFICHAGE DU PERSO#
    ####################
    #on restreint les positions de sonic
    sonic_jump_rect.sonic_pos_restriction(sonic_rect)
    #si la speed est passé à 0 -> le saut n'est plus actif
    if sonic_jump_rect.speed[1] == 0:
        JUMPING = False

    if sonic_jump_rect.speed[1] < 0:
        sonic_jump_rect.change_speed((0,-50))

    #si on saute on affiche sonicJump
    if JUMPING and not LOST:
        sonic_jump_rect.change_speed((0,-3))
        screen.blit(sonic_jump_surface, sonic_jump_rect.rect)
    #si on a pas perdu on affiche le gif sonic qui court
    elif not LOST:
        #affichage du gif à la main
        screen.blit(states_sonic[0][SONICSTATE],(100,height - 200 - 144))
        speed_gif = 0.2 - ACCELERATION / 2000 if ACCELERATION<300 else 0.07
        time_gif, SONICSTATE = animate_gif(speed_gif,4,time_gif, SONICSTATE)
    #sinon on affiche sonic standing
    else:
        if time() - end_time < 3:
            screen.fill((255,255,255))
            screen.blit(game_over_surface,game_over_rect)
        else:
            screen.blit(
                        states_sonic[1][SONICSTANDINGSTATE],
                        (100,height - 200 - states_sonic[1][0].get_height())
                    )
            screen.blit(restart_surface,restart_rect)
            time_gif, SONICSTANDINGSTATE = animate_gif(0.3,2,time_gif, SONICSTANDINGSTATE)
            screen.blit(grass_surface,grass_surface.get_rect(topright=(width,height - 200)))
    pygame.display.flip()
pygame.display.quit()
