import pygame

import Globals
from Physics.PhysicObject import PhysicObject
from Physics.TimedTrajectory import TimedTrajectory
from Weapon.Projectile import Projectile

Timer = 2

class Grenade(Projectile):
    def __init__(self, worm):
        Projectile.__init__(self, worm, size=8)

    def draw(self):
        pygame.draw.circle(Globals.Screen, "blue", self.screenPosition, 4)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 6, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 8, 2)

    def impulse(self, speed):
        self.trajectory = TimedTrajectory(startPosition=self.position, startVelocity=speed, physicObject=self, timer=Timer)
