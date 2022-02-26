import random

import numpy as np
import pygame.draw

import Globals

# Parameters
from EventManager.EventManager import eventManager
from GameLogic.Team import Team
from GameLogic.TurnPhases.IntroNewTurn import IntroNewTurn
from GameLogic.TurnPhases.MoveWormPhase import MoveWormPhase
from GameLogic.TurnPhases.RunSim import RunSim
from GameLogic.TurnPhases.StopTime import StopTime
from GameLogic.TurnPhases.VictoryScreen import VictoryScreen
from GameLogic.TurnPhases.WeaponAimPhase import WeaponAimPhase
from Physics.Trajectory import UpdateTrajectories
from Worm.Worm import Worm

ActionPerTurn = 2


class TurnManager:
    def __init__(self):
        self.nbActions = 0
        self.Teams = []
        self.playingTeam = 0
        self.turnPhase = None

    @property
    def movingWorm(self):
        return self.Teams[self.playingTeam].movingWorm

    def update(self):
        if self.turnPhase is None:
            return
        newPhase = self.turnPhase.update()
        self.changePhase(newPhase)

    def changePhase(self, result):
        if result is None:
            return
        phase = result[0]
        args = result[1:]

        nbTeam = len(list(filter(lambda team: team.isAlive(), self.Teams)))
        if nbTeam == 1:
            self.turnPhase = VictoryScreen(list(filter(lambda team: team.isAlive(), self.Teams))[0])
            return
        if nbTeam == 0:
            self.turnPhase = VictoryScreen(None)
            return

        if self.movingWorm.isDead():
            self.clearDeadWorms()
            self.startTurn()
            return

        self.clearDeadWorms()
        if phase == "MoveWormPhase":
            if self.nbActions == 0:
                self.startTurn()
            else:
                self.turnPhase = MoveWormPhase()
        elif phase == "RunSim":
            self.turnPhase = RunSim(*args)
        elif phase == "WeaponAimPhase":
            self.nbActions -= 1
            self.turnPhase = WeaponAimPhase(*args)
        elif phase == "StopTime":
            self.turnPhase = StopTime(*args, self.nbActions > 0)
        else:
            print("do not know phase:", phase)

    def initTurn(self):
        eventManager.triggerEvent("new turn")
        self.turnPhase = RunSim()

    def startTurn(self):
        eventManager.triggerEvent("new turn")
        if self.movingWorm is None:
            return
        self.movingWorm.active = False
        self.playingTeam += 1
        self.playingTeam %= len(self.Teams)
        self.Teams[self.playingTeam].setNextWorm()
        self.movingWorm.active = True
        self.nbActions = ActionPerTurn
        self.turnPhase = IntroNewTurn(self.Teams[self.playingTeam])

    def createTeams(self, *colors):
        for color in colors:
            self.Teams.append(Team(color, color))

    def createWorms(self, *positions):
        positions = list(map(np.array, positions))
        random.shuffle(positions)
        indexTeam = 0
        worms = list(map(lambda p: Worm(p), positions))
        for worm in worms:
            self.Teams[indexTeam].assignWorm(worm)
            indexTeam = (indexTeam + 1) % len(self.Teams)
        UpdateTrajectories()
        for worm in worms:
            if worm.trajectory.Next is not None:
                worm.position = worm.trajectory.Next.GetPoint(worm.trajectory.Next.startTime)
                worm.impulse(np.array((0, 0)))

    def clearDeadWorms(self):
        for t in self.Teams:
            for w in t.listWorms:
                if w.isDead():
                    w.destroy()
