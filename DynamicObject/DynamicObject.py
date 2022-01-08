class DynamicObject:
    def __init__(self, screen, listDOs, position=(0, 0)):
        self._rect = None
        listDOs.append(self)
        self.screen = screen
        self.x = 0
        self.y = 0
        self.position = position

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    def draw(self):
        return None

    def update(self):
        self.rect = self.draw()

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]