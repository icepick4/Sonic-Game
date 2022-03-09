from time import time
import pygame
from classes.Sonic import Sonic
pygame.init()
pygame.mixer.set_num_channels(8)

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
#timer pour obtenir les ticks
timer = pygame.time.Clock()

##############
#LES BOOLEENS#
##############
#état de saut
jumping = False
falling = False
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
rockSurface = pygame.image.load("images/rock.png").convert_alpha()
enemies = []
#sonic en saut
sonicJumpSurface = pygame.image.load("images/sonicJump.png").convert_alpha()

#le coeur
heartSurface = pygame.image.load("images/heart.png").convert_alpha()



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

##########
#LES SONS#
##########
healingPath = "sounds/healing.wav"
jumpPath = "sounds/jump.mp3"
damagePath = "sounds/damage.wav"
lostPath = "sounds/lost.wav"
end = pygame.mixer.Channel(5)
####################
#TEXTES SUR L'ECRAN#
####################
#init du score, du bestscore, et du lastscore
score = 0
with open("bestScore.txt") as f:
    bestScore = int(f.readline())
scoreTimer = time()
scoreFont = pygame.font.SysFont("Courier New", 50)
bigFont = pygame.font.SysFont("Courier New", 75)
scoreLiveFont = pygame.font.SysFont("Courier New", 200)
scoreSurface = scoreLiveFont.render("{0}".format(0), True, (0,0,0))
lastScoreSurface = scoreFont.render("Last score : {0}".format(0), True, (0,0,0))
lastScoreRect = lastScoreSurface.get_rect(midtop=(width/2, 100))
bestScoreSurface = scoreFont.render("Best score : {0}".format(bestScore), True, (0,0,0))
bestScoreRect = bestScoreSurface.get_rect(midtop=(width/2, 25))
restartSurface = bigFont.render("PRESS SPACE TO START", True, (255,10,10))
restartRect = restartSurface.get_rect(midtop=(width/2,height/2))

#bouton pour fermer la fenetre
endFont = pygame.font.SysFont("Courier New", 50)
endSurface = endFont.render("CLOSE", True, (0,0,0))
endRect = endSurface.get_rect(topleft=(windowSize[0]-180,10))

gameOverSurface = pygame.transform.smoothscale(pygame.image.load("images/gameOver.png").convert_alpha(),(width,height))
gameOverRect = (0,0)




