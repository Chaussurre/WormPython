from Weapon.Projectiles.Grenade import Grenade
from Weapon.Weapon import Weapon


class GrenadeLauncher(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Grenade")

    def createProjectile(self, worm):
        return Grenade(worm)
