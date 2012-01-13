"""Contains class definitions for the different types of blocks in the game.
For the definition of BaseBlock, the interface for all block types, see
BaseGameObjects.py"""

from BaseGameObjects import BaseBlock

class Basic(BaseBlock):
    
    def __init__ (self, game_window=None, **blockAttrs):
        blockAttrs['image_names'] = [blockAttrs['color']]
        BaseBlock.__init__ (self, game_window=game_window, **blockAttrs)

class UnbreakableBlock (BaseBlock):
    
    def __init__ (self, game_window=None, **blockAttrs):
        BaseBlock.__init__ (self, game_window=game_window, **blockAttrs)



########################
#Helpers
########################
blockTypes = {'unbreakable' : UnbreakableBlock, 
              'basic' : Basic
              }

   
def get_block(blockType, **blockAttrs):
    if blockType in blockTypes:
        #Instantiate an instance of that block type
        return blockTypes[blockType] (**blockAttrs)

    else:
        raise ValueError("Bad block type: %s" % blockType)
