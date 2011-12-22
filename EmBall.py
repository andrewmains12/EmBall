#!/usr/bin/env python

from __future__ import division
import os.path
import sys
import math
from optparse import OptionParser

#Pygame imports
import pygame
from pygame.locals import *

#EmBall imports
from level import Level, load_level
import Helpers
from Helpers import *
from BaseGameObjects import *
from EmBallConstants import *    

########################


class GameWindow (object):
    """Defines an EmBall window with a screen, clock, etc. 
    
    Each GameWindow subclass should implement gameLoop, which is responsible for 
    events handling and the like
    """

    def __init__ (self, enclosing_game_window=None):
        """Initializes the GameWindow with a screen, clock and so on. 
           
           These attributes will be taken from enclosing_game_window if provided
        """

        if not enclosing_game_window:
            #Need to do pygame initialization if this is the first window
            pygame.init() 
            #Init screen
            winstyle = 0  # |FULLSCREEN
            bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
            self.screen = pygame.display.set_mode(SCREENRECT.size, 
                                                  winstyle, 
                                                  bestdepth)
            self.clock = pygame.time.Clock()

        else:
            self.screen = enclosing_game_window.screen
            self.clock  = enclosing_game_window.clock
            self.enclosing_game_window = enclosing_game_window

"""Game loop for mainscreen"""
class MainGame(GameWindow):
    
    def __init__ (self, startLevel):
        super(MainGame, self).__init__()
        self.startLevel = startLevel
        self.background = load_image("startBackground")

        #Init groups
        self.all = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.headers = pygame.sprite.Group()
        
        #Assign containers
        Button.containers = self.all, self.buttons
        
        xPos, yPos = SCREENRECT.center
        self.startButton = Button (
                           "START", (xPos, yPos + 50), color='green', 
                                fontsize=100)
        self.startButton.add(self.buttons, self.all)
        
        self.drawTitleScreen()
       

    def gameLoop(self):
        while True:
                        #Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

                elif event.type == MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()                    

                    if self.startButton.rect.collidepoint(mousePos):
                        #If hit start button:
                        self.game = Game(self.startLevel, self)
                        self.game.gameLoop()
                        self.all.clear(self.screen, self.background)
                        self.drawTitleScreen()
        
            
            
        #Redraw screen
            
            self.clock.tick(80)

    def drawTitleScreen(self):
        self.all.draw(self.background)
        self.screen.blit(self.background, (0,0)) 
        pygame.display.flip()

"""Game loop for pyball game--runs gameplay"""
class Game (GameWindow):
    def __init__(self, levelName, maingame):
        super(Game, self).__init__(enclosing_game_window=maingame)
        #Assign game constants
        self.lives = LIVES
        self.score = SCORE


        #Init groups
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
    
        #Assign groups
        Ball.containers = self.all, self.balls
        Paddle.containers = self.all, self.paddles
        BaseBlock.containers = self.all, self.blocks

        #Init messages
        self.messages = WIN_LOSS_MESSAGES

        #Init sprites

        self.level = load_level(levelName)
        for block in self.level.blocks:
            self.blocks.add(block)
            self.all.add(block)
        
        self.ball = Ball()
        self.paddle = Paddle()
        
        #Init background
        self.background = self.level.background
        self.screen.blit(self.background, (0,0))

    def handleCollisions(self):
        if (self.paddle.rect.colliderect(self.ball.rect)):
           
            self.ball.paddleBounce(self.paddle)

            debugPrint("Hit paddle")
            debugPrint(str(self) + "\n")

        else:
            hitBlocks = pygame.sprite.spritecollide \
                                    (self.ball, self.blocks, False)
            if len(hitBlocks) != 0:
            
                block = hitBlocks[0]
                self.ball.blockBounce(block)                
                block.hit()

    def handleDrop(self):
        #Lose life
        self.lives = self.lives - 1
        
        self.ball.kill()
        self.ball = Ball()

        if self.lives != 0:
        #Draw drop message to screen
            dropText = Text(self.messages['drop'])
            texts = pygame.sprite.Group(dropText)
            texts.draw(self.screen)
            pygame.display.flip()
            pygame.time.wait(500)
            texts.clear(self.screen, self.background)
            
    
        
    ###############################
    # Victory/Loss Methods
    ###############################
    """Checks for loss conditions  (lives gone)"""
    def lost(self):
        return (self.lives == 0)  

    def won (self):
        return not self.blocks.sprites

    def handleLoss(self):
        self.gameover(self.messages['loss'])

    def handleWin(self):
        self.gameover(self.messages['win'])

    def gameover (self, msg):
        self.gameover = True
        self.ball.kill()
        winLossTxt = Text(msg) 
                            
        rtnText = Text(self.messages['rtnToMain']) 
        
        texts = pygame.sprite.Group(rtnText, winLossTxt)

        winLossTxt.positionBelow (rtnText)
        texts.draw(self.screen)
        pygame.display.flip()
    """Returns a string represent the current state of the game--direction of 
       the ball, etc"""

    def __str__ (self):
        
        return \
"Ball: dir = %(ballD)s, pos = %(ballP)s \n\
Paddle: pos = %(paddleP)s" % \
            {'ballD' : str(self.ball.direction), \
             'ballP' : str(self.ball.rect.center), \
             'paddleP' : str(self.paddle.rect.center) \
             }


    def gameLoop(self, *args):
                
        while True:
            #Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Repost for outer loop to catch
                    pygame.event.post(pygame.event.Event(QUIT))
                    return
                
                elif event.type == BALLDROP:
                    self.handleDrop()

                        #Check for game over:
            if self.lost():
                self.handleLoss()
                break
                
            elif self.won():
                self.handleWin()
                break

            keystate = pygame.key.get_pressed()
              
            #Clear previously drawn sprites 
            self.all.clear(self.screen, self.background)

            #Handle collisions
            self.handleCollisions()
            #Update sprites                                       
            self.all.update()
            
            #Move paddle
            self.paddle.move(keystate[K_RIGHT] - keystate[K_LEFT])

            #Redraw screen
            
            dirty = self.all.draw(self.screen)
            pygame.display.update(dirty)
       
            self.clock.tick(40)

        #Endgame handling
        while True:
            
             #Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Repost for outer loop
                    pygame.event.post(pygame.event.Event(QUIT))
                    return

                elif event.type == KEYDOWN:
                    debugPrint("Exited game")
                    return
                
            
            self.clock.tick(40)



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
        level = args[0]

    else: 
        level = "basic"
                      
    MainGame(level).gameLoop()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
    





