import pygame

import Globals
from Physics.Explosion import Explosion
from Physics.PhysicObject import PhysicObject
from Physics.TimedTrajectory import TimedTrajectory
from Weapon.Projectile import Projectile

ExplosionSize = 30
ExplosionForce = 30
DamageMax = 30

class Rocket(Projectile):
    def __init__(self, worm):
        Projectile.__init__(self, worm, size=8)
        self.explosion = Explosion(self.position, ExplosionSize, force=ExplosionForce, damage=DamageMax)

    def draw(self, time):
        pygame.draw.circle(Globals.Screen, "purple", self.screenPosition, 4)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 6, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 8, 2)


    def predictActionAt(self, time):
        if self.trajectory is None:
            return

        if time > self.trajectory.endTime:
            self.aliveTimer = self.trajectory.endTime
            self.trajectory.Next = None
            self.explosion.detonateAt(time, self.trajectory.GetPoint(time))

    def startPrediction(self):
        self.explosion.exploded = False

    def destroy(self):
        self.explosion.destroy()
        super().destroy()
