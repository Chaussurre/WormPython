import numpy as np

import Globals
from UI import UIGlobals
from UI.AmmoCount import AmmoCount
from UI.Panel import Panel
from UI.Text import Text
from UI.WindIndicator import WindIndicator
from Weapon.WeaponButton import WeaponButton
from Weapon.WeaponList.WeaponList import listWeapons


def InitUI():
    WeaponPanel = Panel(position=np.array(UIGlobals.weaponPanelPosition),
                        size=np.array(
                            (UIGlobals.weaponPanelSize, Globals.ScreenSize[1] - UIGlobals.weaponPanelMargin * 2)),
                        color=UIGlobals.weaponPanelColor)
    UIGlobals.RootUI.addChild(WeaponPanel)

    for i, w in enumerate(listWeapons):
        button = WeaponButton(w)
        button.position += np.array((0, UIGlobals.weaponButtonsSize+UIGlobals.weaponButtonsMargin))*i
        WeaponPanel.addChild(button)

    UIGlobals.RootUI.addChild(AmmoCount())

    introTurnPanel = Panel(position=np.array((Globals.ScreenSize[0] - UIGlobals.weaponPanelSize,
                                              Globals.ScreenSize[1])) / 2,
                           size=np.array(UIGlobals.IntroNewTurnSize),
                           color="blue")
    introTurnBlackPanel = Panel(position=np.array(introTurnPanel.position),
                                size=np.array(UIGlobals.IntroNewTurnSize) * 0.9,
                                color="black")
    introTurnText = Text(position=introTurnPanel.position - introTurnBlackPanel.size / 2, size=50,
                         text="Green Player's Turn")
    introTurnPanel.addChild(introTurnBlackPanel)
    introTurnBlackPanel.addChild(introTurnText)
    introTurnPanel.visible = False
    UIGlobals.RootUI.addChild(introTurnPanel)
    UIGlobals.IntroNewTurnUI = (introTurnPanel, introTurnText)
    WindIndicator()
