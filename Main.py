import pygame
import pygame.gfxdraw

import Globals
from GameLogic.TurnManager import TurnManager
from Input import Input
from Physics.Terrain import GenTerrain
from UI import UIGlobals
from UI.UILayout import InitUI


class GameManager:

    def __init__(self):
        Globals.MainGame = self
        self.running = True
        self.TurnManager = TurnManager()
        pygame.init()
        Globals.Screen = pygame.display.set_mode(Globals.ScreenSize)
        pygame.display.set_caption("Best worm game", "")
        Globals.Screen.fill((0, 0, 0))

    @property
    def movingWorm(self):
        return self.TurnManager.movingWorm

    def main(self):
        GenTerrain()
        self.initWorms()
        self.TurnManager.startTurn(0)
        clock = pygame.time.Clock()
        try:
            while self.running and not self.isGameOver():
                clock.tick(Globals.FrameRate)
                self.updateEvents()
                Globals.Screen.fill((0, 0, 0))
                self.playTurnPhase()
                UIGlobals.RootUI.drawUI()
                pygame.display.flip()
        finally:
            pygame.quit()

    def initWorms(self):
        self.TurnManager.createTeams("green", "yellow")
        self.TurnManager.createWorms((250, 000),
                                     (350, 000),
                                     (450, 000),
                                     (550, 000))

    def playTurnPhase(self):
        if self.TurnManager is None:
            return
        self.TurnManager.update()

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

    def isGameOver(self):
        aliveTeams = [t for t in self.TurnManager.Teams if t.isAlive]
        return len(aliveTeams) <= 1

InitUI()
GameManager().main()
