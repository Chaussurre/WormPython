import numpy as np
import Globals


class DynamicObject:
    def __init__(self, position=(0, 0)):
        self._rect = None
        Globals.listDynamicObjects.append(self)
        self.x = 0
        self.y = 0
        self.position = position
        self.visible = True

    @property
    def screenPosition(self):
        return self.position[0], self.position[1]

    @property
    def position(self):
        return np.array((self.x, self.y))

    @position.setter
    def position(self, value):
        self.x, self.y = float(value[0]), float(value[1])

    def draw(self, time):
        pass

    def update(self, time):
        if self.visible:
            self.draw(time)

    def move(self, direction):
        self.position += direction

    def destroy(self):
        if self in Globals.listDynamicObjects:
            Globals.listDynamicObjects.remove(self)
