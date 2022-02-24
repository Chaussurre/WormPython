import random

import numpy as np

import Globals

# Parameters
from GameLogic.Team import Team
from GameLogic.TurnPhases.MoveWormPhase import MoveWormPhase
from GameLogic.TurnPhases.RunSim import RunSim
from GameLogic.TurnPhases.StopTime import StopTime
from GameLogic.TurnPhases.WeaponAimPhase import WeaponAimPhase
from Physics.Trajectory import UpdateTrajectories
from Worm.Worm import Worm

ActionPerTurn = 2


class TurnManager:
    def __init__(self):
        self.worm = None
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
        self.changePhase(self.turnPhase.update())

    def changePhase(self, result):
        if result is None:
            return
        phase = result[0]
        args = result[1:]

        self.clearDeadWorms()
        if phase == "MoveWormPhase":
            self.turnPhase = MoveWormPhase()
        elif phase == "RunSim":
            self.turnPhase = RunSim(*args)
        elif phase == "WeaponAimPhase":
            self.turnPhase = WeaponAimPhase(*args)
        elif phase == "StopTime":
            self.turnPhase = StopTime(*args)
        else:
            print("do not know phase:", phase)

    def startTurn(self, worm):
        if self.turnPhase is None:
            self.turnPhase = RunSim()
        self.worm = worm
        self.nbActions = ActionPerTurn

    def createTeams(self, *colors):
        for color in colors:
            self.Teams.append(Team(color))

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

    def nextTurn(self):
        self.playingTeam += 1
        self.playingTeam %= len(self.Teams)
        self.startTurn(self.Teams[self.playingTeam].getNextPlaying)

    def clearDeadWorms(self):
        for t in self.Teams:
            for w in t.listWorms:
                if w.isDead():
                    w.destroy()
