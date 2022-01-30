import Globals
import numpy as np

from Physics.Collider import Collider
from Physics.DynamicObject import DynamicObject

from Physics.Trajectory import Trajectory


class PhysicObject(DynamicObject):
    def __init__(self, position=(0, 0), velocity=(0, 0), kinematic=False, size=1):
        DynamicObject.__init__(self, position)
        Globals.listPhysicObjects.append(self)
        self.velocity = np.array((float(velocity[0]), float(velocity[1])))
        self.kinematic = kinematic
        self.trajectory = None
        self.collider = Collider(position, size)
        self.impulse(velocity)

    def update(self):
        if self.trajectory is None:
            self.impulse(np.array((0, 0)))
        self.position = self.trajectory.GetNextPoint()
        DynamicObject.update(self)

    def impulse(self, speed):
        self.trajectory = Trajectory(startPosition=self.position, startVelocity=speed, physicObject=self)

    def predictPositionAt(self, time):
        if self.trajectory is None:
            return self.position
        return self.trajectory.GetPoint(time)

    def getCollisions(self, time):
        colliding = []
        center = self.predictPositionAt(time)

        for x in Globals.listPhysicObjects:
            otherCenter = x.predictPositionAt(time)
            if self.collider.isColliding(x.collider, center=center, otherCenter=otherCenter):
                colliding.append(x)
                print(time)

        return colliding
