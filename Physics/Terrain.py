import numpy as np
import pygame
import Globals
from Physics.Collision import Collision


class Terrain:
    def __init__(self):
        self.nodes = []
        self.nodeLinks = []
        self.destroyedZones = []
        self.nextDestroyedZones = []

    def updateDestroyedZones(self):
        for collider, center, _ in self.nextDestroyedZones:
            collider.position = center
            self.destroyedZones.append(collider)

    def addNode(self, position):
        position = np.array(list(map(float, position)))
        self.nodes.append(position)
        self.nodeLinks.append([])

    def link(self, node1, node2):
        if node1 > node2:
            node1, node2 = node2, node1
        if node2 not in self.nodeLinks[node1]:
            self.nodeLinks[node1].append(node2)

    def destroy(self, collider, center=None, time=0):
        if center is None:
            center = collider.position

        if self.getCollision(collider, center=center, time=time) is not None:
            self.nextDestroyedZones.append((collider, center, time))

    @property
    def edges(self):
        result = []
        for node, neighbors in enumerate(self.nodeLinks):
            for node2 in neighbors:
                result.append((node, node2))
        return result

    def draw(self, time):
        for p in self.nodes:
            pygame.draw.circle(Globals.Screen, "white", p, Globals.TerrainSize)

        for l in self.edges:
            pygame.draw.line(Globals.Screen, "white", self.nodes[l[0]], self.nodes[l[1]], Globals.TerrainSize * 2)

                pygame.draw.circle(Globals.Screen, "black", pos, collider.size)

    def getCollision(self, collider, center=None, time=0):
        if center is None:
            center = collider.position

        for line in self.edges:
            start = self.nodes[line[0]]
            lineUnit = self.nodes[line[1]] - start
            lineSize = np.linalg.norm(lineUnit, 2)
            lineUnit /= lineSize
            return None

            relative = center - start
        return Collision(collider, None, delta, center)

    def getNonDestroyedCollision(self, collider, center=None):
        if center is None:
            center = collider.position
        collision = self.getCollisionWithEdges(collider, center)
        if collision is None:
            collision = self.getCollisionWithNodes(collider, center)
        return collision

    def isPointInTerrain(self, point, destroyedZone):
        if isPointCoveredBy(point, destroyedZone):
            return False
        for edge in self.edges:
            normal = self.getNormalWithEdge(point, edge)
            if normal is not None and np.linalg.norm(normal, 2) < Globals.TerrainSize:
                return True

        for node in self.nodes:
            if np.linalg.norm(node - point, 2) < Globals.TerrainSize:
                return True
        return False

    def getNormalWithEdge(self, point, edge):
        start = self.nodes[edge[0]]
        lineUnit = self.nodes[edge[1]] - start
        lineSize = np.linalg.norm(lineUnit, 2)
        lineUnit /= lineSize

        relative = point - start
        dot = np.linalg.multi_dot((relative, lineUnit))
        if dot < 0 or dot > lineSize:
            return None
        projected = lineUnit * dot
        return relative - projected

    def getCollisionWithEdges(self, collider, center):
        for edge in self.edges:
            normal = self.getNormalWithEdge(center, edge)
            if normal is None:
                continue
            normalSize = np.linalg.norm(normal, 2)
            deltaSize = Globals.TerrainSize + collider.size - normalSize
            if deltaSize < 0 or normalSize == 0:
                continue
            normal /= normalSize
            delta = -normal * deltaSize
            return Collision(collider, None, delta, center)
        return None

    def getCollisionWithNodes(self, collider, center):
        for nodePos in self.nodes:
            relative = center - nodePos
            distance = np.linalg.norm(relative, 2)
            size = Globals.TerrainSize + collider.size - distance

            if size > 0 and distance > 0:
                delta = -relative / distance * size
                return Collision(collider, None, delta, center)
        return None


def isPointCoveredBy(point, zones):
    for zone, center in zones:
        if zone.HasPoint(point, center=center):
            return True
    return False
