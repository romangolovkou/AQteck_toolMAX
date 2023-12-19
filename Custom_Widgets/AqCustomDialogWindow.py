
########################################################################
## IMPORTS
########################################################################
import os
import __main__

from AQ_ResizeWidgets import *
from AppCore import Core
########################################################################
## COMPILE SASS
########################################################################
from .Qss import SassCompiler
CompileStyleSheet = SassCompiler.CompileStyleSheet
# from .Qss.SvgToPngIcons import NewIconsGenerator

from .QCustomQPushButtonGroup import QCustomQPushButtonGroup


########################################################################
## IMPORT PYSIDE2 OR PYSIDE6
########################################################################
# if 'PySide2' in sys.modules:
#     from PySide2 import QtWidgets, QtGui, QtCore
#     from PySide2.QtCore import *
#     from PySide2.QtGui import *
#     from PySide2.QtWidgets import *
#     from PySide2.QtCore import Signal

# elif 'PySide6' in sys.modules:
#     from PySide6 import QtWidgets, QtGui, QtCore
#     from PySide6.QtCore import *
#     from PySide6.QtGui import *
#     from PySide6.QtWidgets import *
#     from PySide6.QtCore import Signal

########################################################################
## MODULE UPDATED TO USE QT.PY
########################################################################
from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import Signal


# JSON FOR READING THE JSON STYLESHEET
import json

from . QCustomQPushButton import applyAnimationThemeStyle, applyButtonShadow, iconify, applyCustomAnimationThemeStyle, applyStylesFromColor

class QDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.clickPosition = None  # Initialize clickPosition attribute

    #######################################################################
    # Add mouse events to the window
    #######################################################################
    def create_resize_frame(self, resizeFrameWidth):
        Core.event_manager.register_event_handler('resize_' + self.objectName(), self.resize_MainWindow)
        # # Создаем виджеты для изменения размеров окна
        if resizeFrameWidth is not None and resizeFrameWidth and isinstance(resizeFrameWidth, int):
            if resizeFrameWidth < 2 or resizeFrameWidth > 15:
                print(self.objectName() + 'Error: "resizeFrameWidth" must below 2 to 15. Current value = '\
                      + str(resizeFrameWidth))
                if resizeFrameWidth < 2:
                    resizeFrameWidth = 2
                else:
                    resizeFrameWidth = 15
                print('Value changed! "resizeFrameWidth" = ' + str(resizeFrameWidth))
            self.resizeLineWidth = resizeFrameWidth
        else:
            print('resizeFrameWidth is "None" or not "int"')
            print('Was setted default resizeFrameWidth = 5')
            self.resizeLineWidth = 5

        self.resizeWidthR_widget = resizeWidthR_Qwidget(Core.event_manager, self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(Core.event_manager, self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(Core.event_manager, self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(Core.event_manager, self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(Core.event_manager, self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(Core.event_manager, self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(Core.event_manager, self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(Core.event_manager, self)

    def resize_MainWindow(self, pos_x, pos_y, width, height):
        if pos_x == '%':
            pos_x = self.pos().x()
        if pos_y == '%':
            pos_y = self.pos().y()
        if width == '%':
            width = self.width()
        if height == '%':
            height = self.height()

        self.setGeometry(pos_x, pos_y, width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, 'resizeFrameEnable'):
            if self.resizeFrameEnable is True:
                self.resizeWidthR_widget.setGeometry(self.width() - self.resizeLineWidth,
                                                     self.resizeLineWidth, self.resizeLineWidth,
                                                     self.height() - (self.resizeLineWidth * 2))
                self.resizeWidthL_widget.setGeometry(0, self.resizeLineWidth, self.resizeLineWidth,
                                                     self.height() - (self.resizeLineWidth * 2))
                self.resizeHeigthLow_widget.setGeometry(self.resizeLineWidth, self.height() - self.resizeLineWidth,
                                                        self.width() - (self.resizeLineWidth * 2),
                                                        self.resizeLineWidth)
                self.resizeHeigthTop_widget.setGeometry(self.resizeLineWidth, 0,
                                                        self.width() - (self.resizeLineWidth * 2),
                                                        self.resizeLineWidth)
                self.resizeDiag_BotRigth_widget.move(self.width() - self.resizeLineWidth,
                                                     self.height() - self.resizeLineWidth)
                self.resizeDiag_TopLeft_widget.move(0, 0)
                self.resizeDiag_TopRigth_widget.move(self.width() - self.resizeLineWidth, 0)
                self.resizeDiag_BotLeft_widget.move(0, self.height() - self.resizeLineWidth)

        event.accept()

    #######################################################################
    # Add mouse events to the window
    #######################################################################
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # Hide floating widgets
        cursor = QtGui.QCursor()
        xPos = cursor.pos().x()
        yPos = cursor.pos().y()
        if hasattr(self, "floatingWidgets"):
            for x in self.floatingWidgets:
                if hasattr(x, "autoHide") and x.autoHide:
                    x.collapseMenu()


    #######################################################################
    #######################################################################

    #######################################################################
    # Update restore button icon on maximizing or minimizing window
    #######################################################################
    def updateRestoreButtonIcon(self):
        # If window is maxmized
        if self.isMaximized():
            # Change Iconload
            if len(str(self.maximizedIcon)) > 0:
                self.restoreBtn.setIcon(QtGui.QIcon(str(self.maximizedIcon)))
        else:
            # Change Icon
            if len(str(self.normalIcon)) > 0:
                self.restoreBtn.setIcon(QtGui.QIcon(str(self.normalIcon)))


    def restore_or_maximize_window(self):
        # If window is maxmized
        if self.isMaximized():
            self.showNormal()
            if hasattr(self, "floatingWidgets"):
                for x in self.floatingWidgets:
                    x.paintEvent(None)

        else:
            self.showMaximized()

        print("Window minimum size ", self.minimumSize().width(), "x", self.minimumSize().height())
        self.updateRestoreButtonIcon()

     # ###############################################
    # Function to Move window on mouse drag event on the tittle bar
    # ###############################################
    def moveWindow(self, e):
        # Detect if the window is  normal size
        # ###############################################
        if not self.isMaximized(): #Not maximized
            # Move window only when window is normal size
            # ###############################################
            #if left mouse button is clicked (Only accept left mouse button clicks)
            if e.buttons() == Qt.LeftButton:
                #Move window
                if self.clickPosition is not None:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        else:
            self.showNormal()

    def toggleWindowSize(self, e):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    ########################################################################
    ## Check Button Groups
    ########################################################################
    def checkButtonGroup(self):
        btn = self.sender()
        group = btn.group
        groupBtns = getattr(self, "group_btns_"+str(group))
        active = getattr(self, "group_active_"+str(group))
        notActive = getattr(self, "group_not_active_"+str(group))

        for x in groupBtns:
            if not x == btn:
                x.setStyleSheet(notActive)
                x.active = False

        btn.setStyleSheet(active)
        btn.active = True

    def compileSassTheme(self, progress_callback):
        ########################################################################
        ## GENERATE NEW ICONS FOR CURRENT THEME
        NewIconsGenerator.generateNewIcons(self, progress_callback)

    def makeAllIcons(self, progress_callback):
        ########################################################################
        ## GENERATE ALL ICONS FOR ALL THEMES
        NewIconsGenerator.generateNewIcons(self, progress_callback)

    def sassCompilationProgress(self, n):
        pass
        # self.ui.activityProgress.setValue(n)

    def restart(self):
        try:
            # Restart
            # os.execl(sys.executable, str(os.path.abspath(__main__.__file__)), *sys.argv)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Your app theme has been successfuly generated. Please restart your app to fully apply your new theme")
            msg.setInformativeText("Show more details...")
            msg.setWindowTitle("Finished generating app theme!")
            msg.setDetailedText("The app needs to be restarted in order to apply the new Icons")
            msg.setStandardButtons(QMessageBox.Ok)

            retval = msg.exec_()

        except Exception as e:
            raise Exception("Failed to restart the app, please close and open the app again.")

    #######################################################################
