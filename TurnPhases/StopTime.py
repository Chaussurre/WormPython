import pygame

import Globals
import Input.Input
from EventManager.EventManager import eventManager
from Physics import Trajectory
from Physics.TimedTrajectory import TimedTrajectory
from UI import UIGlobals
from Weapon.WeaponList.WeaponList import listWeapons


class StopTime:
    def __init__(self, time, endTime):
        for button in UIGlobals.listWeaponButtons:
            button.active = True
        self.chosenWeapon = None
        for w in listWeapons:
            eventManager.addListener(w.eventChoose, self.chooseWeapon)
        self.time = time
        self.endTime = endTime

    def update(self):
        Globals.Terrain.draw(self.time)
        Trajectory.printTrajectories(time=self.time)
        for DO in Globals.listDynamicObjects:
            DO.update(self.time)

        if self.chosenWeapon is not None:
            self.stopListen()
            for PO in Globals.listPhysicObjects:
                PO.impulse(PO.trajectory.GetVelocity(self.time))
                PO.aliveTimer -= self.time
            return "WeaponAimPhase", self.chosenWeapon

        if Input.Input.IsKeyUp(pygame.K_SPACE):
            self.stopListen()
            return "RunSim", self.time, self.endTime

    def stopListen(self):
        for w in listWeapons:
            eventManager.removeListener(w.eventChoose, self.chooseWeapon)

    def chooseWeapon(self, weapon):
        self.chosenWeapon = weapon
