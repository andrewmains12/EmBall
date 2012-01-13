import os

from emball import Helpers
from emball.Helpers import *

from emball.GameWindow import MainGame
from optparse import OptionParser

#File hack to let the helper functions know where everything is
Helpers.set_dirs_relative(os.path.dirname(__file__))

def initParser ():
    usage = "usage: ./Emball.py [options] [level_name]"
    parser = OptionParser(usage)
    parser.set_defaults(debug=False, logFile=getLogName())
    parser.add_option ("-d", action="store_true", dest="debug",\
                     help = "Causes program to be run in debug mode")
    parser.add_option ("-l", action="store", dest="logFile",\
                     help = "Causes debug messages to be logged")
    
    return parser
   


def main():    
    #Do option parsing
    parser = initParser()
    options, args = parser.parse_args()
    
    #Set helper constants
    Helpers.DEBUG = options.debug
    Helpers.LOG_FILE = options.logFile

    if len(args) != 0: 
        level = args[0]

    else: 
        level = "basic"
                      
    MainGame(level).gameLoop()    
    pygame.quit()



if __name__ == "__main__":
    main()
