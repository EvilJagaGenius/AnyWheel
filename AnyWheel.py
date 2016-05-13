#AnyWheel v.0.1
#2016, Nathan McNany
#Needs a working installation of Pygame and PyUserInput to work.
#Note: this is very much tailored to my Logitech Dual Action.  If it doesn't work with other pads, fiddle with the code.

import pygame, pykeyboard, sys
from pykeyboard import PyKeyboard
from pygame import *
pygame.init()

kbEmu = PyKeyboard()  #Short for keyboard emulator.
gamepad = None
if pygame.joystick.get_count() > 0:
    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()

WX = 360
WY = 360
window = pygame.display.set_mode((WX, WY), 0, 32)

TXTSIZE = 32
TXTFONT = pygame.font.Font(None, TXTSIZE)
TXTFONT.set_bold(True)

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

PETAL_COORDS = [(120,0), (240,0), (240,120), (240,240), (120,240), (0,240), (0,120), (0,0)]

#XYBA
BUTTONS = [0, 3, 2, 1]
COLORS = [BLUE, YELLOW, RED, GREEN]
COORDS = [(0, TXTSIZE), (TXTSIZE, 0), (TXTSIZE * 2, TXTSIZE), (TXTSIZE, TXTSIZE * 2)]
BASE_SET = ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx', 'yz,.', ':/@-']
CAPS_SET = ['ABCD', 'EFGH', 'IJKL', 'MNOP', 'QRST', 'UVWX', 'YZ?!', ';\\&_']
NUMS_SET = ['1234', '5678', '90*+', 'xx$`', '\'"~|', '=#%^', '<>[]', '{}()']


def getPetalSurf(petalString, colors=False):
    petalSurf = pygame.surface.Surface((TXTSIZE * 3, TXTSIZE * 3)) # A square
    for i in range(4):
        if colors == False:
            petalSurf.blit(TXTFONT.render(petalString[i], True, WHITE), COORDS[i])
        elif colors == True:
            petalSurf.blit(TXTFONT.render(petalString[i], True, COLORS[i]), COORDS[i])

    return petalSurf

def main():
    rtDown = False
    ltDown = False
    while True:
        facePress = False
        faceButton = None
        
        selectedSet = BASE_SET

        window.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 4:
                    ltDown = True
                elif event.button == 5:
                    rtDown = True
            elif event.type == JOYBUTTONUP:
                if event.button == 4:
                    ltDown = False
                elif event.button == 5:
                    rtDown = False
                elif event.button < 4:
                    facePress = True
                    faceButton = event.button



        if rtDown and not ltDown:
            selectedSet = CAPS_SET
        if ltDown and not rtDown:
            selectedSet = NUMS_SET


        #Determine where the stick's pointing and which petal to select.  -1 means no petal is selected.
        xPos = gamepad.get_axis(0)
        yPos = gamepad.get_axis(1)

        petal = -1
        if xPos >= .75:
            if yPos >= .75:
                petal = 3
            elif yPos <= -.75:
                petal = 1
            else:
                petal = 2

        elif xPos <= -.75:
            if yPos >= .75:
                petal = 5
            elif yPos <= -.75:
                petal = 7
            else:
                petal = 6

        else:
            if yPos >= .75:
                petal = 4
            elif yPos <= -.75:
                petal = 0

        if facePress and petal != -1:
            for i in range(4):
                if BUTTONS[i] == faceButton:
                    kbEmu.tap_key(selectedSet[petal][i])
                



        #Blit and schtuff
        for i in range(8):
            colors = False
            if i == petal:
                colors = True

            petalSurf = getPetalSurf(selectedSet[i], colors)
            window.blit(petalSurf, PETAL_COORDS[i])




        
        pygame.display.update()

        
if gamepad != None:
    main()
else:
    pygame.quit()
    print('Please plug in and turn on your gamepad, then restart the program.')
    input('Press ENTER to close')
    sys.exit()
