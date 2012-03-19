#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import warnings

from wpyf.api import Label
from .wpf_control import WPFControl

from ...components.label import AbstractTkLabel


class WPFLabel(WPFControl, AbstractTkLabel):
    """ A WPF implementation of Label.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying WPF Label control.

        """
        self.widget = Label()
        self.add_to_parent(parent)

    def initialize(self):
        """ Initializes the attributes on the underlying control.

        """
        super(WPFLabel, self).initialize()
        shell = self.shell_obj
        self.set_label(shell.text)
        self.set_word_wrap(shell.word_wrap)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_text_changed(self, text):
        """ The change handler for the 'text' attribute.

        """
        self.set_label(text)

    def shell_word_wrap_changed(self, word_wrap):
        """ The change handler for the 'word_wrap' attribute.

        """
        self.set_word_wrap(word_wrap)

    def set_label(self, label):
        """ Sets the label on the underlying control.

        """
        self.widget.Content = unicode(self.shell_obj.text)

    def set_word_wrap(self, wrap):
        """ Sets the word wrapping on the underlying widget.

        """
        warnings.warn("'wrap' option is not yet supported in the wpf backend")
