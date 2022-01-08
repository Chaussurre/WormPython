import Globals
from Physics.DynamicObject import DynamicObject
import numpy as np


class PhysicObject(DynamicObject):
    def __init__(self, position=(0, 0), velocity=(0, 0)):
        DynamicObject.__init__(self, position)
        self.velocity = np.array((float(velocity[0]), float(velocity[1])))

    def update(self):
        self.velocity += Globals.Gravity / Globals.FrameRate
        self.position += self.velocity / Globals.FrameRate
        DynamicObject.update(self)
