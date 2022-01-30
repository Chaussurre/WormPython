import numpy as np
import pygame.draw

import Globals


class Trajectory:
    def __init__(self, startPosition, startVelocity=np.array((0, 0)), startTime=0, physicObject=None):
        self.startPosition = startPosition
        self.startVelocity = startVelocity
        self.startTime = startTime
        self.time = startTime
        self.physicObject = physicObject
        self.endTime = float("inf")
        self.Next = None

    def GetNextPoint(self):
        self.time += 1.0 / Globals.FrameRate
        return self.GetPoint(self.time)

    def GetPoint(self, time):
        if time > self.endTime:
            time = self.endTime

        return 0.5 * time * time * Globals.Gravity + self.startVelocity * time + self.startPosition

    def IsOver(self, time):
        if self.Next is None:
            return time > self.endTime
        return self.Next.IsOver(time)

    def print(self, color="red"):
        previousPos = self.GetPoint(self.time)
        predictTime = self.time
        step = 10
        for i in range(0, 5000, step):
            predictTime += 1.0 / Globals.FrameRate * step
            nextPos = self.GetPoint(predictTime)
            pygame.draw.line(Globals.Screen, start_pos=previousPos, end_pos=nextPos, color=color, width=3)
            previousPos = nextPos

    def findEnd(self):
        if self.physicObject is not None:
            time = self.time
            for i in range(5000):
                time += 1.0 / Globals.FrameRate
                if len(self.physicObject.getCollisions(time)) > 0:
                    return time
        return float("inf")

    def update(self):
        self.endTime = self.findEnd()


def UpdateTrajectories():
    for x in Globals.listPhysicObjects:
        if x.trajectory is not None:
            x.trajectory.update()
