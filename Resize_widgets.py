from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from functools import partial
from MouseEvent_func import mousePressEvent_WidthR, mouseMoveEvent_WidthR, \
                            mousePressEvent_WidthL, mouseMoveEvent_WidthL, \
                            mousePressEvent_HeigthLow, mouseMoveEvent_HeigthLow, \
                            mousePressEvent_HeigthTop, mouseMoveEvent_HeigthTop, \
                            mousePressEvent_Diag_TopLeft, mouseMoveEvent_Diag_TopLeft, \
                            mousePressEvent_Diag_TopRigth, mouseMoveEvent_Diag_TopRigth, \
                            mousePressEvent_Diag_BotLeft, mouseMoveEvent_Diag_BotLeft, \
                            mousePressEvent_Diag_BotRigth, mouseMoveEvent_Diag_BotRigth, \
                            mousePressEvent_Dragging, mouseMoveEvent_Dragging, mouseReleaseEvent_Dragging

class resizeWidthR_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины окна R
        self.setGeometry(
            QRect(parent.width() - parent.resizeLineWidth, parent.resizeLineWidth,
                  parent.resizeLineWidth, parent.height() - (parent.resizeLineWidth * 2)))
        self.setObjectName("resizeWidthR_widget")
        self.setCursor(Qt.SizeHorCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_WidthR, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_WidthR, parent)

class resizeWidthL_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины окна L
        self.setGeometry(
            QRect(0, parent.resizeLineWidth, parent.resizeLineWidth,
                  parent.height() - (parent.resizeLineWidth * 2)))
        self.setObjectName("resizeWidthL_widget")
        self.setCursor(Qt.SizeHorCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_WidthL, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_WidthL, parent)


class resizeHeigthLow_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения высоты окна
        self.setGeometry(
            QRect(parent.resizeLineWidth, parent.height() - parent.resizeLineWidth,
                  parent.width() - (parent.resizeLineWidth * 2), parent.resizeLineWidth))
        self.setObjectName("resizeHeigthLow_widget")
        self.setCursor(Qt.SizeVerCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_HeigthLow, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_HeigthLow, parent)


class resizeHeigthTop_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения высоты окна
        self.setGeometry(
            QRect(parent.resizeLineWidth, 0,
                  parent.width() - (parent.resizeLineWidth * 2), parent.resizeLineWidth))
        self.setObjectName("resizeHeigthTop_widget")
        self.setCursor(Qt.SizeVerCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_HeigthTop, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_HeigthTop, parent)


class resizeDiag_BotRigth_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины и высоты окна (прав. нижний угол)
        self.setGeometry(
            QRect(parent.width() - parent.resizeLineWidth, parent.height() - parent.resizeLineWidth,
                  parent.resizeLineWidth, parent.resizeLineWidth))
        self.setObjectName("resizeDiag_BotRigth_widget")
        self.setCursor(Qt.SizeFDiagCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_Diag_BotRigth, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Diag_BotRigth, parent)


class resizeDiag_BotLeft_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины и высоты окна (лев. нижний угол)
        self.setGeometry(
            QRect(0, parent.height() - parent.resizeLineWidth,
                  parent.resizeLineWidth, parent.resizeLineWidth))
        self.setObjectName("resizeDiag_BotLeft_widget")
        self.setCursor(Qt.SizeBDiagCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_Diag_BotLeft, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Diag_BotLeft, parent)


class resizeDiag_TopLeft_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины и высоты окна (лев. верх. угол)
        self.setGeometry(QRect(0, 0, parent.resizeLineWidth, parent.resizeLineWidth))
        self.setObjectName("resizeDiag_TopLeft_widget")
        self.setCursor(Qt.SizeFDiagCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_Diag_TopLeft, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Diag_TopLeft, parent)


class resizeDiag_TopRigth_Qwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем виджет для изменения ширины и высоты окна (прав. верх. угол)
        self.setGeometry(
            QRect(parent.width() - parent.resizeLineWidth, 0, parent.resizeLineWidth, parent.resizeLineWidth))
        self.setObjectName("resizeDiag_TopRigth_widget")
        self.setCursor(Qt.SizeBDiagCursor)  # Устанавливаем курсор
        self.setStyleSheet("background-color: transparent;\n")
        self.mousePressEvent = partial(mousePressEvent_Diag_TopRigth, parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Diag_TopRigth, parent)