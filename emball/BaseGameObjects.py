"""Provides base classes for the main game objects, paddles, blocks and
balls. These classes can be subclassed to make specific types of each"""

from __future__ import division
import pygame
from pygame.locals import *

#EmBall imports
import Helpers
from Helpers import *
from EmBallConstants import *    



class GameObject(pygame.sprite.Sprite):
    """Base object """
    
    containers = None
    def __init__ (self, game_window=None):
        """Initialize a GameObject with the game in which it is contained"""
        self.game_window = game_window
        if self.containers is None:    
            raise InitializationError \
              ("Game object initialized without self.containers being defined")        

        self.rect = None
        pygame.sprite.Sprite.__init__(self, self.containers)
        
    
    def hit (self, other_object):
        """Action to be taken when other_object hits this one"""
        pass
    
    def colliding (self, other_object):
        return self.rect.colliderect(other_object.rect)
    
    #TODO: change these to operate on GameObjects instead of rects
    def topCollision (self, rect):
        """Tests whether top of sprite is colliding with rect"""
        for x in range(self.rect.left, self.rect.right, COLLISIONSTEP):
            if rect.collidepoint((x, self.rect.top)):
                return True

        return False


    def bottomCollision (self, rect):
        """Tests whether bottom side of sprite is colliding with rect"""
        for x in range(self.rect.left, self.rect.right, COLLISIONSTEP):
            if rect.collidepoint((x, self.rect.bottom)):
                return True
        
        return False

    

    def leftCollision(self, rect):
        """Tests whether left side of sprite is colliding with rect"""
        for y in range(self.rect.top, self.rect.bottom, COLLISIONSTEP):
            if rect.collidepoint((self.rect.left, y)):
                return True

        return False

    

    def rightCollision(self, rect):        
        """Tests whether right side of sprite is colliding with rect"""
        for y in range(self.rect.top, self.rect.bottom, COLLISIONSTEP):
            if rect.collidepoint((self.rect.right, y)):
                return True

        return False



class Ball(GameObject):
    #Class vars
    images = []
    
    def __init__(self, game_window=None):       
        GameObject.__init__ (self, game_window)
       
        if Ball.images == []:
            Ball.images.append(Helpers.load_builtin_image("ball"))
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = BALLSTART
        self.direction = normalize(BALLDIR)
        self.speed = BALLSPEED
           

    def blockBounce(self, direction, blocks):
        """Determines the new direction after bouncing off any blocks"""
        hitBlocks = pygame.sprite.spritecollide(self, blocks, False)
            
        if len(hitBlocks) == 0:            
            return direction
    
        block = hitBlocks[0]        
        block.hit(self)        
        xDir, yDir = direction
        
        if block.leftCollision(self.rect) or block.rightCollision(self.rect):
            xDir = -xDir        
        if block.topCollision(self.rect) or block.bottomCollision(self.rect):
            yDir = -yDir

        return xDir, yDir
    
    def wallBounce(self, direction):
        """
        Simulates a reflection off the walls of the game. Collisions are elastic
        """

        xDir, yDir = direction
        #Bounce off of side walls
        if self.rect.left < SCREENRECT.left \
           or self.rect.right > SCREENRECT.right:
            xDir = -xDir

        #Bounce off of top (there is no bottom
        if self.rect.top < SCREENRECT.top: 
          yDir = -yDir
    
        return xDir, yDir

    def paddleBounce(self, direction, paddle):
        """
        Get new direction after bounce off of paddle. Direction is determined by
        position the ball hits on the paddle relative to the center.       
        """
        if not self.colliding (paddle):
            return direction

        paddle.hit(self)
        xDir,yDir = direction
        
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
        return normalize((xDir,yDir))
    
    

    def update (self):
        if self.rect.bottom > SCREENRECT.bottom:
            pygame.event.post(pygame.event.Event(BALLDROP))
            return
                
        self.direction = xDir, yDir = self.handleCollisions()
        xSpeed, ySpeed = self.speed        
        self.rect.move_ip(xDir * xSpeed, yDir * ySpeed)
        

    def handleCollisions(self):        
        direction = self.direction
        direction = self.wallBounce(direction)
        direction = self.paddleBounce(direction, self.game_window.paddle)
        direction = self.blockBounce(direction, self.game_window.blocks)
        
        return direction
        
        
class Paddle (GameObject):

    def __init__ (self, game_window=None):
        """Precondition: Paddle.containers must be defined"""        
        GameObject.__init__(self, game_window=game_window)
        self.image = Helpers.load_builtin_image("paddle")
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

    def hit (self, other_object):
        debugPrint("Hit paddle")
        debugPrint(str(self.game_window) + "\n")


#####################################################

class BaseBlock(GameObject):
    """
    The base class for all block objects in the game. Various attributes are meant
    to be overridden by subclasses to do different, more interesting things.
    """
    containers = []

    def __init__ (self, game_window=None, **blockAttrs):

        GameObject.__init__(self, game_window)
        
        image_names = blockAttrs['image_names']
        self.images = [Helpers.load_builtin_image(name) for name in image_names]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = blockAttrs['pos']
        
    def hit(self, other_object):
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
    

    def positionBelow (self, txt):
        """Draws the given text on the line below this one onto the surface"""
        x, y = self.rect.bottomleft
        txt.rect.topleft = x, y + self.fontsize / 5
    

class Button (Text):
    pass


