import unittest
from emball.Helpers import InitializationError
from pygame.locals import *

from emball.GameWindow import GameWindow

class MockGameWindow (GameWindow):
    """Class to test event handler autodiscovery"""
    
    def __init__(self):
        #Initialize self.event_handlers and nothing else, since we don't need 
        #screens and such
        self.event_handlers = {}
        
        
    def on_mousebuttondown(self, event, **kwargs):
        pass

class EventHandlerTest(unittest.TestCase):
    
    def setUp (self):
        self.game_window = MockGameWindow()

    def test_add_event_handlers (self):
        """Test that events are properly registered by addEventHandlers"""
        
        def handler(event, **kwargs):
            pass 

        self.game_window.addEventHandlers ((QUIT, handler))
        
        self.assertEqual(self.game_window.event_handlers[QUIT], handler)
        
    def test_auto_discover_handlers (self):
        """Test that on_mousebuttondown was successfully discovered and registered"""
        self.game_window.auto_discover_handlers()
        self.assertEqual(self.game_window.event_handlers[MOUSEBUTTONDOWN],
                         self.game_window.on_mousebuttondown)

    def test_auto_discover_handlers_error (self):
        """Check for an appropriate exception when auto-registering a bad event
        """
        def on_foobar (self, event, **kwargs):
            pass
        self.game_window.on_foobar = on_foobar        
        self.assertRaises (InitializationError, self.game_window.auto_discover_handlers)

    

