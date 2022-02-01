import numpy as np

import Globals
from UI.Button import Button
from UI.Panel import Panel
from UI.Text import Text
from UI.UIElement import RootUI

weaponPanelSize = 200
weaponPanelMargin = 0
weaponPanelColor = (0, 0, 100)

weaponButtonsMargin = 20
weaponButtonsSize = 40

def InitUI():
    WeaponPanelPosition = (Globals.ScreenSize[0] - weaponPanelSize / 2 - weaponPanelMargin, Globals.ScreenSize[1] / 2)
    WeaponPanel = Panel(position=np.array(WeaponPanelPosition),
                        size=np.array((weaponPanelSize, Globals.ScreenSize[1] - weaponPanelMargin * 2)),
                        color=weaponPanelColor)
    RootUI.addChild(WeaponPanel)

    GrenadeButton = Button(position=np.array((WeaponPanelPosition[0],
                                              weaponPanelMargin + weaponButtonsMargin + weaponButtonsSize / 2)),
                           size=np.array((weaponPanelSize - 2 * weaponButtonsMargin, weaponButtonsSize)),
                           text="Grenade",
                           sizeFont=30)
    WeaponPanel.addChild(GrenadeButton)