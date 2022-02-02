import numpy as np

import Globals
import pygame
from Physics.PhysicObject import PhysicObject
from Input import Input

class Worm(PhysicObject):
    def __init__(self, position=np.array((0.0, 0.0)), velocity=np.array((0.0, 0.0)), team="green"):
        PhysicObject.__init__(self, position=position, velocity=velocity, size=15)
        self.team = team

    def draw(self):
        pygame.draw.circle(Globals.Screen, self.team, self.screenPosition, 10)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 12, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 15, 3)

    def inputMove(self):
        Xmove = Input.GetKeyBoardDirection()[0]
        if Xmove < 0:
            move = np.array(Globals.MoveJumps)
            move[0] *= -1
            self.impulse(move)
        if Xmove > 0:
            self.impulse(Globals.MoveJumps)
        return Xmove != 0
