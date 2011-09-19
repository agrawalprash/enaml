#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import Instance, implements
from traitsui.ui import UI

from .qt_control import QtControl

from ..traitsui_item import ITraitsUIItemImpl


class QtTraitsUIItem(QtControl):
    """ A Qt implementation of TraitsUIItem.

    The traits ui item allows the embedding of a traits ui window in 
    an Enaml application.

    See Also
    --------
    TraitsUIItem

    """
    implements(ITraitsUIItemImpl)
    
    #---------------------------------------------------------------------------
    # ITraitsUIItemImpl interface
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying traits ui subpanel.

        """
        parent = self.parent
        model = parent.model
        view = parent.view
        handler = parent.handler
        parent_widget = self.parent_widget()
        self.ui = ui = model.edit_traits(parent=parent_widget, view=view,
                                         handler=handler, kind='subpanel')
        self.widget = ui.control
    
    def initialize_widget(self):
        """ No initialization needs to be done for the traits ui item.

        """
        pass
        
    #---------------------------------------------------------------------------
    # Implementation
    #---------------------------------------------------------------------------
    ui = Instance(UI)

