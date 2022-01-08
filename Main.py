import pygame
import pygame.gfxdraw

import Globals
from Worm.Worm import Worm
from Input import Input

class GameManager:

    def __init__(self):
        pygame.init()
        Globals.Screen = pygame.display.set_mode((1000, 600))
        Globals.Screen.fill((0, 0, 0))


    def main(self):
        Worm(position=(100, 100), velocity=(50, -50))

        pygame.display.flip()
        clock = pygame.time.Clock()
        running = True
        try:
            while running:
                clock.tick(Globals.FrameRate)
                Input.UpdateKeys()
                event = pygame.event.poll()
                while event.type != pygame.NOEVENT:
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        Input.SetKeyDown(event.key)
                    if event.type == pygame.KEYUP:
                        Input.SetKeyUp(event.key)
                    event = pygame.event.poll()

                # Remove all the space used by dynamic objects
                for DO in Globals.listDynamicObjects:
                    if DO.rect is not None:
                        pygame.draw.rect(Globals.Screen, (0, 0, 0), DO.rect)

                # Draw all dynamic objects
                for DO in Globals.listDynamicObjects:
                    DO.update()

                pygame.display.flip()
        finally:
            pygame.quit()


GameManager().main()
