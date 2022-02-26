from Weapon.Projectiles.Bouncing import Bouncing
from Weapon.Weapon import Weapon


class BouncingLauncher(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Bouncing")

    def createProjectile(self, worm):
        return Bouncing(worm)
