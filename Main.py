import pygame
import pygame.gfxdraw

import Globals
from Worm.Worm import Worm
from Input import Input

class GameManager:

    def __init__(self):
        self.running = True
        pygame.init()
        Globals.Screen = pygame.display.set_mode((1000, 600))
        Globals.Screen.fill((0, 0, 0))

    def UpdateEvents(self):
        Input.UpdateKeys()
        event = pygame.event.poll()
        while event.type != pygame.NOEVENT:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                Input.SetKeyDown(event.key)
            if event.type == pygame.KEYUP:
                Input.SetKeyUp(event.key)
            event = pygame.event.poll()

    # Remove from the screen all the space used by dynamic objects
    def ClearDynamicObjects(self):
        for DO in Globals.listDynamicObjects:
            if DO.rect is not None:
                pygame.draw.rect(Globals.Screen, (0, 0, 0), DO.rect)

    def UpdateDynamicObjects(self):
        for DO in Globals.listDynamicObjects:
            DO.update()

    def main(self):
        Worm(position=(100, 100), velocity=(50, -50))

        pygame.display.flip()
        clock = pygame.time.Clock()
        try:
            while self.running:
                clock.tick(Globals.FrameRate)
                self.UpdateEvents()

                self.ClearDynamicObjects()

                self.UpdateDynamicObjects()

                pygame.display.flip()
        finally:
            pygame.quit()


GameManager().main()
