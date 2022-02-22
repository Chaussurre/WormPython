import pygame

import Globals
from Physics.Explosion import Explosion
from Physics.PhysicObject import PhysicObject
from Physics.TimedTrajectory import TimedTrajectory
from Weapon.Projectile import Projectile

Timer = 3
ExplosionSize = 30
ExplosionForce = 30
DamageMax = 40

class Grenade(Projectile):
    def __init__(self, worm):
        Projectile.__init__(self, worm, size=8)
        self.explosion = Explosion(self.position, ExplosionSize, force=ExplosionForce, damage=DamageMax)
        self.aliveTimer = Timer

    def draw(self, time):
        pygame.draw.circle(Globals.Screen, "blue", self.screenPosition, 4)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 6, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 8, 2)

    def impulse(self, speed, time=0):
        self.trajectory = TimedTrajectory(startPosition=self.position,
                                          startVelocity=speed,
                                          physicObject=self,
                                          startTime=time,
                                          timer=Timer)

    def predictActionAt(self, time):
        if time > Timer:
            self.explosion.detonateAt(Timer, self.trajectory.GetPoint(Timer))

    def startPrediction(self):
        self.explosion.exploded = False

    def destroy(self):
        self.explosion.destroy()
        super().destroy()
