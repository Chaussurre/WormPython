import numpy
import pygame.font
pygame.init()

ScreenSize = (1000, 600)
listDynamicObjects = []
listPhysicObjects = []
FrameRate = 60
Screen = None
Gravity = numpy.array((0, 250))
TerrainSize = 30
Terrain = None
Bounciness = 0.4
MoveJumps = numpy.array((30, -100))
Font = "Comic Sans MS"
