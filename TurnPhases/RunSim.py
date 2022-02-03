import Globals
from Physics import Trajectory
from UI import UILayout, UIGlobals


class RunSim:
    def __init__(self, mainGame, endTime=None):
        self.mainGame = mainGame
        self.time = 0
        if endTime is None:
            self.endSimTime = Trajectory.UpdateTrajectories()
        else:
            self.endSimTime = endTime
        for button in UIGlobals.listWeaponButtons:
            button.active = False

    def update(self):
        Trajectory.printTrajectories(self.time)
        for DO in Globals.listDynamicObjects:
            DO.update(self.time)
        self.time += 1.0 / Globals.FrameRate
        if self.time >= self.endSimTime:
            for x in [x for x in Globals.listPhysicObjects if x.aliveTimer != float("inf")]:
                x.destroy()
            return "MoveWormPhase", None
        return None