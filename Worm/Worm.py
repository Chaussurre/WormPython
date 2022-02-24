import numpy as np

import Globals
import pygame
from Physics.PhysicObject import PhysicObject
from Input import Input
from Physics import Trajectory
from UI.Panel import Panel

LifeMax = 100
LifeBarSize = 50


class Worm(PhysicObject, pygame.sprite.Sprite):
    def __init__(self, position=np.array((0.0, 0.0)), velocity=np.array((0.0, 0.0)), team=None):
        PhysicObject.__init__(self, position=position, velocity=velocity, size=15)
        self.image = pygame.image.load("Sprites/POYO.png")
        self.team = None
        if team is not None:
            self.team = team
            self.team.assignWorm(self)
        self.lifeBar = Panel(color="red")
        self.lifePanel = Panel(color="white", size=np.array((LifeBarSize + 2, 12)))
        self.lifePanel.addChild(Panel(color="black", size=np.array((LifeBarSize, 10))))
        self.lifePanel.addChild(self.lifeBar)
        self.life = LifeMax

    def draw(self, _):
        if self.life > 0:
            self.lifePanel.position = self.position + np.array((0, - 40))
            self.lifeBar.size = np.array((self.life / LifeMax * LifeBarSize, 10))
            self.lifeBar.position = self.lifePanel.position - (LifeMax - self.life) / LifeMax * LifeBarSize / 2 * np.array((1, 0))
            self.lifePanel.drawUI()
        pygame.draw.circle(Globals.Screen, self.team.color, self.screenPosition, 15)
        Globals.Screen.blit(self.image, (self.x - 15, self.y - 16))

    def inputMove(self):
        xMove = Input.GetKeyBoardDirection()[0]
        if xMove < 0:
            move = np.array(Globals.MoveJumps)
            move[0] *= -1
            self.impulse(move)
        if xMove > 0:
            self.impulse(Globals.MoveJumps)
        return xMove != 0

    def dealDamage(self, damage):
        if damage < 0:
            damage = 0
        self.life -= damage
        if self.life < 0:
            self.life = 0

    def destroy(self):
        super().destroy()
        if self.team is not None:
            self.team.removeWorm(self)

    def isDead(self):
        return not Trajectory.isInBounds(self.position) or self.life <= 0
