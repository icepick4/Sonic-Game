"""registration page"""
from time import time
import pickle
import pygame

pygame.display.init()
window_size = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(window_size)
width = window_size[0]
height = window_size[1]

LOGGING = True
NEWPLAYER = True
NAMEID = ""
FONTPATH = "font/BACKTO1982.TTF"
pygame.font.init()
font = pygame.font.Font(FONTPATH, width // 30)
big_font = pygame.font.Font(FONTPATH, 80)
name_surface = big_font.render(f"{NAMEID}", True, (0,0,0))
name_rect = name_surface.get_rect(midtop=(width / 2, height / 2))
text_surface = font.render("Press RETURN to continue", True, (0,0,0))
text_rect = text_surface.get_rect(midtop = (width/2, 50))
cursor_surface = font.render("-", True, (50,50,50))
cursor_rect = cursor_surface.get_rect(topleft=(name_rect.topright))
cursor_time = time()
while LOGGING:
    cursor_rect = cursor_surface.get_rect(topleft = (name_rect.topright))
    screen.fill((150,150,150))
    name_surface = font.render(f"{NAMEID}", True, (0,0,0))
    name_rect = name_surface.get_rect(midtop=(width / 2, height / 2))
    screen.blit(name_surface, name_rect)

    if int(((time()))*2.2)%2 == 0 and len(NAMEID) < 20:
        screen.blit(cursor_surface, cursor_rect)
        cursor_time = time()
    if len(NAMEID) == 0:
        NAMEID = "Type your name"
    if NAMEID != "Type your name":
        screen.blit(text_surface, text_rect)
    for event in pygame.event.get():
        if event.type == 256:
            PLAYING = False
            LOGGING = False
        elif event.type == 768:
            if (event.unicode.isalpha() or event.unicode.isnumeric()) and len(NAMEID) < 20:
                if NAMEID == "Type your name":
                    NAMEID = ""
                NAMEID += event.unicode
            elif event.key == 8:
                if NAMEID != "Type your name":
                    NAMEID = NAMEID[0:len(NAMEID)-1]
            elif event.key in (13,1073741912) and len(NAMEID) > 0 and NAMEID != "Type your name":
                PLAYING = True
                LOGGING = False
    pygame.display.flip()


REGISTERED = False
#init du bestscore
SCORE = 0
try:
    with open("bestScore.pickle", "rb") as f:
        scores = pickle.load(f)
except FileNotFoundError:
    scores = {}
    with open("bestScore.pickle", "wb") as f:
        pickle.dump(scores, f)

for key,value in scores.items():
    if key == NAMEID:
        NEWPLAYER = False
        BESTSCORE = value
if NEWPLAYER:
    BESTSCORE = 0
