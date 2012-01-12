
import Helpers
from Helpers import *

from GameWindow import MainGame
from optparse import OptionParser

def initParser ():
    usage = "usage: ./Emball.py [options] [level_name]"
    parser = OptionParser()
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
