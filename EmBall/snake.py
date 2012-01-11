import os, sys
import pygame
from pygame.locals import *

IMAGEPATH = "/Users/andrewmains/Documents/Coding/game/PurpGuy.gif"
ARROWKEYS = set((K_RIGHT, K_LEFT, K_UP, K_DOWN))

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
        
        self.clock = pygame.time.Clock()
    def getSprites(self):
        self.purpDude = purpDude()
        self.sprites = pygame.sprite.RenderPlain((self.purpDude))

    def MainLoop(self):
        self.getSprites()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key in ARROWKEYS:
                        self.purpDude.move(event.key)

            self.sprites.draw(self.screen)
            pygame.display.flip()
            

class purpDude(pygame.sprite.Sprite):
    
    x_dist = y_dist = 1
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGEPATH)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

    
    def move (self, key):
        xmove = ymove = 0

        if key == K_LEFT:
            xmove = - purpDude.x_dist
        elif key == K_RIGHT:
            xmove = purpDude.x_dist
        elif key == K_UP:
            ymove = - purpDude.y_dist
        elif key == K_DOWN:
            ymove =  purpDude.y_dist

        self.rect.move_ip(xmove, ymove)

def main():
    m = PyManMain()
    m.MainLoop()
