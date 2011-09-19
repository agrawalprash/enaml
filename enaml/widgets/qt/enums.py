#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
""" Translations between Enaml enums and Qt enums
"""

from .qt import QtCore

from ...enums import DataRole, Orientation


QtOrientation = {
    Orientation.HORIZONTAL: QtCore.Qt.Orientation.Horizontal,
    Orientation.VERTICAL: QtCore.Qt.Orientation.Vertical
}

EnamlOrientation = dict((value, key) for key, value in QtOrientation.items())

QtDataRole = {
    DataRole.DISPLAY: QtCore.Qt.DisplayRole,
    DataRole.DECORATION: QtCore.Qt.DecorationRole,
    DataRole.EDIT: QtCore.Qt.EditRole,
    DataRole.TOOL_TIP: QtCore.Qt.ToolTipRole,
    DataRole.STATUS_TIP: QtCore.Qt.StatusTipRole,
    DataRole.WHATS_THIS: QtCore.Qt.WhatsThisRole,
    DataRole.FONT: QtCore.Qt.FontRole,
    DataRole.TEXT_ALIGNMENT: QtCore.Qt.TextAlignmentRole,
    DataRole.BACKGROUND: QtCore.Qt.BackgroundRole,
    DataRole.FOREGROUND: QtCore.Qt.ForegroundRole,
    DataRole.CHECK_STATE: QtCore.Qt.CheckStateRole,
    DataRole.SIZE_HINT: QtCore.Qt.SizeHintRole,
    DataRole.USER: QtCore.Qt.UserRole,
}

EnamlDataRole = dict((value, key) for key, value in QtDataRole.items())

