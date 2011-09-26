#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from ..common import push_button


class TestQtPushButton(push_button.TestPushButton):
    """ QtPushButton tests. """
    
    def button_pressed(self):
        """ Press the button programmatically.
        
        """
        self.widget.pressed.emit()
    
    def button_released(self):
        """ Release the button programmatically.
        
        """
        self.widget.released.emit()

    def button_clicked(self):
        """ Click the button programmatically.
        
        """
        self.widget.clicked.emit()
        
