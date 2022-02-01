import Globals
from Physics import Trajectory
from UI import UILayout


class RunSim:
    def __init__(self, mainGame):
        self.mainGame = mainGame
        self.time = 0
        self.endSimTime = Trajectory.UpdateTrajectories()
        for button in UILayout.listWeaponButtons:
            button.active = False

    def update(self):
        printTrajectories(self.time)
        for DO in Globals.listDynamicObjects:
            DO.update(self.time)
        self.time += 1.0 / Globals.FrameRate
        if self.time >= self.endSimTime:
            return "MoveWormPhase"
        return None

def printTrajectories(time=0, color="red"):
    for PO in Globals.listPhysicObjects:
        if PO.trajectory is not None:
            PO.trajectory.print(time, color=color)