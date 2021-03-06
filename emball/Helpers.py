"""This module provides a suite of utilitarian functions to perform tasks such
as loading images etc"""

from __future__ import division
import os
from os.path import dirname
import pygame

import math
import time

#Debug constants
DEBUG = False

#Directory related voodoo 
#Since resources such as images are in different places when the app
#is packaged than when it's in a module, we provide some hacky ways to update the 
#location of the di
#relative to a main directory. 

def set_dirs_relative(main_dir):
    """Sets all dir variables to their appropriate location relative to main_dir"""
    global MAIN_DIR, IMG_DIR, LOG_DIR
    
    MAIN_DIR = main_dir
    IMG_DIR = os.path.join(main_dir, "Images")
    LOG_DIR = os.path.join("/tmp","EmBall", "log")

#This assignment will probably get overridden
set_dirs_relative(dirname(dirname(os.path.abspath(__file__))))

LOG_FILE = None
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

def load_builtin_image(imgName):
    """Loads an image registered with the IMG_FILES dictionary"""
    if imgName not in IMG_FILES:
        raise KeyError ("%s is not a builtin image--\
see Helpers.IMG_FILES for valid arguments")
    return load_image(os.path.join(IMG_DIR, IMG_FILES[imgName]))

    
def load_image (img_path):
    try:
        surface = pygame.image.load(img_path)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%
                         (img_path, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    return [load_builtin_image(f) for f in files]

class DummySound:
    def play(self):
        pass

def load_sound(sound_file):
    if not pygame.mixer:
        return DummySound()
    sound_file = os.path.join(MAIN_DIR, 'data', sound_file)
    try:
        sound = pygame.mixer.Sound(sound_file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % sound_file)
    return DummySound()

 

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
        super(InitializationError, self).__init__ (reason)
        self.reason = reason


#Movement Helpers
def normalize (vector):
    """Takes in a vector represented as a tuple and returns a normalized vector"""    
    x,y = vector
    length = math.sqrt(x*x + y*y)
    return x / length, y / length

###########
# Debug Functions
#############
def debugPrint(x, debug_level=0):
    if DEBUG:
        print (x)

    if LOG_FILE != None:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR) 
        with open(os.path.join(LOG_DIR, LOG_FILE), 'w') as f: 
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
    
    
