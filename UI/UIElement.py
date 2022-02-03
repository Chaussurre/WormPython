import numpy as np


class UIElement:
    def __init__(self, position=np.array((0, 0))):
        self.children = []
        self.__position = position
        self.visible = True

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, pos):
        for c in self.children:
            c.position = c.position + pos - self.__position
        self.__position = pos

    def drawUI(self):
        for c in self.children:
            c.drawUI()

    def addChild(self, child):
        self.children.append(child)
