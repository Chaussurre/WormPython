import numpy as np

import Globals
from EventManager.EventManager import eventManager
from Input import Input
from Physics import Trajectory
from UI.UIGlobals import listWeaponButtons


class WeaponAimPhase:
    def __init__(self, weapon, endTime=0):
        self.weapon = weapon
        for b in listWeaponButtons:
            b.visible = False
            b.active = False
        self.worm = Globals.MainGame.movingWorm
        self.projectile = weapon.createProjectile(self.worm)
        self.endTimeSim = endTime
        self.initConditions = []
        for PO in Globals.listPhysicObjects:
            self.initConditions.append((PO, PO.getVelocity(0)))

    def update(self):
        Globals.Terrain.draw(0)
        if Input.mouseClickDown(0):
            self.endPhase()
            eventManager.triggerEvent("shot", self.weapon)
            return "RunSim", 0, self.endTimeSim

        Globals.Terrain.nextDestroyedZones.clear()

        for PO, speed in self.initConditions:
            PO.impulse(speed)

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
