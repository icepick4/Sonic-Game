"""screen of best scores"""
import pygame
from register import width, height, screen, scores

def get_scores(sorted_scores):
    """return the surfaces and rects to blit"""
    ctr = 0
    for key, value in sorted_scores:
        if ctr == 0:
            ctr_surface = big_font.render(f"{ctr+1}", True, (255,215,0))
        elif ctr == 1:
            ctr_surface = big_font.render(f"{ctr+1}", True, (192,192,192))
        elif ctr == 2:
            ctr_surface = big_font.render(f"{ctr+1}", True, (97,78,26))
        else:
            ctr_surface = big_font.render(f"{ctr+1}", True, (0,0,0))
        ctr_rect = ctr_surface.get_rect(topleft = (15, (height / 6.5) * ctr + (height / 4.5)))
        id_surface = big_font.render(f"{key}", True, (0,0,0))
        id_rect = id_surface.get_rect(topleft=(111, (height / 6.5) * ctr + (height / 4.5)))
        score_surface = big_font.render(f"{value}", True, (0,0,0))
        score_rect=score_surface.get_rect(topright=(width-15,(height/6.5)*ctr+(height / 4.5)))
        ctr+=1
        screen.blit(ctr_surface, ctr_rect)
        screen.blit(id_surface, id_rect)
        screen.blit(score_surface, score_rect)
    return True

FONTPATH = "font/BACKTO1982.TTF"
font = pygame.font.Font(FONTPATH, width // 30)
big_font = pygame.font.Font(FONTPATH, 80)

def screen_scores(looping):
    """lauching screen of scores"""
    exit_surface = big_font.render("EXIT", True, (0,0,0))
    exit_rect = exit_surface.get_rect(topleft=(10,10))
    while looping:
        screen.fill((150,150,150))
        for event in pygame.event.get():
            if event.type == 256:
                looping = False
            elif event.type == 1024:
                width_restriction = exit_rect.left < event.pos[0] < exit_rect.right
                height_restriction = exit_rect.top < event.pos[1] < exit_rect.bottom
                if width_restriction and height_restriction:
                    exit_surface = big_font.render("EXIT", True, (255,60,60))
                else:
                    exit_surface = big_font.render("EXIT", True, (0,0,0))
            elif event.type == 1025 and event.button == 1:
                if width_restriction and height_restriction:
                    looping = False
        screen.blit(exit_surface, exit_rect)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores[0:5]
        get_scores(sorted_scores)
        pygame.display.flip()
    return True
