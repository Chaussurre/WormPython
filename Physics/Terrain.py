import random

import numpy as np
import pygame
import Globals
from Physics.Collision import Collision
from UI import UIGlobals


class Terrain:
    def __init__(self):
        self.nodes = []
        self.nodeLinks = []
        self.triangles = []
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

    def addTriangle(self, node1, node2, node3):
        t = tuple(sorted((node1, node2, node3)))
        if t not in self.triangles:
            self.triangles.append(t)

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
        pygame.draw.polygon(Globals.Screen, "blue", self.nodes[1::])

        for p in self.nodes[1::]:
            pygame.draw.circle(Globals.Screen, "white", p, Globals.TerrainSize)

        for a, b in self.edges:
            pygame.draw.line(Globals.Screen, "white", self.nodes[a], self.nodes[b], Globals.TerrainSize * 2)

        for zone in self.destroyedZones:
            pygame.draw.circle(Globals.Screen, "black", zone.position, zone.size)
        for collider, pos, t in self.nextDestroyedZones:
            if time >= t:
                pygame.draw.circle(Globals.Screen, "black", pos, collider.size)

    def getCollision(self, collider, center=None, time=0):
        if center is None:
            center = collider.position

        collision = self.getNonDestroyedCollision(collider, center)

        destroyedZones = list(map(lambda x: (x, x.position), self.destroyedZones))
        for zone, c, t in self.nextDestroyedZones:
            if t <= time:
                destroyedZones.append((zone, c))

        if collision is None and not isPointCoveredBy(center, destroyedZones):
            return None

        if collision is not None:
            delta = collision.delta / np.linalg.norm(collision.delta) * collider.size
            if not isPointCoveredBy(center + delta, destroyedZones):
                return collision

        points = []
        for n in range(0, 100):
            angle = 2 * 3.14 * n / 100
            point = np.array((np.cos(angle), np.sin(angle))) * collider.size + center
            if self.isPointInTerrain(point, destroyedZones):
                points.append(point)

        if len(points) == 0:
            return None

        delta = np.array((0.0, 0.0))
        for point in points:
            delta += center - point
        delta /= len(points)

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

        def TriangleArea(t):
            p1, p2, p3 = t
            l1 = np.linalg.norm(p1 - p2)
            l2 = np.linalg.norm(p1 - p3)
            l3 = np.linalg.norm(p3 - p2)
            semi = (l1 + l2 + l3) / 2
            s = semi * (semi - l1) * (semi - l2) * (semi - l3)
            if s < 0:
                return 0
            return np.sqrt(s)

        for a, b, c in self.triangles:
            triangles = [(point, self.nodes[b], self.nodes[c]),
                         (self.nodes[a], point, self.nodes[c]),
                         (self.nodes[a], self.nodes[b], point)]
            mainTriangle = [self.nodes[a], self.nodes[b], self.nodes[c]]
            if np.abs(sum(map(TriangleArea, triangles)) - TriangleArea(mainTriangle)) < 10:
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


def GenTerrain(genAlgo="block"):
    if genAlgo == "block":
        genBlockTerrain()
    else:
        terrain = Terrain()
        terrain.addNode((100, 400))
        terrain.addNode((700, 400))
        terrain.link(0, 1)
        Globals.Terrain = terrain
        print("doesn't know generation algo", genAlgo)


# terrain gen parameters
numPointUp = 15
numPointDown = 5
HorizontalVariance = 0.8, 1
VerticalVariance = 0.1, 1


def genBlockTerrain():
    terrain = Terrain()
    size = np.array(((Globals.ScreenSize[0] - UIGlobals.weaponPanelSize), Globals.ScreenSize[1]))
    center = size / 2 + np.array((0, 100))
    terrain.addNode(center)
    last = None
    for i in range(1, numPointUp + numPointDown):
        var = random.uniform(*HorizontalVariance), random.uniform(*VerticalVariance)
        angle = i / numPointDown * 3.14
        if i > numPointDown:
            angle = (i - numPointDown) / numPointUp * 3.14 + 3.14
        point = np.array((np.cos(angle) * size[0] / 2 * var[0],
                          np.sin(angle) * size[1] / 2 * var[1]))
        terrain.addNode(point + center)
        if last is not None:
            terrain.link(last, i)
            terrain.addTriangle(0, last, i)
        last = i
    terrain.addTriangle(0, last, 1)
    terrain.link(last, 1)
    Globals.Terrain = terrain
