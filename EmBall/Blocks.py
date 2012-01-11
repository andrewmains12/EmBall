"""Contains class definitions for the different types of blocks in the game.
For the definition of BaseBlock, the interface for all block types, see
BaseGameObjects.py"""

from game.BaseGameObjects import BaseBlock
from game.Helpers import IMG_FILES

class Basic(BaseBlock):
    
    def __init__ (self, **blockAttrs):
        blockAttrs['image_names'] = [blockAttrs['color']]
        BaseBlock.__init__ (self, **blockAttrs)

class UnbreakableBlock (BaseBlock):
    
    def __init__ (self, **blockAttrs):
        BaseBlock.__init__ (self, **blockAttrs)



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
        raise InitializationError("Bad block type: %s" % blockType)
