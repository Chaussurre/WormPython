import Globals
import pygame
from Physics.PhysicObject import PhysicObject
from Input import Input

class Worm(PhysicObject):

    def draw(self):
        pygame.draw.circle(Globals.Screen, "green", self.screenPosition, 10)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 12, 2)
        rect = pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 15, 3)
        return rect

    def update(self):
        self.move(Input.GetKeyBoardDirection())
        PhysicObject.update(self)


