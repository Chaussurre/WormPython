import pygame
import pygame.gfxdraw
from Worm import Worm
from Input import Input

class GameManager:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.screen.fill((0, 0, 0))

        self.listDOs = []

    def main(self):
        Worm.Worm(self.screen, self.listDOs, position=(30, 30))

        pygame.display.flip()
        clock = pygame.time.Clock()
        running = True
        try:
            while running:
                clock.tick(60)
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
                for DO in self.listDOs:
                    if DO.rect is not None:
                        pygame.draw.rect(self.screen, (0, 0, 0), DO.rect)

                # Draw all dynamic objects
                for DO in self.listDOs:
                    DO.update()

                pygame.display.flip()
        finally:
            pygame.quit()


GameManager().main()
