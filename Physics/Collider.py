import numpy as np

import Globals
from Physics.Collision import Collision


class Collider:
    def __init__(self, position, size, physicObject=None):
        self.size = size
        self.position = position
        self.physicObject = physicObject

    def HasPoint(self, point, center=None):
        if center is None:
            center = self.position
        relative = point - center
        return np.linalg.norm(relative, 2) < self.size

    def getCollision(self, otherCollider, center=None, otherCenter=None):
        delta = self.collisionDelta(otherCollider, center=center, otherCenter=otherCenter)
        if np.linalg.norm(delta, 2) == 0:
            return None
        if center is None:
            center = self.position
        return Collision(self, otherCollider, delta, center)

    def collisionDelta(self, otherCollider, center=None, otherCenter=None):
        if center is None:
            center = self.position
        if otherCenter is None:
            otherCenter = otherCollider.position

        relative = otherCenter - center
        distance = np.linalg.norm(relative, 2)
        size = self.size + otherCollider.size - distance
        if size < 0 or distance == 0:
            return np.array((0, 0))
        return relative / distance * size

    def getCollisions(self, time, center):
        colliding = []

        terrainCollision = Globals.Terrain.getCollision(self, center, time)
        if terrainCollision is not None:
            colliding.append(terrainCollision)

        for x in Globals.listPhysicObjects:
            otherCenter = x.predictPositionAt(time)

            if otherCenter is None:
                continue

            collision = self.getCollision(x.collider, center=center, otherCenter=otherCenter)
            if collision is not None:
                colliding.append(collision)

        return colliding