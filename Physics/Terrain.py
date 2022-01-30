import pygame

import Globals


class Terrain:
    def __init__(self):
        self.nodes = []
        self.nodeLinks = []

    def addNode(self, position):
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