import Globals
import pygame
from Physics.PhysicObject import PhysicObject
from Input import Input

class Worm(PhysicObject):

    def __init__(self, position=(0, 0), velocity=(0, 0)):
        PhysicObject.__init__(self, position=position, velocity=velocity, size=15)

    def draw(self):
        pygame.draw.circle(Globals.Screen, "green", self.screenPosition, 10)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 12, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 15, 3)

