from time import time
import pygame
from classes.Sonic import Sonic
pygame.init()

windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

############
#LES TIMERS#
############
#init du delais d'affichage du gif
timeGif = time()
timeGifDuck = time()
timeGifCharac = time()
#init du départ du saut
startJump = time()
timeJump = 0.4
#init du temps de spawn des mobs
timeSpawn = time()
#init temps d'effet de fond
effectTime = time()

##############
#LES BOOLEENS#
##############
#état de saut
jumping = False
preJump = False
#variable qui maintient le while du jeu
playing = True
#état de dégat pour effet visuel (fond rouge) ou heal (fond vert)
damage = False
healing = False
#état qui définit si on a perdu ou non
lost = True
#état qui définie quel image du gif on affiche
sonicState = 0
sonicStandingState = 0
#état qui définie quel image du gif on affiche
duckState = 0

############
#LES IMAGES#
############
#personnage en gif
#tableau des états de sonic : tab[0][i] -> état de saut, tab[1][i] -> état de standing
statesSonic = [[0,0,0,0],[0,0]]
statesSonic[0][0] = pygame.image.load("images/sonic1.gif").convert_alpha()
statesSonic[0][1] = pygame.image.load("images/sonic2.gif").convert_alpha()
statesSonic[0][2] = pygame.image.load("images/sonic3.gif").convert_alpha()
statesSonic[0][3] = pygame.image.load("images/sonic4.gif").convert_alpha()
statesSonic[1][0] = pygame.image.load("images/sonicStanding1.gif").convert_alpha()
statesSonic[1][1] = pygame.image.load("images/sonicStanding2.gif").convert_alpha()

#le canard en gif
statesDuck = [0,0]
statesDuck[0] = pygame.image.load("images/duck1.png").convert_alpha()
statesDuck[1] = pygame.image.load("images/duck2.png").convert_alpha()
#init des enemies
enemySpikeSurface = pygame.image.load("images/spike.png").convert_alpha()
enemyBirdSurface = pygame.image.load("images/bird.png").convert_alpha()

#sonic en saut
sonicJumpSurface = pygame.image.load("images/sonicJump.png").convert_alpha()

#le coeur
heartSurface = pygame.image.load("images/heart.png").convert_alpha()

#rock image
rockSurface = pygame.image.load("images/rock.png").convert_alpha()

######################
#LES TYPES DE CLASSES#
######################
sonicJumpRect = Sonic(sonicJumpSurface.get_rect(topleft=(100,height - 200 - 144*4)))
sonic1Rect = Sonic(statesSonic[0][0].get_rect(topleft=(100,height - 200 - 144)))

################
#LES TYPES RECT#
################
heartRect = heartSurface.get_rect(topleft=(65,65))
#rect qui restreint le personnage
sonicRect = pygame.Rect((100,200), (128,height - 400))