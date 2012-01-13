#!/usr/bin/env python

from __future__ import division
import sys
import re

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
    """
    Defines an EmBall window with a screen, clock, etc. 
    
    Each GameWindow subclass should, at a minimum, define event handlers, which will
    be used by the gameLoop.

    There are two ways of doing this:
       1. Autodiscovery: Methods matching GameWindow.EVENT_PATTERN will be registered
       by auto_discover_handlers.
       
       2. Manual registration: You can register manually events using addEventHandlers.
          This allows for more flexibility (handlers can be any callable object)
                
    """

    def __init__ (self, enclosing_game_window=None):
        """Initializes the GameWindow with a screen, clock and so on. 
           
           These attributes will be taken from enclosing_game_window if provided
        """        
        self.event_handlers = {}
        
        if not enclosing_game_window:
            #Need to do pygame initialization if this is the first window
            pygame.init() 
            #Init screen
            winstyle = 0  
            bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
            self.screen = pygame.display.set_mode(SCREENRECT.size, 
                                                  winstyle, 
                                                  bestdepth)
            self.clock = pygame.time.Clock()

        else:
            self.screen = enclosing_game_window.screen
            self.clock  = enclosing_game_window.clock
            self.enclosing_game_window = enclosing_game_window

    EVENT_PATTERN = r'^on_(.*)$'
    def auto_discover_handlers (self):
        """Find any methods matching EVENT_PATTERN and register them with their event
                
        Methods of the form on_<event_name> will be picked up by this method, and
        registered under event_name.

        event_name must be defined in the global scope (and should correspond to 
        a valid pygame event as well, though this is not checked here)
        """

        for name in dir(self):
            m = re.match(GameWindow.EVENT_PATTERN, name)            
            if m:
                event_name = m.groups()[0].upper()
                try:
                    self.registerEvent(eval(event_name), 
                                       getattr(self, name))
                except NameError:
                    raise InitializationError("No pygame event by name of " \
                                                  + event_name)

    
    def addEventHandlers(self, *event_handlers):
        
        """Register any event handlers with this GameWindow
        
        event_handlers: list of event, handler pairs

        Subclasses should call this method in order to register their own events
        with the GameWindow.

        Sample usage:
            
            self.addEventHandlers ((QUIT, lambda kwargs: sys.exit(0)),
                                  (MOUSEBUTTONDOWN, self.do_awesome_thing)
            )

        """
        for event, handler in event_handlers:
            self.registerEvent(event, handler)

    def registerEvent (self, event_type, handler):
        """Registers handler with event
        
        event_type: A pygame event type constant defined in pygame.locals
        handler: A function or bound method taking in an event and a dictionary of 
        arguments 
        """
        self.event_handlers[event_type] = handler

    def handleEvents(self, **args):
        """Checks for registered events and calls the appropriate handler
        
        Events are processed in order of registration.
        """
        for event in pygame.event.get():
            if event.type in self.event_handlers:
                self.event_handlers[event.type](event, **args)

class MainGame(GameWindow):
    """Game loop for mainscreen"""
    
    def __init__ (self, startLevel):
        super(MainGame, self).__init__()
        self.startLevel = startLevel
        self.background = load_builtin_image("startBackground")

        self.addEventHandlers((QUIT, self.on_quit),
                              (MOUSEBUTTONDOWN, self.on_mousebuttondown))
        #Init groups
        self.all = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.headers = pygame.sprite.Group()
        
        #Assign containers
        Button.containers = self.all, self.buttons
        
        #Register event handlers
        
        xPos, yPos = SCREENRECT.center
        self.startButton = Button (
                           "START", (xPos, yPos + 50), color='green', 
                                fontsize=100)
        self.startButton.add(self.buttons, self.all)        
        self.drawTitleScreen()
        
                    
    ######################################
    #Event handlers
    ######################################
    def on_mousebuttondown (self, event, **kwargs):
        """Starts main game if the mouse is clicking the startbutton"""        
        mousePos = pygame.mouse.get_pos()                    

        if self.startButton.rect.collidepoint(mousePos):
            #If hit start button:
            self.runGame(self.startLevel)

    def on_quit (self, event, **kwargs):
        """Run postgame cleanup upon receiving QUIT"""
        pygame.quit()
        sys.exit(0)
        
    def gameLoop(self):
        while True:
            self.handleEvents()                 
            self.clock.tick(80)

    def runGame (self, startLevel):
        Game(self.startLevel, self).gameLoop()
        self.all.clear(self.screen, self.background)
        self.drawTitleScreen()
                
        

    def drawTitleScreen(self):
        self.all.draw(self.background)
        self.screen.blit(self.background, (0,0)) 
        pygame.display.flip()


class Game (GameWindow):
    """
    Main game loop for EmBall--handles display and all of the game objects 
    needed for the game.
    """
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
            

    def movePaddle (self):
        """Moves the paddle based on the input from the arrow keys"""
        keystate = pygame.key.get_pressed()
        self.paddle.move(keystate[K_RIGHT] - keystate[K_LEFT])        

        
    ###############################
    # Victory/Loss Methods
    ###############################

    def lost(self):
        """Checks for loss conditions  (lives gone)"""
        return self.lives <= 0

    def won (self):
        """Checks for victory conditions  (blocks gone)"""
        return not self.blocks.sprites()

    def gameOver (self):
        """Checks for end game conditions and handles them appropriately"""
        if self.lost():
            self.handleLoss()
            return True
        elif self.won():
            self.handleWin()
            return True
        else:
            return False
        
    def handleLoss(self):
        self.do_gameover(self.messages['loss'])

    def handleWin(self):
        self.do_gameover(self.messages['win'])

    def do_gameover (self, msg):
        """Displays MSG below the rtnToMain message on the screen"""
        self.gameover = True
        self.ball.kill()
        winLossTxt = Text(msg) 
                            
        rtnText = Text(self.messages['rtnToMain']) 
        
        texts = pygame.sprite.Group(rtnText, winLossTxt)

        winLossTxt.positionBelow (rtnText)
        texts.draw(self.screen)
        pygame.display.flip()


####################################################
# Debug methods
####################################################        

    def __str__ (self):
        """
        Returns a string representing the current state of the game--direction of 
        the ball, etc
        """

        return \
"Ball: dir = %(ballD)s, pos = %(ballP)s \n\
Paddle: pos = %(paddleP)s" % \
            {'ballD' : str(self.ball.direction), \
                 'ballP' : str(self.ball.rect.center), \
                 'paddleP' : str(self.paddle.rect.center) \
             }


#################################################
# Screen Drawing Methods
#################################################

    def redrawScreen (self):
        dirty = self.all.draw(self.screen)
        pygame.display.update(dirty)

    def clearScreen (self):
        self.all.clear (self.screen, self.background)


#################################################
# Game loops
#################################################

    def gameLoop(self, *args):
        """Runs the main game"""
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Repost for outer loop to catch
                    pygame.event.post(pygame.event.Event(QUIT))
                    return                
                elif event.type == BALLDROP:
                    self.handleDrop()

                #Ctrl-C
                elif isConsoleEscape (event):
                    import pdb; pdb.set_trace()
#                    self.console()

            if self.gameOver():
                self.endGameLoop()
                return
                                        
            self.clearScreen()

            self.handleCollisions()            
            self.all.update()            
            self.movePaddle()
            self.redrawScreen()       
            self.clock.tick(40)

    def endGameLoop(self):
        """Loop until the user presses a key"""
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



