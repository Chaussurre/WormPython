import numpy as np
import pygame.draw

import Globals
from UI.UIElement import UIElement


class Panel(UIElement):
    def __init__(self, position=np.array((0, 0)), size=np.array((10, 10)), color="blue"):
        UIElement.__init__(self, position=position)
        self.size = size
        self.color = color

    def drawUI(self):
        topLeft = self.position - self.size / 2
        bottomRight = self.position + self.size / 2
        pygame.draw.rect(Globals.Screen,
                         color=self.color,
                         rect=(topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]))
        UIElement.drawUI(self)