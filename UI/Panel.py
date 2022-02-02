import numpy as np
import pygame.draw

import Globals
import Input.Input
from UI.UIElement import UIElement


class Panel(UIElement):
    def __init__(self, position=np.array((0, 0)), size=np.array((10, 10)), color="blue"):
        UIElement.__init__(self, position=position)
        self.size = size
        self.color = color
        self.rect = self.position - self.size / 2, self.position + self.size / 2

    @property
    def rectWithSize(self):
        return self.rect[0], self.size

    def drawUI(self):
        if not self.visible:
            return
        pygame.draw.rect(Globals.Screen,
                         color=self.color,
                         rect=self.rectWithSize)
        UIElement.drawUI(self)

    def isMouseOver(self):
        return Input.Input.mouseInRect(self.rect)