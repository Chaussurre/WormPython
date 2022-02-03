import numpy as np
import pygame
import pygame.gfxdraw

import Globals
from Input import Input
from Physics.Terrain import Terrain
from TurnPhases.MoveWormPhase import MoveWormPhase
from TurnPhases.RunSim import RunSim
from TurnPhases.WeaponAimPhase import WeaponAimPhase
from UI import UIGlobals
from UI.UILayout import InitUI
from Worm.Worm import Worm


class GameManager:

    def __init__(self):
        Globals.MainGame = self
        self.running = True
        self.turnPhase = None
        self.listWorms = []
        self.focusedWorm = 0
        pygame.init()
        Globals.Screen = pygame.display.set_mode(Globals.ScreenSize)
        pygame.display.set_caption("Best worm game", "")
        Globals.Screen.fill((0, 0, 0))

    @property
    def movingWorm(self):
        return self.listWorms[self.focusedWorm]

    def main(self):
        Globals.Terrain = self.createTerrain()
        self.addWorm(position=np.array((150, 300)), team="green")
        self.addWorm(position=np.array((350, 300)), team="purple")
        self.addWorm(position=np.array((450, 300)), team="green")
        self.addWorm(position=np.array((650, 300)), team="purple")

        clock = pygame.time.Clock()
        self.turnPhase = RunSim()
        try:
            while self.running:
                clock.tick(Globals.FrameRate)
                self.updateEvents()
                Globals.Screen.fill((0, 0, 0))
                Globals.Terrain.draw()
                self.playTurnPhase()
                UIGlobals.RootUI.drawUI()
                pygame.display.flip()
        finally:
            pygame.quit()

    def playTurnPhase(self):
        if self.turnPhase is None:
            return
        self.ChangePhase(self.turnPhase.update())

    def updateEvents(self):
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

    def createTerrain(self):
        terrain = Terrain()
        terrain.addNode((100, 400))
        terrain.addNode((700, 400))
        terrain.link(0, 1)
        return terrain

    def ChangePhase(self, result):
        if result is None:
            return
        phase, arg = result

        self.clearDeadWorms()
        if phase == "MoveWormPhase":
            self.turnPhase = MoveWormPhase()
        elif phase == "RunSim":
            self.turnPhase = RunSim(arg)
        elif phase == "WeaponAimPhase":
            self.turnPhase = WeaponAimPhase(arg)
        else:
            print("do not know phase:", phase)

    def addWorm(self, position, team="green"):
        self.listWorms.append(Worm(position, team=team))

    def removeWorm(self, worm):
        index = self.listWorms.index(worm)
        if self.focusedWorm > index:
            self.focusedWorm -= 1
        self.listWorms.remove(worm)
        if self.focusedWorm < 0 or self.focusedWorm >= len(self.listWorms):
            self.focusedWorm = 0

    def ChangeTurn(self):
        self.focusedWorm += 1
        self.focusedWorm = self.focusedWorm % len(self.listWorms)

    def clearDeadWorms(self):
        for w in self.listWorms:
            if w.isDead():
                w.destroy()

InitUI()
GameManager().main()
