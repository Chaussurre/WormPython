import numpy as np
import pygame.draw

import Globals
import Worm.Worm
from Physics.Collider import Collider
from Physics.DynamicObject import DynamicObject

ExplosionDuration = 0.2


class Explosion(DynamicObject):
    def __init__(self, position=np.array((0, 0)), size=10, force=10, damage=10, ):
        super().__init__(position=position)
        self.collider = Collider(position, size)
        self.visibleAt = float("inf")
        self.exploded = False
        self.force = force
        self.damage = damage

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

        Globals.Terrain.destroy(self.collider, position, time)

        colliding = self.collider.getCollisions(time, position)
        for c in colliding:
            if c.otherCollider is not None:
                PO = c.otherCollider.physicObject
                if PO is not None:
                    relative = PO.position - position
                    distance = np.linalg.norm(relative)
                    force = self.force / ((distance / 100) ** 2)
                    if force > self.force * 10:
                        force = self.force * 10
                    PO.impulseAt(relative / distance * force, time)
                    damage = self.damage
                    distance -= PO.collider.size
                    if distance > self.collider.size * 0.5:
                        damage = self.damage * (self.collider.size - distance) / (self.collider.size * 0.5)
                    if isinstance(PO, Worm.Worm.Worm):
                        PO.trajectory.addEvent(time, lambda: PO.dealDamage(damage))
