import pygame

KeyList = []
KeyDownList = []
KeyUpList = []


def SetKeyDown(key):
    KeyDownList.append(key)
    KeyList.append(key)

def SetKeyUp(key):
    KeyUpList.append(key)
    KeyList.remove(key)

def UpdateKeys():
    KeyDownList.clear()
    KeyUpList.clear()

def IsKey(key):
    return key in KeyList

def IsKeyDown(key):
    return key in KeyDownList

def IsKeyUp(key):
    return key in KeyUpList

def GetKeyBoardDirection():
    x = 0
    y = 0
    if IsKey(pygame.K_LEFT) or IsKey(pygame.K_q):
        x += -1
    if IsKey(pygame.K_RIGHT) or IsKey(pygame.K_d):
        x += 1
    if IsKey(pygame.K_UP) or IsKey(pygame.K_z):
        y += -1
    if IsKey(pygame.K_DOWN) or IsKey(pygame.K_s):
        y += 1
    return x, y

