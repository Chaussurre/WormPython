import Globals
from UI import UIGlobals

ActiveTime = 2


class IntroNewTurn:
    def __init__(self, team):
        self.Panel, Text = UIGlobals.IntroNewTurnUI
        self.Panel.visible = True
        Text.text = f"{team.name} player's turn"
        self.Panel.color = team.color
        self.time = 0

    def update(self):
        Globals.Terrain.draw(0)
        for DO in Globals.listDynamicObjects:
            DO.update(100)
        self.time += 1 / Globals.FrameRate
        if self.time > ActiveTime:
            self.Panel.visible = False
            return "MoveWormPhase",
        return None
