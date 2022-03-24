import pygame
from pygame.locals import *
from variables import scores, bigFont, width, height, screen, exitSurface, exitRect


def ScreenScores(looping):
    exitSurface = bigFont.render("EXIT", True, (0,0,0))
    while looping:
        ctr = 0
        screen.fill((150,150,150))
        for event in pygame.event.get():
            if event.type == QUIT:
                looping = False
            elif event.type == pygame.MOUSEMOTION:
                if exitRect.left < event.pos[0] < exitRect.right and exitRect.top < event.pos[1] < exitRect.bottom:
                    exitSurface = bigFont.render("EXIT", True, (255,60,60))
                else:
                    exitSurface = bigFont.render("EXIT", True, (0,0,0))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exitRect.left < event.pos[0] < exitRect.right and exitRect.top < event.pos[1] < exitRect.bottom:
                    looping = False
        screen.blit(exitSurface, exitRect)

        sortedScores = sorted(scores.items(), key=lambda x: x[1], reverse=True)  
        sortedScores = sortedScores[0:5] 
        
        for key, value in sortedScores:
            if ctr == 0:
                ctrSurface = bigFont.render("{}".format(ctr +1), True, (255,215,0))
            elif ctr == 1:
                ctrSurface = bigFont.render("{}".format(ctr +1), True, (192,192,192))
            elif ctr == 2:
                ctrSurface = bigFont.render("{}".format(ctr +1), True, (97,78,26))
            else:
                ctrSurface = bigFont.render("{}".format(ctr +1), True, (0,0,0))

            ctrRect = ctrSurface.get_rect(topleft = (15, (height / 5) * ctr + (height / 5) / 2))

            nameSurface = bigFont.render("{}".format(key), True, (0,0,0))
            nameRect = nameSurface.get_rect(topleft=(111, (height / 5) * ctr + (height / 5) / 2))

            scoreSurface = bigFont.render("{}".format(value), True, (0,0,0))
            scoreRect = scoreSurface.get_rect(topright=(width - 15, (height / 5) * ctr + (height / 5) / 2))

            screen.blit(ctrSurface, ctrRect)
            screen.blit(nameSurface, nameRect)
            screen.blit(scoreSurface, scoreRect)
            ctr +=1
        pygame.display.flip()
    return True



