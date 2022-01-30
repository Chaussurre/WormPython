import numpy as np

from Physics.Collision import Collision


class Collider:
    def __init__(self, position, size):
        self.size = size
        self.position = position

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
        size = -distance + self.size + otherCollider.size
        if size < 0 or distance == 0:
            return np.array((0, 0))
        return relative / distance * size