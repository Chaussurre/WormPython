import numpy as np


class Collider:
    def __init__(self, position, size):
        self.size = size
        self.position = position

    def HasPoint(self, point, center=None):
        if center is None:
            center = self.position
        relative = point - center
        return np.linalg.norm(relative, 2) < self.size

    def isColliding(self, otherCollider, center=None, otherCenter=None):
        return np.linalg.norm(self.collisionDelta(otherCollider, center, otherCenter), 2) > 0

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