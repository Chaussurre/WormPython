"""Proof of concept gfxdraw example"""

import pygame
import pygame.gfxdraw


pygame.init()
screen = pygame.display.set_mode((1000, 600))
screen.fill((0, 0, 0))

pygame.draw.circle(screen, "green", (50, 100), 10)
pygame.draw.circle(screen, "black", (50, 100), 12, 2)
pygame.draw.circle(screen, "white", (50, 100), 15, 3)

pygame.display.flip()
try:
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == "q":
                break
        pygame.display.flip()
finally:
    pygame.quit()