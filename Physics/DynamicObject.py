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

    def draw(self):
        pass

    def update(self, time):
        self.draw()

    def move(self, direction):
        self.position += direction
