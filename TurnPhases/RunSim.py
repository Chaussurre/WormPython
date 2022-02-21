import pygame

import Globals
from Input import Input
from Physics import Trajectory
from UI import UIGlobals


class RunSim:
    def __init__(self, startTime=0, endTime=None, canBeStopped=False):
        self.time = startTime
        if endTime is None:
            self.endSimTime = Trajectory.UpdateTrajectories()
        else:
            self.endSimTime = endTime
        for button in UIGlobals.listWeaponButtons:
            button.active = False
        self.canBeStopped = canBeStopped

    def update(self):
        Trajectory.printTrajectories(self.time)
        for DO in Globals.listDynamicObjects:
            DO.update(self.time)

        if Input.IsKeyUp(pygame.K_SPACE):
            return "StopTime", self.time, self.endSimTime

        if Input.IsKey(pygame.K_SPACE):
            self.time += 1.0 / Globals.FrameRate * Globals.TimeSlowSpace
        else:
            self.time += 1.0 / Globals.FrameRate

        if self.time >= self.endSimTime:
            for x in [x for x in Globals.listPhysicObjects if x.aliveTimer != float("inf")]:
                x.destroy()
            Globals.MainGame.ChangeTurn()
            return "MoveWormPhase",
        return None
