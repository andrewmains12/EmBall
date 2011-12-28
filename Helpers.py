from __future__ import division
import os
import sys
import pygame

import math
import time

"""This module provides a suite of utilitarian functions to perform tasks such
as loading images etc"""
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

#Debug constants
LOG_DIR = os.path.join(MAIN_DIR, "log")


#Image Utilities

IMG_DIR = os.path.join(MAIN_DIR, "Images")

IMG_FILES = {"ball" :  "ball.png",
            "paddle" : "paddle.png",
            "blue" : "Blocks/blue.png",
            "red"  : "Blocks/red.png",
            "unbreakable" : "Blocks/unbreakable.png",
            "startBackground" : "Backgrounds/bricks.png" 
}


#File helpers:

def get_path_for_level(levelName):
    levelsDir = os.path.join(MAIN_DIR, "Levels")
    path = os.path.join(levelsDir, levelName)
    return path

def load_image(imgName):
    "loads an image, prepares it for play"
    f = os.path.join(IMG_DIR, IMG_FILES[imgName])

    try:
        surface = pygame.image.load(f)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(f, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(MAIN_DIR, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

 

###################################
###     Exception Types ##########

class EmBallError (Exception):
    """Base class for problems occuring in EmBall"""
    pass

class InitializationError(EmBallError):
    """Raised for problems with initializing the game and or objects

    Attributes:
    reason: reason for the exception
    
    """
    def __init__(self, reason):
        self.reason = reason



#Movement Helpers

"""Takes in a vector represented as a tuple and returns a normalized vector"""    
def normalize (vector):
    x,y = vector
    length = math.sqrt(x*x + y*y)
    return x / length, y / length

###########
# Debug Functions
#############
def debugPrint(x, debug_level=0):
    if debug:
        print (x)
    
    if logFile != None:
        with open(os.path.join(LOG_DIR, logFile), 'w') as f: 
                f.write(str(x) + '\n')
            
def getLogName ():
    """Returns a name for a new log file (in the log directory"""

    return os.path.join (LOG_DIR, time.strftime("%H:%M-%m-%Y"))

def isConsoleEscape (event):
    """
    Returns true iff EVENT represents the escape sequence for the console (ctrl-c)
    """
    ctrl_pressed = pygame.key.get_mods() & pygame.locals.KMOD_CTRL

    return ctrl_pressed and \
           event.type == pygame.locals.KEYDOWN and\
           event.key == pygame.locals.K_c
    
    
