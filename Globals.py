import numpy
import numpy as np
import pygame.font
pygame.init()


#global variables
listDynamicObjects = []
listPhysicObjects = []
Screen = None
Terrain = None
MainGame = None
Wind = np.array((0, 0))

#parameters
TimeSlowSpace = 1.0/5.0
CollisionTestRate = 30
ScreenSize = (1000, 600)
FrameRate = 20
Gravity = numpy.array((0, 250))
TerrainSize = 10
Bounciness = 0.4
MoveJumps = numpy.array((60, -130))
Font = "Comic Sans MS"
WindVariance = (30, 100)