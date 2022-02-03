import Globals
import numpy as np

from Physics.Collider import Collider
from Physics.DynamicObject import DynamicObject

from Physics.Trajectory import Trajectory


class PhysicObject(DynamicObject):
    def __init__(self, position=(0, 0), velocity=(0, 0), kinematic=False, size=1):
        DynamicObject.__init__(self, position)
        Globals.listPhysicObjects.append(self)
        self.aliveTimer = float("inf")
        self.kinematic = kinematic

        self.trajectory = None
        self.impulse(np.array(velocity))
        self.collider = Collider(position, size, physicObject=self)
        # A list of objects that will be ignored in the first trajectory, useful if two objects starts at the same pos
        self.ignoreObjects = []

    def update(self, time):
        if self.trajectory is not None:
            self.position = self.trajectory.GetPoint(time)
        if time <= self.aliveTimer:
            super().update(time)

    def impulse(self, speed, time=0):
        if time < self.aliveTimer:
            self.trajectory = Trajectory(startPosition=self.position,
                                         startVelocity=speed,
                                         physicObject=self,
                                         startTime=time)

    def impulseAt(self, speed, time):
        if time > self.aliveTimer:
            return
        if self.trajectory is None:
            self.impulse(speed, time=time)
        else:
            self.trajectory.impulseAt(speed, time)

    def predictPositionAt(self, time):
        if time > self.aliveTimer:
            return None
        if self.trajectory is None:
            return self.position
        return self.trajectory.GetPoint(time)

    def startPrediction(self):
        pass

    def predictActionAt(self, time):
        pass

    def getCollisions(self, time):
        colliding = self.collider.getCollisions(time, self.predictPositionAt(time))

        # We only check ignored collisions for 0.5 secs
        if time < 0.5:
            colliding = [x for x in colliding if x.otherCollider not in self.ignoreObjects]

        return colliding

    def destroy(self):
        super().destroy()
        Globals.listPhysicObjects.remove(self)