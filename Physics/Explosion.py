import numpy as np
import pygame.draw

import Globals
from Physics.Collider import Collider
from Physics.DynamicObject import DynamicObject

ExplosionDuration = 0.2

class Explosion(DynamicObject):
    def __init__(self, position=np.array((0, 0)), size=10, force=10):
        super().__init__(position=position)
        self.collider = Collider(position, size)
        self.visibleAt = float("inf")
        self.exploded = False
        self.force = force

    def draw(self, time):
        if self.visibleAt < time < self.visibleAt + ExplosionDuration:
            time -= self.visibleAt
            size = self.collider.size * time / ExplosionDuration
            pygame.draw.circle(Globals.Screen, "red", self.position, size)
            if size > 6:
                pygame.draw.circle(Globals.Screen, "yellow", self.position, size - 6)

    def detonateAt(self, time, position):
        if self.exploded:
            return
        self.visibleAt = time
        self.position = position
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