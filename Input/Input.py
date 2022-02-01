import pygame
import numpy as np

KeyList = []
KeyDownList = []
KeyUpList = []

mouseButtons = []
mouseButtonsDown = []
mouseButtonsUp = []

def mousePos():
    return np.array(pygame.mouse.get_pos())

def mouseClick(button=0):
    return button in mouseButtons

def mouseClickDown(button=0):
    return button in mouseButtonsDown

def mouseClickUp(button=0):
    return button in mouseButtonsUp

def mouseInRect(rect):
    pos = mousePos()
    return rect[0][0] <= pos[0] <= rect[1][0] and rect[0][1] <= pos[1] <= rect[1][1]

def SetKeyDown(key):
    KeyDownList.append(key)
    KeyList.append(key)

def SetKeyUp(key):
    KeyUpList.append(key)
    KeyList.remove(key)

def UpdateKeys():
    KeyDownList.clear()
    KeyUpList.clear()

    mouseButtonsUp.clear()
    mouseButtonsDown.clear()

    for button, pressed in enumerate(pygame.mouse.get_pressed(3)):
        if pressed:
            if button not in mouseButtons:
                mouseButtons.append(button)
                mouseButtonsDown.append(button)
        else:
            if button in mouseButtons:
                mouseButtons.remove(button)
                mouseButtonsUp.append(button)

def IsKey(key):
    return key in KeyList

def IsKeyDown(key):
    return key in KeyDownList

def IsKeyUp(key):
    return key in KeyUpList

def GetKeyBoardDirection():
    direction = np.array([0, 0])
    if IsKey(pygame.K_LEFT) or IsKey(pygame.K_q):
        direction += np.array([-1, 0])
    if IsKey(pygame.K_RIGHT) or IsKey(pygame.K_d):
        direction += np.array([1, 0])
    if IsKey(pygame.K_UP) or IsKey(pygame.K_z):
        direction += np.array([0, -1])
    if IsKey(pygame.K_DOWN) or IsKey(pygame.K_s):
        direction += np.array([0, 1])
    return direction

