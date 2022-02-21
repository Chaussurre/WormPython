import numpy
import pygame.font
pygame.init()


#global variables
listDynamicObjects = []
listPhysicObjects = []
Screen = None
Terrain = None
WeaponSelected = None
MainGame = None

#parameters
TimeSlowSpace = 1.0/5.0
CollisionTestRate = 40
ScreenSize = (1000, 600)
FrameRate = 20
Gravity = numpy.array((0, 250))
TerrainSize = 30
Bounciness = 0.4
MoveJumps = numpy.array((60, -130))
Font = "Comic Sans MS"
