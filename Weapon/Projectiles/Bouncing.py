import pygame

import Globals
from Physics.Explosion import Explosion
from Physics.PhysicObject import PhysicObject
from Physics.TimedTrajectory import TimedTrajectory
from Weapon.Projectile import Projectile

ExplosionSize = 20
ExplosionForce = 20
DamageMax = 20

class Bouncing(Projectile):
    def __init__(self, worm):
        Projectile.__init__(self, worm, size=8)
        self.explosions = [Explosion(self.position, ExplosionSize, force=ExplosionForce, damage=DamageMax),
                           Explosion(self.position, ExplosionSize, force=ExplosionForce, damage=DamageMax),
                           Explosion(self.position, ExplosionSize, force=ExplosionForce, damage=DamageMax)]

    def draw(self, time):
        pygame.draw.circle(Globals.Screen, "cyan", self.screenPosition, 4)
        pygame.draw.circle(Globals.Screen, "black", self.screenPosition, 6, 2)
        pygame.draw.circle(Globals.Screen, "white", self.screenPosition, 8, 2)

    def predictActionAt(self, time):
        if self.trajectory is None:
            return

        traj = self.trajectory
        for i in range(3):
            if traj.endTime < float("inf"):
                self.explosions[i].detonateAt(traj.endTime, traj.GetPoint(traj.endTime))
            if traj.Next is None:
                self.aliveTimer = traj.endTime
                return
            traj = traj.Next

        if time > self.trajectory.Next.Next.endTime:
            self.aliveTimer = self.trajectory.Next.Next.endTime

    def startPrediction(self):
        for explosion in self.explosions:
            explosion.exploded = False
            explosion.visibleAt = float("inf")
        self.aliveTimer = float("inf")

    def destroy(self):
        for explosion in self.explosions:
            explosion.destroy()
        super().destroy()
