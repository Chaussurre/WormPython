class Team:
    def __init__(self, color):
        self.listWorms = []
        self.color = color
        self.wormIndex = 0

    @property
    def movingWorm(self):
        return self.listWorms[self.wormIndex]

    def assignWorm(self, worm):
        worm.team = self
        self.listWorms.append(worm)

    def removeWorm(self, worm):
        if self.listWorms[self.wormIndex] == worm:
            self.listWorms.remove(worm)
            self.getNextPlaying()
        else:
            self.listWorms.remove(worm)

    def isAlive(self):
        return len(self.listWorms) > 0

    def getNextPlaying(self):
        if self.isAlive():
            worm = self.listWorms[self.wormIndex]
            self.wormIndex += 1
            self.wormIndex = self.wormIndex % len(self.listWorms)
            return worm
        return None

