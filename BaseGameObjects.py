from __future__ import division
import pygame
from pygame.locals import *

#EmBall imports
import Helpers
from Helpers import *
from EmBallConstants import *    
"""Provides base classes for the main game objects, paddles, blocks and
balls. These classes can be subclassed to make specific types of each"""


class GameObject(pygame.sprite.Sprite):
    
    """Tests whether top of sprite is colliding with rect"""
    def topCollision (self, rect):
        for x in range(self.rect.left, self.rect.right, COLLISIONSTEP):
            if rect.collidepoint((x, self.rect.top)):
                return True
#        return rect.collidepoint(self.rect.midbottom)
        return False

    """Tests whether bottom side of sprite is colliding with rect"""
    def bottomCollision (self, rect):
        for x in range(self.rect.left, self.rect.right, COLLISIONSTEP):
            if rect.collidepoint((x, self.rect.bottom)):
                return True
        
        return False
#        return rect.collidepoint(self.rect.midbottom)
    
    """Tests whether left side of sprite is colliding with rect"""
    def leftCollision(self, rect):
        for y in range(self.rect.top, self.rect.bottom, COLLISIONSTEP):
            if rect.collidepoint((self.rect.left, y)):
                return True

        return False
#        rect.collidepoint(self.rect.midleft)
    
    """Tests whether right side of sprite is colliding with rect"""
    def rightCollision(self, rect):
        
        for y in range(self.rect.top, self.rect.bottom, COLLISIONSTEP):
            if rect.collidepoint((self.rect.right, y)):
                return True

        return False

class Ball(GameObject):
    #Class vars
    images = []
    
    def __init__(self):       
        try:
            pygame.sprite.Sprite.__init__(self, self.containers)
        except AttributeError:
            raise InitializationError \
              ("Game object initialized without self.containers being defined")
       
        if Ball.images == []:
            Ball.images.append(Helpers.load_image("ball"))
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = BALLSTART
        self.direction = normalize(BALLDIR)
        self.speed = BALLSPEED
           

    def blockBounce(self,block):
        xDir, yDir = self.direction
        
        if block.leftCollision(self.rect) or block.rightCollision(self.rect):
            xDir = -xDir
        
        if block.topCollision(self.rect) or block.bottomCollision(self.rect):
            yDir = -yDir

        self.direction = xDir, yDir
    """Simulates a reflection off the walls of the game. Collisions are elastic
    """
    def wallbounce(self):

        xDir, yDir = self.direction
        #Bounce off of side walls
        if self.rect.left < SCREENRECT.left \
           or self.rect.right > SCREENRECT.right:
            xDir = -xDir

        #Bounce off of top (there is no bottom
        if self.rect.top < SCREENRECT.top: 
          yDir = -yDir
    
        self.direction = xDir, yDir

    """Get new direction after bounce off of paddle. Direction is determined by
       position the ball hits on the paddle relative to the center.
       
       Args:
           paddle: the paddle
    """
    def paddleBounce(self, paddle):
        xDir,yDir = self.direction
        
        # Vertical collision
        if paddle.topCollision(self.rect) or paddle.bottomCollision(self.rect): 
            yDir = -yDir
            percentOffset =  \
                 (self.rect.centerx - paddle.rect.centerx) / paddle.rect.width

            xDir = percentOffset * PADDLEDEFLECT
            

       # Horizontal Collision
        elif paddle.leftCollision(self.rect) \
                or paddle.rightCollision(self.rect):
            
            xDir = -xDir

           # Normalize x and y
        
        self.direction = normalize((xDir,yDir))
    


    def update (self):
        if self.rect.bottom > SCREENRECT.bottom:
            pygame.event.post(pygame.event.Event(BALLDROP))
            return

        self.wallbounce()
        xDir, yDir = self.direction
        xSpeed, ySpeed = self.speed
        
        self.rect.move_ip(xDir * xSpeed, yDir * ySpeed)
        

class Paddle(GameObject):
    #Needs containers to be defined outside to succeed
    def __init__ (self):
        try:
            pygame.sprite.Sprite.__init__(self, self.containers)
        except AttributeError:
            raise InitializationError \
              ("Game object initialized without self.containers being defined")
        
        self.image = Helpers.load_image("paddle")
        self.rect = self.image.get_rect()
        #Set rect to extend to bottom of screen
#        self.rect.
        self.rect.midbottom = PADDLESTART
        self.speed = PADDLESPEED
        self.atLeftEdge = False
        self.atRightEdge = False

    def move(self, xDir):
        if self.atLeftEdge:
            if xDir == LEFT: return
            else: self.atLeftEdge = False
            
        elif self.atRightEdge:
            if xDir == RIGHT: return
            else: self.atRightEdge = False
            
        else:
            if self.rect.left < SCREENRECT.left:
                self.rect.left = SCREENRECT.left
                self.atLeftEdge = True
            elif self.rect.right > SCREENRECT.right:
                self.rect.right = SCREENRECT.right
                self.atRightEdge = True
            else: 
                self.rect.move_ip(xDir * self.speed,0)


#####################################################

class BaseBlock(GameObject):
    """Color is a string arg describing the color of the brick to use"""
    containers = []

    def __init__ (self, **blockAttrs):
        #try:
        pygame.sprite.Sprite.__init__(self, self.containers)
        #except AttributeError:
         #   raise InitializationError \
          #    ("Game object initialized without self.containers being defined")
        
        image_names = blockAttrs['image_names']
        self.images = [Helpers.load_image(name) for name in image_names]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = blockAttrs['position']
        
    def hit(self):
        self.kill()


######################################

class Text(GameObject):
    def __init__(self, msg, pos=SCREENRECT.center, containers=None, 
                      color=FONTCOLOR, fontsize=DEFAULTFONTSIZE):

        if containers is not None:
            self.containers = containers
        
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, fontsize)
        self.fontsize = fontsize
        self.color = Color(color)
        self.msg = msg
        self.image = self.font.render(msg, False, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        

    # def draw (self, surface, pos):
    #     surface.blit(self.image, pos)
    #     pygame.display.flip()
    
    """Draws the given text on the line below this one onto the surface"""
    def positionBelow (self, txt):
        x, y = self.rect.bottomleft
        txt.rect.topleft = x, y + self.fontsize / 5
    

class Button (Text):
    pass
