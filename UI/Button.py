import numpy as np

from UI.Panel import Panel
from UI.Text import Text
from UI.UIElement import UIElement
from Input import Input


class Button(UIElement):
    def __init__(self,
                 position=np.array((0, 0)),
                 size=np.array((30, 30)),
                 text="Button", sizeFont=30,
                 color="blue",
                 pressedColor=(0, 0, 150),
                 inactiveColor=(0, 0, 125)):
        UIElement.__init__(self, position=position)
        self.active = True
        self.text = Text(position - size / 2, text=text, size=sizeFont)
        self.panel = Panel(position, size=size, color=color)
        self.color = color
        self.pressedColor = pressedColor
        self.inactiveColor = inactiveColor
        self.addChild(self.panel)
        self.addChild(self.text)
        self.callBacks = [lambda: print("clicked button")]
        self.held = False

    def addCallBack(self, callBack):
        self.callBacks.append(callBack)

    def call(self):
        for x in self.callBacks:
            x()

    def drawUI(self):
        if self.active:
            if self.held:
                self.panel.color = self.pressedColor
                if Input.mouseClickUp(0):
                    self.held = False
                    if self.panel.isMouseOver():
                        self.call()
            else:
                self.panel.color = self.color
                if Input.mouseClickDown(0) and self.panel.isMouseOver():
                    self.held = True
        else:
            self.panel.color = self.inactiveColor
        UIElement.drawUI(self)

