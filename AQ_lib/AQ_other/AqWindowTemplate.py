from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog

from AQ_EventManager import AQ_EventManager
from AQ_ResizeWidgets import *
from ui_AqWindowTemplate import Ui_AqWindowTemplate

class AqWindowTemplate(QWidget):
    def __init__(self, widget: QWidget, parent=None):
        super().__init__(parent)
        self._window_name = ''
        self.ui = Ui_AqWindowTemplate()
        self.ui.setupUi(self)
        self.ui.mainWidget = widget
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

    @property
    def name(self):
        return self._window_name

    @name.setter
    def name(self, name):
        self._window_name = name
        self.ui.headertext = name


class AqDialogTemplate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._window_name = ''
        self.ui_title = Ui_AqWindowTemplate()
        self.ui_title.setupUi(self)
        self._dragging_enable = False
        self.dragging_enable = True
        self._resizeFrameEnable = False
        self._resizeFrameWidth = 5
        self.maximizedIcon = "UI/icons/feather/copy.svg"
        self.normalIcon = "UI/icons/feather/square.svg"
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.clickPosition = None  # Initialize clickPosition attribute
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui_title, "closeBtn").clicked.connect(lambda: self.close())
        getattr(self.ui_title, "maximizeBtn").clicked.connect(lambda: self.restore_or_maximize_window())

    @property
    def name(self):
        return self._window_name

    @name.setter
    def name(self, name):
        self._window_name = name
        self.ui_title.headertext.setText(name)

    @property
    def content_widget(self):
        return self.ui_title.mainWidget

    @property
    def dragging_enable(self):
        return self._dragging_enable

    @dragging_enable.setter
    def dragging_enable(self, value: bool):
        self._dragging_enable = value
        if hasattr(self.ui_title, 'headertext'):
            getattr(self.ui_title, 'headertext').mouseMoveEvent = self.moveWindow

    @property
    def resizeFrameEnable(self):
        return self._resizeFrameEnable

    @resizeFrameEnable.setter
    def resizeFrameEnable(self, state_n_width: list):
        if state_n_width[0] is True and self._resizeFrameEnable is False:
            self._resizeFrameWidth = state_n_width[1]
            self.create_resize_frame(self._resizeFrameWidth)

        self._resizeFrameEnable = state_n_width[0]

    def create_resize_frame(self, resizeFrameWidth):
        self.event_manager.register_event_handler('resize_' + self.objectName(), self.resize_MainWindow)
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

        self.resizeWidthR_widget = resizeWidthR_Qwidget(self.event_manager, self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self.event_manager, self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self.event_manager, self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self.event_manager, self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self.event_manager, self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self.event_manager, self)

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
                self.ui_title.maximizeBtn.setIcon(QtGui.QIcon(str(self.maximizedIcon)))
        else:
            # Change Icon
            if len(str(self.normalIcon)) > 0:
                self.ui_title.maximizeBtn.setIcon(QtGui.QIcon(str(self.normalIcon)))


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
