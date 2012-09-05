#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .qt.QtGui import QAction, QKeySequence
from .qt_messenger_widget import QtMessengerWidget


class QtAction(QtMessengerWidget):
    """ A Qt implementation of an Enaml Action.

    """
    # FIXME Currently, the checked state of the action is lost when 
    # switching from checkable to non-checkable and back again.
    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create_widget(self, parent, tree):
        """ Create the underlying QAction object.

        """
        return QAction(parent)

    def create(self, tree):
        """ Create and initialize the underlying control.

        """
        super(QtAction, self).create(tree)
        self.set_text(tree['text'])
        self.set_tool_tip(tree['tool_tip'])
        self.set_status_tip(tree['status_tip'])
        self.set_checkable(tree['checkable'])
        self.set_checked(tree['checked'])
        self.set_enabled(tree['enabled'])
        self.set_visible(tree['visible'])
        self.set_separator(tree['separator'])
        widget = self.widget()
        widget.triggered.connect(self.on_triggered)
        widget.toggled.connect(self.on_toggled)

    #--------------------------------------------------------------------------
    # Signal Handlers
    #--------------------------------------------------------------------------
    def on_triggered(self):
        """ The signal handler for the 'triggered' signal.

        """
        content = {'checked': self.widget().isChecked()}
        self.send_action('triggered', content)

    def on_toggled(self):
        """ The signal handler for the 'toggled' signal.

        """
        if 'checked' not in self.loopback_guard:
            content = {'checked': self.widget().isChecked()}
            self.send_action('toggled', content)

    #--------------------------------------------------------------------------
    # Message Handling
    #--------------------------------------------------------------------------
    def on_action_set_text(self, content):
        """ Handle the 'set_text' action from the Enaml widget.

        """
        self.set_text(content['text'])

    def on_action_set_tool_tip(self, content):
        """ Handle the 'set_tool_tip' action from the Enaml widget.

        """
        self.set_tool_tip(content['tool_tip'])

    def on_action_set_status_tip(self, content):
        """ Handle the 'set_status_tip' action from the Enaml widget.

        """
        self.set_status_tip(content['status_tip'])

    def on_action_set_checkable(self, content):
        """ Handle the 'set_checkable' action from the Enaml widget.

        """
        self.set_checkable(content['checkable'])

    def on_action_set_checked(self, content):
        """ Handle the 'set_checked' action from the Enaml widget.

        """
        self.set_checked(content['checked'])

    def on_action_set_enabled(self, content):
        """ Handle the 'set_enabled' action from the Enaml widget.

        """
        self.set_enabled(content['enabled'])

    def on_action_set_visible(self, content):
        """ Handle the 'set_visible' action from the Enaml widget.

        """
        self.set_visible(content['visible'])

    def on_action_set_separator(self, content):
        """ Handle the 'set_separator' action from the Enaml widget.

        """
        self.set_separator(content['separator'])

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_text(self, text):
        """ Set the text on the underlying control.

        """
        widget = self.widget()
        widget.setText(text)
        parts = text.split('\t')
        if len(parts) > 1:
            shortcut = QKeySequence(parts[-1])
            widget.setShortcut(shortcut)

    def set_tool_tip(self, tool_tip):
        """ Set the tool tip on the underlying control.

        """
        self.widget().setToolTip(tool_tip)

    def set_status_tip(self, status_tip):
        """ Set the status tip on the underyling control.

        """
        self.widget().setStatusTip(status_tip)

    def set_checkable(self, checkable):
        """ Set the checkable state on the underlying control.

        """
        self.widget().setCheckable(checkable)

    def set_checked(self, checked):
        """ Set the checked state on the underlying control.

        """
        with self.loopback_guard('checked'):
            self.widget().setChecked(checked)

    def set_enabled(self, enabled):
        """ Set the enabled state on the underlying control.

        """
        self.widget().setEnabled(enabled)

    def set_visible(self, visible):
        """ Set the visible state on the underlying control.

        """
        self.widget().setVisible(visible)

    def set_separator(self, separator):
        """ Set the separator state on the underlying control.

        """
        self.widget().setSeparator(separator)
