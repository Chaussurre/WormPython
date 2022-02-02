import numpy as np

import Globals
from Input import Input
from Physics import Trajectory
from UI.UIGlobals import listWeaponButtons


class WeaponAimPhase:
    def __init__(self, mainGame, weapon):
        self.mainGame = mainGame
        self.weapon = weapon
        for b in listWeaponButtons:
            b.visible = False
            b.active = False

    def update(self):
        if Input.mouseClickDown(0):
            self.endPhase()
            return "RunSim", None

        worm = self.mainGame.movingWorm
        relative = Input.mousePos() - worm.position
        worm.impulse(relative)

        Trajectory.UpdateTrajectories()
        Trajectory.printTrajectories()

        for DO in Globals.listDynamicObjects:
            DO.update(0)
        return None

    def endPhase(self):
        for b in listWeaponButtons:
            b.visible = True
            b.active = True
