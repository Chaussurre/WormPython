import numpy as np
import pygame.font

import Globals
from UI.UIElement import UIElement


class Text(UIElement):
    def __init__(self, position=np.array((0, 0)), text="UI Element", size=30):
        self.size = size
        self.text = text
        UIElement.__init__(self, position=position)
        self.font = pygame.font.SysFont(Globals.Font, size)

    def drawUI(self):
        if not self.visible:
            return
        Globals.Screen.blit(self.font.render(self.text, 1, "white"), tuple(self.position))
        UIElement.drawUI(self)