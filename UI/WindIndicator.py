import numpy as np
import pygame.draw

import Globals
from Physics.DynamicObject import DynamicObject

# parameters
WindIndicatorPosition = 130, 50
RatioWindSize = 0.2
ArrowWidth = 6

class WindIndicator(DynamicObject):
    def __init__(self):
        DynamicObject.__init__(self, position=WindIndicatorPosition)

    def draw(self, _):
        if np.linalg.norm(Globals.Wind, 2) < 0.1:
            return
        basePos = self.position, self.position + Globals.Wind * RatioWindSize
        relative = basePos[0] - basePos[1]
        relative /= np.linalg.norm(relative, 2)
        normal = np.array((-relative[1], relative[0])) * ArrowWidth
        pygame.draw.polygon(Globals.Screen, "white", (basePos[0] + normal,
                                                      basePos[0] - normal,
                                                      basePos[1] - normal,
                                                      basePos[1] - 2 * normal,
                                                      basePos[1] - relative * 2 * ArrowWidth,
                                                      basePos[1] + 2 * normal,
                                                      basePos[1] + normal))