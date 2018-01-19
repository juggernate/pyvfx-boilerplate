"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform

import maya.cmds as cmds

sys.dont_write_bytecode = True  # Avoid writing .pyc files

MAYA = True

# Window title and object names
WINDOW_TITLE = 'Boilerplate'
WINDOW_OBJECT = 'boilerPlate'
DOCK_WITH_MAYA_UI = True

# Repository path, e.g. REPO_PATH = '/Users/fredrik/code/repos/pyvfx-boilerplate/'
REPO_PATH = os.path.dirname(__file__)

# Palette filepath
PALETTE_FILEPATH = os.path.join(REPO_PATH, 'boilerdata', 'qpalette_maya2016.json')

# Full path to where .ui files are stored
UI_PATH = os.path.join(REPO_PATH, 'boilerdata')

from boilerlib.Qt import QtWidgets  # pylint: disable=E0611
from boilerlib.Qt import QtCore  # pylint: disable=E0611
from boilerlib.Qt import QtCompat

# from boilerlib import mayapalette

# Debug
# print('Using' + QtCompat.__binding__)

class Boilerplate(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and built-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None):
        super(Boilerplate, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        if MAYA:
            # Makes Maya perform magic which makes the window stay
            # on top in OS X and Linux. As an added bonus, it'll
            # make Maya remember the window position
            self.setProperty("saveWindowPref", True)

        self.counter = 0

        # Filepaths
        main_window_file = os.path.join(UI_PATH, 'main_window.ui')
        module_file = os.path.join(UI_PATH, 'module.ui')

        # Load UIs
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI
        self.module_widget = QtCompat.load_ui(module_file)  # Module UI

        # Attach module to main window UI's boilerVerticalLayout layout
        self.main_widget.boilerVerticalLayout.addWidget(self.module_widget)

        # Edit widget which resides in module UI
        self.module_widget.boilerLabel.setText('Push the button!')

        # Edit widget which resides in main window UI
        self.main_widget.boilerPushButton.setText('Push me!')

        # Set the main widget
        self.setCentralWidget(self.main_widget)

        # Define minimum size of UI
        self.setMinimumSize(200, 200)

        # Signals
        # The "pushButton" widget resides in the main window UI
        self.main_widget.boilerPushButton.clicked.connect(self.say_hello)

    def say_hello(self):
        """Set the label text.
        The "label" widget resides in the module
        """
        self.counter += 1
        self.module_widget.boilerLabel.setText('{}x Hello world!'.format(self.counter))


def _maya_delete_ui():
    """Delete existing UI in Maya"""
    if cmds.window(WINDOW_OBJECT, q=True, exists=True):
        cmds.deleteUI(WINDOW_OBJECT)  # Delete window
    if cmds.dockControl('MayaWindow|' + WINDOW_TITLE, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + WINDOW_TITLE)  # Delete docked window


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


def run_maya():
    """Run in Maya"""
    _maya_delete_ui()  # Delete any existing existing UI
    boil = Boilerplate(parent=_maya_main_window())

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    boil.setProperty("saveWindowPref", True)

    if not DOCK_WITH_MAYA_UI:
        boil.show()  # Show the UI
    elif DOCK_WITH_MAYA_UI:
        allowed_areas = ['right', 'left']
        cmds.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left',
                         content=WINDOW_OBJECT, allowedArea=allowed_areas)


if __name__ == "__main__":
    run_maya()
