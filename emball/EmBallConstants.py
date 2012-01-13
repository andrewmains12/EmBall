import pygame
from pygame.locals import USEREVENT
"""Contains the constants used by other modules"""


#Physical Constants

SCREENDIMS = 0, 0, 480, 520
SCREENRECT = pygame.rect.Rect(SCREENDIMS)
RIGHT = UP = 1
LEFT = DOWN = -1

#Paddle Constants
PADDLESPEED = 10
PADDLEDEFLECT = 2
PADDLESTART = SCREENRECT.centerx, SCREENRECT.bottom - 20

#Ball Constants
BALLSPEED = (7,7)  
BALLSTART = (5, SCREENRECT.centery)
BALLDIR = (1,1)

#Block Constants
BLOCKSIZE = 32,24

#Collision constants
COLLISIONSTEP = 1

#Game Constants
LIVES = 3
SCORE = 0

#Font constants
DEFAULTFONTSIZE = 40
FONTCOLOR = 'black'

#EmBall event constants
BALLDROP = USEREVENT + 1



#Messages
WIN_LOSS_MESSAGES = {
          'drop' : "Si puo fare!",
          'win' : "Victory!!!" ,
          'loss' : "Bad news bears, you lost :(.",
          'rtnToMain' : "Press any key to return to main menu"
          }
