import numpy as np

import Globals
from Input import Input
from Physics import Trajectory
from UI.UIGlobals import listWeaponButtons


class WeaponAimPhase:
    def __init__(self, weapon):
        self.weapon = weapon
        for b in listWeaponButtons:
            b.visible = False
            b.active = False
        self.worm = Globals.MainGame.movingWorm
        self.projectile = weapon.createProjectile(self.worm)
        self.endTimeSim = 0

    def update(self):
        if Input.mouseClickDown(0):
            self.endPhase()
            Globals.MainGame.ChangeTurn()
            return "RunSim", self.endTimeSim

        for x in Globals.listPhysicObjects:
            x.trajectory = None

        relative = Input.mousePos() - self.worm.position
        self.projectile.impulse(relative)

        self.endTimeSim = Trajectory.UpdateTrajectories()
        Trajectory.printTrajectories()

        for DO in Globals.listDynamicObjects:
            DO.update(0)
        return None

    def endPhase(self):
        for b in listWeaponButtons:
            b.visible = True
            b.active = True
