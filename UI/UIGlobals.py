import Globals
from UI.UIElement import UIElement

weaponPanelSize = 200
weaponPanelMargin = 0
weaponPanelColor = (0, 0, 100)
weaponPanelPosition = (Globals.ScreenSize[0] - weaponPanelSize / 2 - weaponPanelMargin, Globals.ScreenSize[1] / 2)

weaponButtonsMargin = 20
weaponButtonsSize = 40

ammoCountSize = (50, 40)
ammoCountPosition = (60, 40)

IntroNewTurnUI = (None, None)
IntroNewTurnSize = (530, 80)

listWeaponButtons = []
RootUI = UIElement()