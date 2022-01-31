import numpy as np
import pygame

import Globals
from Physics.Collision import Collision


class Terrain:
    def __init__(self):
        self.nodes = []
        self.nodeLinks = []

    def addNode(self, position):
        position = np.array(list(map(float, position)))
        self.nodes.append(position)
        self.nodeLinks.append([])

    def link(self, node1, node2):
        if node1 > node2:
            node1, node2 = node2, node1
        if node2 not in self.nodeLinks[node1]:
            self.nodeLinks[node1].append(node2)

    @property
    def edges(self):
        result = []
        for node, neighbors in enumerate(self.nodeLinks):
            for node2 in neighbors:
                result.append((node, node2))
        return result

    def draw(self):
        for p in self.nodes:
            pygame.draw.circle(Globals.Screen, "white", p, Globals.TerrainSize)

        for l in self.edges:
            pygame.draw.line(Globals.Screen, "white", self.nodes[l[0]], self.nodes[l[1]], Globals.TerrainSize * 2)

    def getCollision(self, collider, center=None):
        if center is None:
            center = collider.position

        for line in self.edges:
            start = self.nodes[line[0]]
            lineUnit = self.nodes[line[1]] - start
            lineSize = np.linalg.norm(lineUnit, 2)
            lineUnit /= lineSize

            relative = center - start
            dot = np.linalg.multi_dot((relative, lineUnit))
            if dot < 0 or dot > lineSize:
                continue
            projected = lineUnit * dot
            normal = relative - projected
            normalSize = np.linalg.norm(normal, 2)
            deltaSize = Globals.TerrainSize + collider.size - normalSize
            if deltaSize < 0 or normalSize == 0:
                continue
            normal /= normalSize
            delta = -normal * deltaSize
            return Collision(collider, None, delta, center)

        for pos in self.nodes:
            relative = center - pos
            distance = np.linalg.norm(relative, 2)
            size = Globals.TerrainSize + collider.size - distance

            if size > 0 and distance > 0:
                delta = -relative / distance * size
                return Collision(collider, None, delta, center)

        return None
