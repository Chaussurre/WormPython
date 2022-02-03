import numpy as np

from Physics.PhysicObject import PhysicObject


class Projectile(PhysicObject):
    def __init__(self, worm, size=15):
        PhysicObject.__init__(self, position=worm.position, size=size)
        self.worm = worm
        self.ignoreObjects.append(worm.collider)
        if worm.trajectory is not None:
            worm.ignoreObjects.append(self.collider)

