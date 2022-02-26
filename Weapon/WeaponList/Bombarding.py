import numpy as np

import Globals
from UI import UIGlobals
from Weapon.Projectiles.Rocket import Rocket
from Weapon.Weapon import Weapon

initSpeed = (30, 0)
numRockets = 3
margin = 30

class Bombarding(Weapon):
    def __init__(self):
        Weapon.__init__(self, "Bombarding")

    def createProjectile(self, worm):
        return [Rocket(worm) for _ in range(numRockets)]

    def tryShoot(self, targetPos, worm, projectile):
        for i, p in enumerate(projectile):
            p.position = np.array((targetPos[0] + margin * i, 0))
            p.impulse(np.array(initSpeed))
