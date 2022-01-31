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
        self.time = 0
        self.endSimTime = 0
        self.inputMode = False
        self.listWorms = []
        self.focusedWorm = 0
        pygame.init()
        Globals.Screen = pygame.display.set_mode(Globals.ScreenSize)
        pygame.display.set_caption("Best worm game", "")
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
            DO.update(self.time)

    def PrintTrajectories(self, time=0, color="red"):
        for PO in Globals.listPhysicObjects:
            if PO.trajectory is not None:
                PO.trajectory.print(time, color=color)

    def main(self):
        Globals.Terrain = self.createTerrain()

        self.addWorm(position=np.array((300, 450)))

        pygame.display.flip()
        clock = pygame.time.Clock()
        self.setSimMode()

        try:
            while self.running:
                clock.tick(Globals.FrameRate)
                self.UpdateEvents()
                Globals.Screen.fill((0, 0, 0))
                Globals.Terrain.draw()
                if self.inputMode:
                    self.runInputMode()
                else:
                    self.runSimMode()
                pygame.display.flip()
        finally:
            pygame.quit()

    def createTerrain(self):
        terrain = Terrain()
        terrain.addNode((210, 500))
        terrain.addNode((900, 500))
        terrain.link(0, 1)
        return terrain

    def setSimMode(self):
        self.inputMode = False
        self.endSimTime = Trajectory.UpdateTrajectories()

    def runSimMode(self):
        self.PrintTrajectories(self.time)
        self.UpdateDynamicObjects()
        self.time += 1.0 / Globals.FrameRate
        if self.time >= self.endSimTime:
            self.setInputMode()

    def setInputMode(self):
        for x in Globals.listPhysicObjects:
            x.trajectory = None
        self.inputMode = True
        self.time = 0
        print("ready for inputs")


    def runInputMode(self):
        if len(self.listWorms) == 0:
            return

        self.UpdateDynamicObjects()

        worm = self.listWorms[self.focusedWorm]
        if worm.inputMove():
            self.setSimMode()

    def addWorm(self, position):
        self.listWorms.append(Worm(position))


GameManager().main()
