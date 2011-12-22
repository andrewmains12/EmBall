from __future__ import division
import os
import sys
import pygame
import math

"""This module provides a suite of utilitarian functions to perform tasks such
as loading images etc"""
main_dir = os.path.split(os.path.abspath(__file__))[0]

#Debug constants
log_dir = os.path.join(main_dir, "log")


#Image Utilities

img_dir = os.path.join(main_dir, "Images")

ImgFiles = {"ball" :  "ball.png",
            "paddle" : "paddle.png",
            "blue" : "Blocks/blue.png",
            "red"  : "Blocks/red.png",
            "unbreakable" : "Blocks/unbreakable.png",
            "startBackground" : "Backgrounds/bricks.png" 
}


#File helpers:

def get_path_for_level(levelName):
    levelsDir = os.path.join(main_dir, "Levels")
    path = os.path.join(levelsDir, levelName)
    return path

def load_image(imgName):
    "loads an image, prepares it for play"
    f = os.path.join(img_dir, ImgFiles[imgName])

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
    file = os.path.join(main_dir, 'data', file)
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
def debugPrint(x):
    if debug:
        print (x)

    if logFile != None:
        with open(os.path.join(log_dir, logFile), 'w') as f: 
                f.write(str(x) + '\n')
            
