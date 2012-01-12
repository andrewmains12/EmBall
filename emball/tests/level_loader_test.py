import sys
sys.path.append("..")
import unittest

from EmBall import Helpers

from EmBall.level import Level, elementToDict, safe_decode_json

from MonkeyPatches import HelperPatch

import xml.dom.minidom as xml

class LevelTest (unittest.TestCase):
    """Test to make sure we can initialize levels properly"""

    TEST_LVL = """<?xml version='1.0' encoding='UTF-8'?>
                    <level lives="4" background="[255,255,255]">
                      <block color="blue" pos="[1,1]"/>
                      <block color="red"  pos="[2,2]"/>   
                    </level>
               """

    def setUp (self):
        """
        Setup to initialize the level with our test xml. This xml would normally
        be read from a file, but we mock that aspect here with our string.
        """        
        #Monkey patch image loading 
        Helpers.load_image = HelperPatch.load_image
        self.level = Level()
        self.level.doc = xml.parseString (self.TEST_LVL)
        self.block_attrs = [elementToDict (ele) 
                            for ele in self.level.doc.getElementsByTagName ("block")]
        
    def test_get_blocks_from_doc (self):        
        blocks = self.level.get_blocks_from_doc()
        
        #Test positions
        for block, test_attrs in zip(blocks, self.block_attrs):
            self.assertEqual (list(block.rect.topleft), safe_decode_json(test_attrs["pos"]))
        

    
if __name__ == "__main__":
    unittest.main()
    
