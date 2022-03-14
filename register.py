from time import sleep
import pygame
from pygame.locals import *
pygame.init()
windowSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(windowSize)
width = windowSize[0]
height = windowSize[1]

logging = True
newPlayer = False
name = ""
fontPath = "font/BACKTO1982.TTF"
font = pygame.font.Font(fontPath, width // 30)
bigFont = pygame.font.Font(fontPath, 80)
nameSurface = bigFont.render("{0}".format(name), True, (0,0,0))
nameRect = nameSurface.get_rect(midtop=(width / 2, height / 2))
textSurface = font.render("Press RETURN to continue", True, (0,0,0))
textRect = textSurface.get_rect(midtop = (width/2, 50))
while logging:
    screen.fill((150,150,150))
    nameSurface = font.render("{0}".format(name), True, (0,0,0))
    nameRect = nameSurface.get_rect(midtop=(width / 2, height / 2))
    screen.blit(nameSurface, nameRect)
    screen.blit(textSurface, textRect)
    if len(name) == 0:
        name = "Type your name"
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
# while not registered:
#     name = input("Entrez votre nom\n")
#     if len(name) < 25:
#         registered = True
with open("bestScore.txt") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")

players = []
scores = []
for i in lines:
    players.append(i[0]) 
    scores.append(i[1])
    
if name not in players:
    with open('bestScore.txt', 'a') as f:
        f.write(name + " 0")
    players.append(name)
    scores.append(0)
    bestScore = 0
    newPlayer = True
    playerIndex = len(players) - 1
else:
    for i in range(len(players)):
        if players[i] == name:
            bestScore = int(scores[i])
            playerIndex = i
 