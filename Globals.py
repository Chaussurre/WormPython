import numpy
import pygame.font
pygame.init()


#global variables
listDynamicObjects = []
listPhysicObjects = []
Screen = None
Terrain = None
WeaponSelected = None

#parameters
ScreenSize = (1000, 600)
FrameRate = 60
Gravity = numpy.array((0, 250))
TerrainSize = 30
Bounciness = 0.4
MoveJumps = numpy.array((30, -100))
Font = "Comic Sans MS"
