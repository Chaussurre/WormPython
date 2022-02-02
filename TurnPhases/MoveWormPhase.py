import Globals
from EventManager.EventManager import eventManager
from UI import UILayout, UIGlobals
from Weapon.WeaponList import listWeapons


class MoveWormPhase:
    def __init__(self, mainGame):
        self.mainGame = mainGame
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
        if self.chosenWeapon is not None:
            return "WeaponAimPhase", self.chosenWeapon

        if len(self.mainGame.listWorms) == 0:
            return None

        for x in Globals.listDynamicObjects:
            x.update(0)

        worm = self.mainGame.listWorms[self.mainGame.focusedWorm]
        if worm.inputMove():
            self.stopListen()
            return "RunSim", None
        return None
