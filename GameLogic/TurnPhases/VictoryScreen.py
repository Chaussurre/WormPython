import Globals
from EventManager.EventManager import eventManager
from UI import UIGlobals

ActiveTime = 2


class VictoryScreen:
    def __init__(self, team):
        self.Panel, Text = UIGlobals.IntroNewTurnUI
        self.Panel.visible = True
        if team is None:
            Text.text = "Tie..."
            self.Panel.color = "white"
        else:
            Text.text = f"{team.name} player won!"
            self.Panel.color = team.color
        self.time = 0

    def update(self):
        Globals.Terrain.draw(0)
        for DO in Globals.listDynamicObjects:
            DO.update(100)
        self.time += 1 / Globals.FrameRate
        if self.time > ActiveTime:
            eventManager.triggerEvent("quit")
        return None
