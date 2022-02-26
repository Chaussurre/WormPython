from Weapon.Projectiles.Rocket import Rocket
from Weapon.Weapon import Weapon


class RocketLauncher(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Rocket")

    def createProjectile(self, worm):
        return Rocket(worm)
