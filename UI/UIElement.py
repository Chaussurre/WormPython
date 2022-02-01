import numpy as np


class UIElement:
    def __init__(self, position=np.array((0, 0))):
        self.children = []
        self.position = position

    def drawUI(self):
        for c in self.children:
            c.drawUI()

    def addChild(self, child):
        self.children.append(child)


RootUI = UIElement()
