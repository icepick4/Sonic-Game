from time import time
import pygame
import pickle
from pygame.locals import *
pygame.init()
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

logging = True
newPlayer = True
name = ""
fontPath = "font/BACKTO1982.TTF"
font = pygame.font.Font(fontPath, width // 30)
bigFont = pygame.font.Font(fontPath, 80)
nameSurface = bigFont.render("{0}".format(name), True, (0,0,0))
nameRect = nameSurface.get_rect(midtop=(width / 2, height / 2))
textSurface = font.render("Press RETURN to continue", True, (0,0,0))
textRect = textSurface.get_rect(midtop = (width/2, 50))
cursorSurface = font.render("-", True, (50,50,50))
cursorRect = cursorSurface.get_rect(topleft=(nameRect.topright))
cursorTime = time()
while logging:
    
    cursorRect = cursorSurface.get_rect(topleft = (nameRect.topright))
    screen.fill((150,150,150))
    nameSurface = font.render("{0}".format(name), True, (0,0,0))
    nameRect = nameSurface.get_rect(midtop=(width / 2, height / 2))
    screen.blit(nameSurface, nameRect)

    if int(((time()))*2.2)%2 == 0 and len(name) < 20:
        screen.blit(cursorSurface, cursorRect)
        cursorTime = time()
    if len(name) == 0:
        name = "Type your name"
    if name != "Type your name":
        screen.blit(textSurface, textRect)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            logging = False
        elif event.type == KEYDOWN:
            if (event.unicode.isalpha() or event.unicode.isnumeric()) and len(name) < 20:
                if name == "Type your name":
                    name = ""
                name += event.unicode
            elif event.key == K_BACKSPACE:
                if name != "Type your name":
                    name = name[0:len(name)-1]
            elif (event.key == K_RETURN  or event.key == K_KP_ENTER) and len(name) > 0 and name != "Type your name":
                playing = True
                logging = False
    pygame.display.flip()


registered = False
#init du bestscore
score = 0
try:
    with open("bestScore.pickle", "rb") as f:
        scores = pickle.load(f)
except:
    scores = {}
    with open("bestScore.pickle", "wb") as f:
        pickle.dump(scores, f)

for key,value in scores.items():
    if key == name:
        newPlayer = False
        bestScore = value
if newPlayer:
    bestScore = 0
 