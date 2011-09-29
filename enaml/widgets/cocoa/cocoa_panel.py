from Foundation import NSMakeRect
from AppKit import NSView, NSViewWidthSizable, NSViewHeightSizable


from traits.api import implements

from .cocoa_component import CocoaComponent

from ..panel import IPanelImpl


class CocoaPanel(CocoaComponent):
    """ A Cocoa implementation of Panel.

    A panel arranges its children onto a QFrame.

    See Also
    --------
    Panel

    """
    implements(IPanelImpl)

    #---------------------------------------------------------------------------
    # IPanelImpl interface
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying wxPanel.

        """
        self.widget = NSView.alloc().init()
        #self.widget.setFrame_(NSMakeRect(0,0,200,200))
    
    def initialize_widget(self):
        """ There is nothing to initialize on a panel.

        """
        pass
        self.widget.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)

    def create_style_handler(self):
        """ Creates and sets the window style handler.

        """
        pass
    
    def initialize_style(self):
        """ Initializes the style for the window.

        """
        pass
    
    def layout_child_widgets(self):
        """ Arrange the child widgets onto the panel. The children are
        all Containers which provide their own layout. Typically, there
        will be only one container, but in case there are more, all 
        containers get added to a vertical box sizer.

        """
        layout = NSView.alloc().init()
        #layout.setFrame_(NSMakeRect(0,0,200,200))
        layout.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        for child in self.child_widgets():
            layout.addSubview_(child)
        self.widget.addSubview_(layout)
