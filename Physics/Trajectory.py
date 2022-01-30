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
            if self.Next is not None:
                return self.Next.GetPoint(time)
            time = self.endTime
        time -= self.startTime

        return 0.5 * time * time * Globals.Gravity + self.startVelocity * time + self.startPosition

    def GetVelocity(self, time):
        if time > self.endTime:
            if self.Next is not None:
                return self.Next.GetVelocity(time)
            time = self.endTime
        time -= self.startTime

        return time * Globals.Gravity + self.startVelocity

    def IsOver(self, time):
        if self.Next is None:
            return time > self.endTime
        return self.Next.IsOver(time)

    def print(self, color="red"):
        previousPos = self.GetPoint(self.time)
        predictTime = self.time
        step = 20
        currentTraj = self
        while predictTime > currentTraj.endTime and currentTraj.Next is not None:
            currentTraj = currentTraj.Next
        for i in range(0, 5000, step):
            predictTime += 1.0 / Globals.FrameRate * step
            if predictTime > currentTraj.endTime:
                predictTime = currentTraj.endTime
                if currentTraj.Next is not None:
                    currentTraj = currentTraj.Next
            nextPos = self.GetPoint(predictTime)
            pygame.draw.line(Globals.Screen, start_pos=previousPos, end_pos=nextPos, color=color, width=3)
            previousPos = nextPos


    def findEnd(self):
        if self.physicObject is not None:
            time = self.time
            for i in range(5000):
                time += 1.0 / Globals.FrameRate
                collisions = self.physicObject.getCollisions(time)
                if len(collisions) > 0:
                    normal = np.array((0.0, 0.0))
                    for c in collisions:
                        normal += c.delta

                    self.Next = Trajectory(startPosition=self.GetPoint(time) + normal,
                                           startVelocity=reflectVelocityOnNormal(self.GetVelocity(time), normal),
                                           startTime=time,
                                           physicObject=self.physicObject)

                    return time
        return float("inf")

    def update(self):
        self.endTime = self.findEnd()


def UpdateTrajectories():
    for x in Globals.listPhysicObjects:
        if x.trajectory is not None:
            x.trajectory.update()


def reflectVelocityOnNormal(velocity, normal):
    normal /= np.linalg.norm(normal, 2)
    projected = np.linalg.multi_dot((velocity, normal)) * normal
    return velocity - 2 * projected
