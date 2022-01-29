import numpy as np
import pygame.draw

import Globals


class Trajectory:
    def __init__(self, startPosition, startVelocity=np.array((0, 0)), startTime=0):
        self.startPosition = startPosition
        self.startVelocity = startVelocity
        self.startTime = startTime
        self.time = startTime
        self.print()

    def GetNextPoint(self):
        self.time += 1.0 / Globals.FrameRate
        return self.GetPoint(self.time)

    def GetPoint(self, time):
        return 0.5 * time * time * Globals.Gravity + self.startVelocity * time + self.startPosition

    def IsOver(self, time):
        return False

    def print(self, color="red"):
        previousPos = self.GetPoint(self.time)
        predictTime = self.time
        step = 10
        for i in range(0, 5000, step):
            predictTime += 1.0 / Globals.FrameRate * step
            nextPos = self.GetPoint(predictTime)
            pygame.draw.line(Globals.Screen, start_pos=previousPos, end_pos=nextPos, color=color, width=3)
            previousPos = nextPos

