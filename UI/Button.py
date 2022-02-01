import numpy as np

from UI.Panel import Panel
from UI.Text import Text
from UI.UIElement import UIElement


class Button(UIElement):
    def __init__(self, position=np.array((0, 0)), size=np.array((30, 30)), text="Button", sizeFont=30):
        UIElement.__init__(self, position=position)
        self.text = Text(position - size / 2, text=text, size=sizeFont)
        self.panel = Panel(position, size=size)
        self.addChild(self.panel)
        self.addChild(self.text)
        self.callBacks = []

    def addCallBack(self, callBack):
        self.callBacks.append(callBack)

    def call(self):
        for x in self.callBacks:
            x()

