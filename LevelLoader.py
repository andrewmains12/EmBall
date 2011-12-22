from EmBallConstants import *
import EmBall
import textwrap
from Blocks import *
import xml.dom.minidom as xml
import Helpers
"""Contains utilities for loading levels (in xml format)"""

class Level:

    def __init__ (self, lvlName):
        
        self.name = lvlName
        if lvlName == "basic":
            self.get_basic()
        
        else:
            self.doc = xml.parse(Helpers.get_path_for_level(lvlName))
            self.blocks = self.get_blocks()



    def get_blocks(self):
        blockElements = self.doc.getElementsByTagName("block")

        blocks = [] 
        for ele in blockElements:
            blockAttrs = elementToDict(ele)
            blockType = blockAttrs['type']
            blocks.append(get_block((blockType, blockAttrs)))
            
        return blocks
                        
    #Deprecated, soon to kill
    def get_basic(self):
        blocks = []
        i = 0
        for y in range (0, 3*BLOCKSIZE[1], BLOCKSIZE[1]):
            j = i
            for x in range (0, SCREENRECT.right, BLOCKSIZE[0]):
                if j % 2 == 0: color = "blue"
                else:          color = "red"
    
                blockAttrs = {'position' : (x,y),
                               'image_names' : [color]
                              }

                blocks.append(get_block('basic', **blockAttrs))
                j += 1
                i += 1
        
        self.blocks = blocks
        
        #Set basic background
        self.background = pygame.Surface(SCREENRECT.size)
        self.background.fill((255,255,255))


def load_level (level_name):
    try:
        return Level(level_name)
        
    except Exception as e:
        raise LevelLoadingException (e.msg, level_name)

class LevelLoadingException(Exception):
    def __init__ (self, msg, level_name):
        
        error_string = textwrap.dedent( 
            """
            Problem loading level %s, original error was:
            %s   
            """ % (level_name, msg))

        super(LevelLoadingException, self).__init__(error_string)
        self.level_name = level_name
######################################
# xml Helpers
"""Extracts the attributes of element and puts them into a dictionary"""
def elementToDict(element):
    rtnDict = {}
    
    nodeMap = element.attributes

    for i in range (0, nodeMap.length):
        attr = nodeMap.item(i)
        rtnDict[attr.name] = attr.value

    return rtnDict
        
