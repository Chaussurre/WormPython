import Globals
from UI import UILayout


class MoveWormPhase:
    def __init__(self, mainGame):
        self.mainGame = mainGame
        for x in Globals.listPhysicObjects:
            x.trajectory = None
        for button in UILayout.listWeaponButtons:
            button.active = True

    def update(self):
        if len(self.mainGame.listWorms) == 0:
            return

        for x in Globals.listDynamicObjects:
            x.update(0)

        worm = self.mainGame.listWorms[self.mainGame.focusedWorm]
        if worm.inputMove():
            return "RunSim"
        return None