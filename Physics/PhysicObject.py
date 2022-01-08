import Globals
from Physics.DynamicObject import DynamicObject
import numpy as np

class PhysicObject(DynamicObject):
    def __init__(self, position=(0, 0), velocity=(0, 0), kinematic=False):
        DynamicObject.__init__(self, position)
        Globals.listPhysicObjects.append(self)
        self.velocity = np.array((float(velocity[0]), float(velocity[1])))
        self.kinematic = kinematic

    def update(self):
        if not self.kinematic:
            self.velocity += Globals.Gravity / Globals.FrameRate
            self.position += self.velocity / Globals.FrameRate
        DynamicObject.update(self)

    def GetCollisions(self):
        return []
