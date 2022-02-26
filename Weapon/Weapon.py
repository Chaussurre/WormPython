class Weapon:
    def __init__(self, name):
        self.name = name
        self.eventChoose = f"Chosen {name}"

    def createProjectile(self, worm):
        pass

    def tryShoot(self, targetPos, worm, projectile):
        relative = targetPos - worm.position
        projectile.impulse(relative)