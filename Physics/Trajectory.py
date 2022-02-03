import numpy as np
import pygame.draw

import Globals
from UI import UIGlobals


class Trajectory:
    def __init__(self, startPosition, startVelocity=np.array((0, 0)), startTime=0, physicObject=None):
        self.startPosition = startPosition
        self.startVelocity = startVelocity
        self.startTime = startTime
        self.physicObject = physicObject
        self.endTime = float("inf")
        self.Next = None
        self.lastCheckedPos = startPosition

    def GetPoint(self, time):
        if time > self.endTime:
            if self.Next is not None:
                return self.Next.GetPoint(time)
            time = self.endTime

        if time < self.startTime:
            return self.startPosition
        time -= self.startTime

        return 0.5 * time * time * Globals.Gravity + self.startVelocity * time + self.startPosition

    def GetVelocity(self, time):
        if time > self.endTime:
            if self.Next is not None:
                return self.Next.GetVelocity(time)
            time = self.endTime

        if time > self.startTime:
            time -= self.startTime
        else:
            time = self.startTime

        return time * Globals.Gravity + self.startVelocity

    def print(self, time, color="red"):
        if time > self.physicObject.aliveTimer:
            return

        previousPos = self.GetPoint(time)
        predictTime = time
        step = 5
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

    def GetLastTrajectory(self):
        if self.Next is None:
            return self
        return self.Next.GetLastTrajectory()

    def GetTrajectoryAt(self, time):
        if self.endTime > time or self.Next is None:
            return self
        return self.Next.GetLastTrajectory(time)

    def CheckTime(self, time):
        if self.physicObject is not None:

            if time > self.endTime:
                if self.Next is not None:
                    return self.Next.CheckTime(time)
                return False
            elif not self.isInBounds(time):
                self.GetLastTrajectory().endTime = time
                return False
            else:
                collisions = self.physicObject.getCollisions(time)
                if len(collisions) > 0:
                    normal = np.array((0.0, 0.0))
                    for c in collisions:
                        normal += c.delta

                    newVel = reflectVelocityOnNormal(self.GetVelocity(time), normal) * Globals.Bounciness
                    self.endTime = time

                    if np.linalg.norm(newVel, 2) > 5:
                        self.impulseAt(newVel, time)
                        return True
                    if self.endTime < self.startTime + 0.02:
                        self.endTime = self.startTime
                    return False
            self.lastCheckedPos = self.GetPoint(time)
            return True
        return False

    def impulseAt(self, velocity, time):
        self.Next = Trajectory(startPosition=self.lastCheckedPos,
                               startVelocity=velocity,
                               startTime=time,
                               physicObject=self.physicObject)

    def isInBounds(self, time):
        pos = self.GetPoint(time)
        if -40 > pos[0] or pos[0] > Globals.ScreenSize[0] + 40 - UIGlobals.weaponPanelSize:
            return False
        if -40 > pos[1] or pos[1] > Globals.ScreenSize[1] + 40:
            return False
        return True


def UpdateTrajectories():
    time = 0.0
    changed = True
    for x in Globals.listPhysicObjects:
        x.startPrediction()
        if x.trajectory is None:
            x.impulse(np.array((0, 0)))
    while time < 50 and changed:
        changed = False
        time += 1.0 / Globals.CollisionTestRate
        for x in Globals.listPhysicObjects:
            x.predictActionAt(time)
            if x.trajectory.CheckTime(time):
                changed = True
    return time


def reflectVelocityOnNormal(velocity, normal):
    size = np.linalg.norm(normal, 2)
    if size == 0:
        return velocity
    normal /= size
    projected = np.linalg.multi_dot((velocity, normal)) * normal
    return velocity - 2 * projected


def printTrajectories(time=0, color="red"):
    for PO in Globals.listPhysicObjects:
        if PO.trajectory is not None:
            PO.trajectory.print(time, color=color)
