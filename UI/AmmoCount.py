import numpy as np
import pygame.draw

import Globals
from EventManager.EventManager import eventManager
from GameLogic import TurnManager
from UI import UIGlobals
from UI.Panel import Panel
from UI.Text import Text


class AmmoCount(Panel):
    def __init__(self):
        Panel.__init__(self,
                       np.array(UIGlobals.ammoCountPosition),
                       np.array(UIGlobals.ammoCountSize),
                       UIGlobals.weaponPanelColor)
        self.addChild(Text(self.position - self.size / 2, "ammos:", 15))
        self.ammo = 0
        self.resetAmmo()
        eventManager.addListener("shot", self.consumeAmmo)
        eventManager.addListener("new turn", self.resetAmmo)

    def drawUI(self):
        Panel.drawUI(self)
        pos = self.position + np.array((20 - self.size[0] / 2, self.size[1] * 0.25))
        for x in range(self.ammo):
            pygame.draw.circle(Globals.Screen, "white", pos, 5)
            pos += np.array((13, 0))

    def resetAmmo(self, *args):
        self.ammo = TurnManager.ActionPerTurn

    def consumeAmmo(self, *args):
        if self.ammo > 0:
            self.ammo -= 1
