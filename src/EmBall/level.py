from EmBallConstants import *

import textwrap
import os

from Blocks import *

import xml.dom.minidom as xml
import json

from Helpers import get_path_for_level, load_image


class Level(object):
    """
    Represents an EmBall level.        
    """

    def __init__ (self, lvl_path=None):
        """Initialize a new level"""        
        if not lvl_path:
            self.doc = xml.Document()
            self.name = "Untitled"
            self.blocks = []
            self.background = pygame.Surface(SCREENRECT.size)
            self.background.fill((255,255,255))
        else:
            self.name = os.path.basename(lvl_path)
            self.path = lvl_path

            #Special case to keep shit running--gone soon
            if self.name == "basic":
                self.get_basic()
                
            else:
                self.parseFile(lvl_path)        



    @classmethod
    def new_level (cls):
        """Return a blank level with a default background""" 
        
        
    def parseFile (self, lvl_path): 
        self.doc = xml.parse(lvl_path)
        
        self.blocks = self.get_blocks_from_doc()
        self.background = self.get_background_from_doc()
        

    def get_background_from_doc (self):
        """
        Returns the background image for the level.  If a background
        image is specified (by the "img" attribute on the background
        node), returns a surface of this image, otherwise returns a
        surface filled with the color specified by background.color
        """
        background_ele = find_child (self.doc, "background")
        
        if background_ele.hasAttribute ("img"):
            img_path = background_ele.attributes["img"].value
            return load_image(img_path)            
        else:
            rgb_str = background_ele.attributes["color"].value
            rgb_val = tuple((int(x) for x in rgb_str.split(",")))
            background = pygame.Surface(SCREENRECT.size)
            background.fill (rgb_val)

            return background
        
    def get_blocks_from_doc (self):
        """Creates block instances from this level's xml doc"""
        blockElements = self.doc.getElementsByTagName("block")

        blocks = [] 
        for ele in blockElements:
            blockAttrs = elementToDict (ele)
            blockAttrs = dict(((safe_decode_json(key), safe_decode_json(val))
                               for key, val in blockAttrs.items()))
            blockType = blockAttrs.get('type', "basic")
            blocks.append(get_block(blockType, **blockAttrs))
            
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
    
                blockAttrs = {'pos' : (x,y),
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
    return Level(lvl_path=level_path)
        
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


        
def find_child (element, child_name):
    """Finds the immediate child of ELEMENT with CHILD_NAME"""
    for child in element.childNodes:
        if child.localName == child_name:
            return child
    return None

    
def safe_decode_json (item_string):
    """Decodes item_string if it's valid json; else returns item_string
    """    
    try:
        return json.loads(item_string)
    except ValueError:
        return item_string
