import Globals
from EventManager.EventManager import eventManager
from UI import UIGlobals
from Weapon.WeaponList.WeaponList import listWeapons


class MoveWormPhase:
    def __init__(self):
        for x in Globals.listPhysicObjects:
            x.trajectory = None
        for button in UIGlobals.listWeaponButtons:
            button.active = True
        self.chosenWeapon = None
        for w in listWeapons:
            eventManager.addListener(w.eventChoose, self.chooseWeapon)

    def stopListen(self):
        for w in listWeapons:
            eventManager.removeListener(w.eventChoose, self.chooseWeapon)

    def chooseWeapon(self, weapon):
        self.chosenWeapon = weapon

    def update(self):
        Globals.Terrain.draw(0)
        if self.chosenWeapon is not None:
            return "WeaponAimPhase", self.chosenWeapon

        for x in Globals.listDynamicObjects:
            x.update(0)

        worm = Globals.MainGame.movingWorm
        if worm.inputMove():
            self.stopListen()
            return "RunSim",
        return None
