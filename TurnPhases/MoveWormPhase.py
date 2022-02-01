import Globals
from EventManager.EventManager import eventManager
from UI import UILayout, UIGlobals


class MoveWormPhase:
    def __init__(self, mainGame):
        self.mainGame = mainGame
        for x in Globals.listPhysicObjects:
            x.trajectory = None
        for button in UIGlobals.listWeaponButtons:
            button.active = True
        self.listenerGrenade = lambda: self.chooseWeapon("Grenade")
        self.chosenWeapon = None
        eventManager.addListener(f"pressed Grenade", self.listenerGrenade)

    def stopListen(self):
        eventManager.removeListener(f"pressed Grenade", self.listenerGrenade)

    def chooseWeapon(self, weapon):
        print(weapon)
        self.chosenWeapon = weapon

    def update(self):
        if len(self.mainGame.listWorms) == 0:
            return None

        for x in Globals.listDynamicObjects:
            x.update(0)

        worm = self.mainGame.listWorms[self.mainGame.focusedWorm]
        if worm.inputMove():
            self.stopListen()
            return "RunSim"
        return None
