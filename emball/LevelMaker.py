#!/usr/bin/env python2.6

from xml.dom import minidom as xml
from optparse import OptionParser
import os
import sys

#Pygame imports
import pygame
from pygame.locals import *


#EmBall imports
from EmBall import GameWindow
from level import Level
from Blocks import get_block

from Helpers import get_path_for_level
import Helpers


class LevelMaker (GameWindow):
    
    def __init__ (self, lvl_path):
        super(LevelMaker, self).__init__()
        self.level = Level(lvl_path)
        
        #Init groups
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        #Set object following cursor
        self.item_following_cursor = pygame.sprite.GroupSingle()
        
        blocks = self.level.blocks

        #Add level blocks to groups
        self.all.add(*blocks)
        self.blocks.add(*blocks)

        self.background = self.level.background
        self.all.draw(self.background)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def gameLoop (self):
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

                elif event.type == MOUSEBUTTONDOWN:
                    self.place_item()
            
            pygame.event.pump()
            keystate = pygame.key.get_pressed()
            mods = pygame.key.get_mods()

            self.all.clear(self.screen, self.background)

            #Mouse handling
            #Move item_following_cursor with mouse
            self.move_item(pygame.mouse.get_pos())
            self.handle_keys(keystate, mods)
            dirty = self.all.draw(self.screen)
            pygame.display.update(dirty)

            self.clock.tick(40)

    #Item placement and movement

    def place_item(self):
        pass

    def move_item (self, pos):
        if self.item_following_cursor:
            item = self.item_following_cursor.sprite

            #Move item to new pos
            item.rect.center = pos
            
    #Key actions
    def handle_keys(self, keystate, mods):
        if keystate[K_b]:
            self.get_new_block()

        elif keystate[K_s] and (mods & KMOD_CTRL):
            self.save()

    def get_new_block (self):
        pos = pygame.mouse.get_pos()
        block = get_block('basic', 
                          color='red',
                          position=pos)
        #Add block to appropriate groups
        self.all.add(block)
        self.item_following_cursor.add(block)
        
#        self.screen.fill(block
        
    def save (self):
        print ("Saved, in theory")



##########################################
# Script bits (option parsing and the like

def initParser (parser):
    parser.set_defaults(debug=False, logFile=None)
    parser.add_option ("-d", action="store_true", dest="debug",\
                     help = "Causes program to be run in debug mode")
    parser.add_option ("-l", action="store", dest="logFile",\
                     help = "Causes debug messages to be logged")

   
def main():
    
    #Do option parsing
    parser = OptionParser()
    initParser(parser)
    options, args = parser.parse_args()
    Helpers.debug = options.debug
    Helpers.logFile = options.logFile
    
    if len(args) != 0: 
        lvl_name = args[0]

    else: 
        lvl_name = "new_lvl.lvl"
                    
    LevelMaker(get_path_for_level(lvl_name)).gameLoop()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
    




                
                
