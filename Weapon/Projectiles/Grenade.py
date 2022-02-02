import pygame

import Globals
from Weapon.Projectile import Projectile


class Grenade(Projectile):
    def __init__(self, worm):
        Projectile.__init__(self, worm, size=8)

    def draw(self):
        pygame.draw.circle(Globals.Screen, "blue", self.screenPosition, 4)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 6, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 8, 2)

