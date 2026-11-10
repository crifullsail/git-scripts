"""
Pull Windows - Maya utility

Run from the Maya Script Editor (Python tab):

    import sys
    import importlib

    script_folder = r"D:\OneDrive - Full Sail University\CGA-3312\rigging_tools\git-scripts"
    if script_folder not in sys.path:
        sys.path.insert(0, script_folder)

    import dinnerTime
    importlib.reload(dinnerTime)
    dinnerTime.show()

After editing this file, run the commands again to reload the tool.
Use "Pull Windows to This Position" to align visible Maya windows with
this tool window, or "Move Windows to This Screen's Top-Left" to align
them with the top-left corner of the screen containing this tool.
"""

try:
    from PySide6 import QtCore, QtWidgets
    import shiboken6 as shiboken
except ImportError:
    from PySide2 import QtCore, QtWidgets
    import shiboken2 as shiboken

import maya.OpenMayaUI as omui


def _maya_main_window_pointer():
    pointer = omui.MQtUtil.mainWindow()
    if not pointer:
        raise RuntimeError("Could not find Maya's main window.")
    return int(pointer)


def _maya_main_window():
    return shiboken.wrapInstance(
        _maya_main_window_pointer(),
        QtWidgets.QWidget,
    )


class PullWindowsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Pull Windows")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, False)

        layout = QtWidgets.QVBoxLayout(self)
        pull_button = QtWidgets.QPushButton("Pull Windows to This Position")
        pull_button.clicked.connect(self.pull_windows)
        layout.addWidget(pull_button)

        top_left_button = QtWidgets.QPushButton(
            "Move Windows to This Screen's Top-Left"
        )
        top_left_button.clicked.connect(self.move_windows_to_screen_top_left)
        layout.addWidget(top_left_button)

    def pull_windows(self):
        self._move_windows_to(self.frameGeometry().topLeft())

    def move_windows_to_screen_top_left(self):
        screen = self.screen()
        if screen is None:
            raise RuntimeError("Could not determine which screen contains this tool.")
        self._move_windows_to(screen.geometry().topLeft())

    def _move_windows_to(self, target):
        main_window_pointer = _maya_main_window_pointer()
        tool_window_pointer = shiboken.getCppPointer(self)[0]
        app = QtWidgets.QApplication.instance()

        if app is None:
            raise RuntimeError("Could not find Maya's Qt application.")

        for window in app.topLevelWidgets():
            window_pointer = shiboken.getCppPointer(window)[0]
            if (
                window_pointer in (main_window_pointer, tool_window_pointer)
                or not window.isVisible()
            ):
                continue

            delta = target - window.frameGeometry().topLeft()
            window.move(window.pos() + delta)


_tool_window = None


def show():
    global _tool_window

    if _tool_window is None:
        _tool_window = PullWindowsDialog(_maya_main_window())

    _tool_window.show()
    _tool_window.raise_()
    _tool_window.activateWindow()
