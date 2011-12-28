from EmBallConstants import *

import textwrap
import os

from Blocks import *
import xml.dom.minidom as xml
from Helpers import get_path_for_level


class Level(object):
    """Contains utilities for loading levels (in xml format)"""
    def __init__ (self, lvl_path):
        
        self.name = os.path.basename(lvl_path)
        self.path = lvl_path

        #Set basic background
        self.background = pygame.Surface(SCREENRECT.size)

        #Special case to keep shit running--gone soon
        if self.name == "basic":
            self.get_basic()
            return

        #If lvl file already exists, 
        if os.path.isfile(lvl_path):
            self.parseFile(lvl_path)
            
        else:
            #New level
            self.background.fill((255,255,255))
            self.doc = xml.Document()
            self.blocks = []


    def parseFile (self, lvl_path): 
        self.doc = xml.parse(lvl_path)
        self.blocks = self.get_blocks_from_doc()
        rgb = self.get_background_from_doc()
        self.background.fill(rgb)

    def get_background_from_doc (self):
        rgb_str = d.documentElement.attributes["background"].value
        return tuple((int(x) for x in rgb_str.split(",")))

        
    def get_blocks_from_doc (self):
        """Creates block instances from this level's xml doc"""
        blockElements = self.doc.getElementsByTagName("block")

        blocks = [] 
        for ele in blockElements:
            blockAttrs = elementToDict (ele)
            import pdb; pdb.set_trace()
            blockType = blockAttrs.get('type', "basic")
            blocks.append(get_block(blockType, **blockAttrs))
            
        return blocks
                        
    #Deprecated, soon to kill
    def get_basic(self):
        #Fill in white background
        self.background.fill((255,255,255))

        blocks = []
        i = 0
        for y in range (0, 3*BLOCKSIZE[1], BLOCKSIZE[1]):
            j = i
            for x in range (0, SCREENRECT.right, BLOCKSIZE[0]):
                if j % 2 == 0: color = "blue"
                else:          color = "red"
    
                blockAttrs = {'position' : (x,y),
                              'image_names' : [color],
                              'color' : color
                              }

                blocks.append(get_block('basic', **blockAttrs))
                j += 1
                i += 1
        
        self.blocks = blocks
        
        #Set basic background
        self.background = pygame.Surface(SCREENRECT.size)
        self.background.fill((255,255,255))

    def writeLevel (self, path):
        self.doc.writexml (open(path, 'w'), addindent=" " * 4)

def load_level (level_name):
    #    try:
    level_path = get_path_for_level(level_name)
    return Level(level_path)
        
    #except Exception as e:
     #   raise LevelLoadingException (e.message, level_name)

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
######################################


def elementToDict(element):
    """Extracts the attributes of element and puts them into a dictionary"""
    rtnDict = {}    
    nodeMap = element.attributes

    for i in range (0, nodeMap.length):
        attr = nodeMap.item(i)
        rtnDict[attr.name] = attr.value

    return rtnDict
        
