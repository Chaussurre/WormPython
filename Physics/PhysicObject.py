import Globals
import numpy as np
from Physics.DynamicObject import DynamicObject
from Physics.Trajectory import Trajectory


class PhysicObject(DynamicObject):
    def __init__(self, position=(0, 0), velocity=(0, 0), kinematic=False):
        DynamicObject.__init__(self, position)
        Globals.listPhysicObjects.append(self)
        self.velocity = np.array((float(velocity[0]), float(velocity[1])))
        self.kinematic = kinematic
        self.trajectory = None

    def update(self):
        if self.trajectory is None:
            self.trajectory = Trajectory(startPosition=self.position)
        print(self.position)
        self.position = self.trajectory.GetNextPoint()
        DynamicObject.update(self)


    def impulse(self, speed):
        self.trajectory = Trajectory(startPosition=self.position, startVelocity=speed)

    def GetCollisions(self):
        return []
