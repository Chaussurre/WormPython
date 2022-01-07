import pygame

from DynamicObject.DynamicObject import DynamicObject


class Worm(DynamicObject):

    def draw(self):
        pygame.draw.circle(self.screen, "green", self.position, 10)
        pygame.draw.circle(self.screen, "black", self.position, 12, 2)
        rect = pygame.draw.circle(self.screen, "white", self.position, 15, 3)
        return rect

    def update(self):
        DynamicObject.update(self)
        self.x += 1


