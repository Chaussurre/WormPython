import numpy as np

from EventManager.EventManager import eventManager
from UI import UIGlobals
from UI.Button import Button


class WeaponButton(Button):
    def __init__(self, weapon, sizeFont=30):
        Button.__init__(self,
                        position=np.array((UIGlobals.weaponPanelPosition[0],
                                           UIGlobals.weaponPanelMargin +
                                           UIGlobals.weaponButtonsMargin +
                                           UIGlobals.weaponButtonsSize / 2)),
                        size=np.array((UIGlobals.weaponPanelSize - 2 * UIGlobals.weaponButtonsMargin,
                                       UIGlobals.weaponButtonsSize)),
                        text=weapon.name,
                        sizeFont=sizeFont)
        self.weapon = weapon
        UIGlobals.listWeaponButtons.append(self)

    def call(self):
        eventManager.triggerEvent(self.weapon.eventChoose, self.weapon)
