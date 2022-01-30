import numpy as np
import pygame
import pygame.gfxdraw

import Globals
from Physics import Trajectory
from Physics.Terrain import Terrain
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

    def UpdateDynamicObjects(self):
        for DO in Globals.listDynamicObjects:
            DO.update()

    def PrintTrajectories(self, color="red"):
        for PO in Globals.listPhysicObjects:
            if PO.trajectory is not None:
                PO.trajectory.print(color=color)

    def main(self):
        Worm(position=(200, 100), velocity=np.array((50, -50)))
        Worm(position=(550, 100), velocity=np.array((-50, -50)))
        Trajectory.UpdateTrajectories()

        terrain = self.createTerrain()

        pygame.display.flip()
        clock = pygame.time.Clock()
        try:
            while self.running:
                clock.tick(Globals.FrameRate)
                self.UpdateEvents()
                Globals.Screen.fill((0, 0, 0))
                self.PrintTrajectories()
                terrain.draw()
                self.UpdateDynamicObjects()
                pygame.display.flip()
        finally:
            pygame.quit()

    def createTerrain(self):
        terrain = Terrain()
        terrain.addNode((100, 500))
        terrain.addNode((900, 500))
        terrain.link(0, 1)
        return terrain


GameManager().main()
