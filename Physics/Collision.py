class Collision:
    def __init__(self, collider, otherCollider, delta, position):
        self.collider = collider
        self.otherCollider = otherCollider
        self.delta = delta
        self.position = position
