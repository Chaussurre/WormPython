import numpy as np
import pygame.draw

import Globals


class Trajectory:
    def __init__(self, startPosition, startVelocity=np.array((0, 0)), startTime=0, physicObject=None):
        self.startPosition = startPosition
        self.startVelocity = startVelocity
        self.startTime = startTime
        self.physicObject = physicObject
        self.endTime = float("inf")
        self.Next = None

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

    def print(self, time, color="red"):
        previousPos = self.GetPoint(time)
        predictTime = time
        step = 10
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

    def CheckTime(self, time):
        if self.physicObject is not None:

            if time > self.endTime:
                if self.Next is not None:
                    self.Next.CheckTime(time)
            else:
                collisions = self.physicObject.getCollisions(time)
                if len(collisions) > 0:
                    normal = np.array((0.0, 0.0))
                    for c in collisions:
                        normal += c.delta

                    newVel = reflectVelocityOnNormal(self.GetVelocity(time), normal) * Globals.Bounciness
                    self.endTime = time

                    if np.linalg.norm(newVel, 2) > 20:
                        self.Next = Trajectory(startPosition=self.GetPoint(time) - normal,
                                               startVelocity=newVel,
                                               startTime=time,
                                               physicObject=self.physicObject)


def UpdateTrajectories():
    time = 0.0
    while time < 50:
        time += 1.0 / Globals.FrameRate
        for x in Globals.listPhysicObjects:
            x.trajectory.CheckTime(time)

    end = 0
    for x in Globals.listPhysicObjects:
        traj = x.trajectory.GetLastTrajectory()
        if traj.endTime > 50:
            traj.endTime = 50
        if traj.endTime > end:
            end = traj.endTime
    return end


def reflectVelocityOnNormal(velocity, normal):
    normal /= np.linalg.norm(normal, 2)
    projected = np.linalg.multi_dot((velocity, normal)) * normal
    return velocity - 2 * projected
