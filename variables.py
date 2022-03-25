"""variables init"""
from time import time
from random import randint
import pygame
from sonic import Sonic
from environment import Environment
from register import width, height, BESTSCORE, NAMEID


############
#LES TIMERS#
############
#init du delais d'affichage du gif
time_gif = time()
time_gif_duck = time()
time_gif_charac = time()
#init du départ du saut
start_jump = time()
TIMEJUMP = 0.4
#init du temps de spawn des mobs
time_spawn = time()
#init temps d'effet de fond
effect_time = time()
time_score_sound = time()
#timer pour obtenir les ticks
timer = pygame.time.Clock()
end_time = time() - 3
best_score_time = time()
##############
#LES BOOLEENS#
##############
#état de saut
JUMPING = False
FALLING = False
#variable qui maintient le while du jeu
#état de dégat pour effet visuel (fond rouge) ou heal (fond vert)
DAMAGE = False
HEALING = False
BESTSCOREBEATEN = False
#état qui définit si on a perdu ou non
LOST = True
HIGHSCORES = True
#état qui définie quel image du gif on affiche
SONICSTATE = 0
SONICSTANDINGSTATE = 0
#état qui définie quel image du gif on affiche
DUCKSTATE = 0

############
#LES IMAGES#
############
#personnage en gif
#tableau des états de sonic : tab[0][i] -> état de saut, tab[1][i] -> état de standing
states_sonic = [[],[]]
states_sonic[0].append(pygame.image.load("images/sonic1.gif").convert_alpha())
states_sonic[0].append(pygame.image.load("images/sonic2.gif").convert_alpha())
states_sonic[0].append(pygame.image.load("images/sonic3.gif").convert_alpha())
states_sonic[0].append(pygame.image.load("images/sonic4.gif").convert_alpha())
states_sonic[1].append(pygame.image.load("images/sonicStanding1.gif").convert_alpha())
states_sonic[1].append(pygame.image.load("images/sonicStanding2.gif").convert_alpha())

#le canard en gif
states_duck = []
states_duck.append(pygame.image.load("images/duck1.png").convert_alpha())
states_duck.append(pygame.image.load("images/duck2.png").convert_alpha())
#init des enemies
enemy_spike_surface = pygame.image.load("images/spike.png").convert_alpha()
enemy_bird_surface = pygame.image.load("images/bird.png").convert_alpha()
rock_surface = pygame.image.load("images/rock.png").convert_alpha()
enemies = []
#sonic en saut
sonic_jump_surface = pygame.image.load("images/sonicJump.png").convert_alpha()

#le coeur
heart_surface = pygame.image.load("images/heart.png").convert_alpha()

grass_surface = pygame.image.load("images/grass.png").convert_alpha()
grass_rect = Environment(grass_surface.get_rect(topleft=(0,height)), grass_surface,"grass")
grass_2_rect = Environment(grass_surface.get_rect(topleft=(width,height)), grass_surface,"grass")
cloud_surface = pygame.image.load("images/cloud.png").convert_alpha()
cloud_rect = Environment(cloud_surface.get_rect(
                                                topleft=(
                                                        width + randint(0,500),
                                                        randint(200,height / 2)
                                                        )
                                                ),
                                                cloud_surface, "cloud1"
                                            )
cloud_2_rect = Environment(cloud_surface.get_rect(
                                                topleft=(
                                                        width + randint(0,500),
                                                        randint(200,height / 2)
                                                        )
                                                    ),
                                                cloud_surface ,"cloud2"
                                            )
cloud_rect.speed = (620,0)
cloud_2_rect.speed = (550,0)

palm_surface = pygame.image.load("images/palm-min.png").convert_alpha()
palm_2_surface = pygame.image.load("images/palm2-min.png").convert_alpha()
palm_rect = Environment(palm_surface.get_rect(
                                            topleft=(
                                                    width+randint(0,500),
                                                    height - 200
                                                    )
                                                ),
                                                palm_surface, "palm1"
                                            )
palm_2_rect = Environment(palm_2_surface.get_rect(
                                                topleft=(
                                                        width + randint(1000,2500),
                                                        height - 200
                                                        )
                                                    ),
                                                    palm_2_surface, "palm2"
                                            )
palm_2_rect.speed = (475,0)
palm_rect.speed = (475,0)
######################
#LES TYPES DE CLASSES#
######################
sonic_jump_rect = Sonic(sonic_jump_surface.get_rect(topleft=(100,height - 200 - 144*4)))
sonic_1_rect = Sonic(states_sonic[0][0].get_rect(topleft=(100,height - 200 - 144)))
################
#LES TYPES RECT#
################
heart_rect = heart_surface.get_rect(topleft=(65,65))
#rect qui restreint le personnage
sonic_rect = pygame.Rect((100,200), (128,height - 400))

##########
#LES SONS#
##########
HEALINGPATH = "sounds/healing.wav"
JUMPPATH = "sounds/jump.mp3"
DAMAGEPATH = "sounds/damage.wav"
LOSTPATH = "sounds/lost.wav"
SCOREPATH = "sounds/score.wav"
SCORE1000PATH = "sounds/best_score.wav"
BESTSCOREPATH = "sounds/best_score.wav"
MAINMUSIC = "sounds/mainMusic.wav"
####################
#TEXTES SUR L'ECRAN#
####################

scoreTimer = time()
FONTPATH = "font/BACKTO1982.TTF"
score_font = pygame.font.Font(FONTPATH, 40)
big_font = pygame.font.Font(FONTPATH, width // 30)
score_live_font = pygame.font.Font(FONTPATH, 150)
score_surface = score_live_font.render("0", True, (0,0,0))
last_score_surface = score_font.render(f"Last score : {0}", True, (0,0,0))
last_score_rect = last_score_surface.get_rect(midtop=(width/2, 100))
best_score_surface = score_font.render(f"Best score : {BESTSCORE}", True, (0,0,0))
best_score_rect = best_score_surface.get_rect(midtop=(width/2, 25))
restart_surface = big_font.render("PRESS SPACE TO START", True, (255,10,10))
restart_rect = restart_surface.get_rect(midtop=(width/2,height/2))

#bouton pour fermer la fenetre
end_font = pygame.font.Font(FONTPATH, 50)
end_surface = end_font.render("CLOSE", True, (0,0,0))
end_rect = end_surface.get_rect(topright=(width - 10,10))

#bouton best_scores screen
scores_screen_surface = end_font.render("HIGHSCORES", True, (0,0,0))
scores_screen_rect = scores_screen_surface.get_rect(topright=(width - 10,75))
#écran de fin
game_over_surface = score_live_font.render("GAME OVER", True, (0,0,0))
game_over_rect = game_over_surface.get_rect(
                                            midtop = (
                                                    width / 2,
                                                    height / 2 - game_over_surface.get_size()[1] / 2
                                                    )
                                            )
#pseudo
pseudo_font = pygame.font.Font(FONTPATH, int(width // 3 // len(NAMEID)))
pseudo_surface = pseudo_font.render(f"{NAMEID}", True, (0,0,0))
pseudo_rect = pseudo_surface.get_rect(topleft = (30,30))

#background music
pygame.mixer.init()
pygame.mixer.music.load("sounds/mainMusic.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.18)
