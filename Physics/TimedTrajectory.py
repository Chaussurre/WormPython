import numpy as np

from Physics.Trajectory import Trajectory


class TimedTrajectory(Trajectory):
    def __init__(self, startPosition, timer=1, startVelocity=np.array((0, 0)), startTime=0, physicObject=None):
        super().__init__(startPosition,
                         startVelocity=startVelocity,
                         startTime=startTime,
                         physicObject=physicObject)
        self.timer = timer
        self.endTime = timer

    def GetPoint(self, time):
        if time > self.timer:
            return super().GetPoint(self.timer)
        return super().GetPoint(time)