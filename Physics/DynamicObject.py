import numpy as np
import Globals


class DynamicObject:
    def __init__(self, position=(0, 0)):
        self._rect = None
        Globals.listDynamicObjects.append(self)
        self.x = 0
        self.y = 0
        self.position = position

    @property
    def screenPosition(self):
        return self.position[0], self.position[1]

    @property
    def position(self):
        return np.array((self.x, self.y))

    @position.setter
    def position(self, value):
        self.x, self.y = float(value[0]), float(value[1])

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    def draw(self):
        return None

    def update(self):
        self.rect = self.draw()

    def move(self, direction):
        self.position += direction
