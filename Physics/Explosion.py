import numpy as np
import pygame.draw

import Globals
from Physics.Collider import Collider
from Physics.DynamicObject import DynamicObject


class Explosion(DynamicObject):
    def __init__(self, position=np.array((0, 0)), size=10, force=10):
        super().__init__(position=position)
        self.collider = Collider(position, size)
        self.visible = False
        self.exploded = False
        self.force = force

    def draw(self):
        pygame.draw.circle(Globals.Screen, "red", self.position, self.collider.size)

    def detonateAt(self, time, position):
        if self.exploded:
            return
        self.exploded = True
        colliding = self.collider.getCollisions(time, position)
        for c in colliding:
            if c.otherCollider is not None:
                PO = c.otherCollider.physicObject
                if PO is not None:
                    relative = PO.position - position
                    distance = np.linalg.norm(relative)
                    force = self.force / ((distance / 100) ** 2)
                    PO.impulseAt(relative / distance * force, time)