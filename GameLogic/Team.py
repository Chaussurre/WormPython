class Team:
    def __init__(self, color, name):
        self.name = name
        self.listWorms = []
        self.color = color
        self.wormIndex = 0

    @property
    def movingWorm(self):
        if len(self.listWorms) == 0:
            return None
        return self.listWorms[self.wormIndex]

    def assignWorm(self, worm):
        worm.team = self
        self.listWorms.append(worm)

    def removeWorm(self, worm):
        indexWorm = self.listWorms.index(worm)
        if self.listWorms[self.wormIndex] == worm:
            self.listWorms.remove(worm)
            self.setNextWorm()
        else:
            if indexWorm < self.wormIndex:
                self.wormIndex -= 1
            self.listWorms.remove(worm)

    def isAlive(self):
        return any(map(lambda worm: not worm.isDead(), self.listWorms))

    def getNextPlaying(self):
        if self.isAlive():
            return self.listWorms[self.wormIndex]
        return None

    def setNextWorm(self):
        if self.isAlive():
            self.wormIndex += 1
            self.wormIndex = self.wormIndex % len(self.listWorms)

