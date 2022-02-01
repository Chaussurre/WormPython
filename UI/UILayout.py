import numpy as np

import Globals
from UI import UIGlobals
from UI.Panel import Panel
from Weapon.WeaponButton import WeaponButton
from Weapon.WeaponList import listWeapons


def InitUI():
    WeaponPanel = Panel(position=np.array(UIGlobals.weaponPanelPosition),
                        size=np.array((UIGlobals.weaponPanelSize, Globals.ScreenSize[1] - UIGlobals.weaponPanelMargin * 2)),
                        color=UIGlobals.weaponPanelColor)
    UIGlobals.RootUI.addChild(WeaponPanel)

    for w in listWeapons:
        WeaponPanel.addChild(WeaponButton(w))



