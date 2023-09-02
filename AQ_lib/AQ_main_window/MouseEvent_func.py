from Resize_func import resize_window_width, resize_window_height, resize_and_move_win_width,\
    resize_and_move_win_height
from PyQt5.QtCore import Qt


def mousePressEvent_Dragging(self, event):
    if event.button() == Qt.LeftButton and event.y() <= self.height():
        if (event.x() >= self.btn_minimize.x() and event.y() <= self.btn_minimize.height()) == False:
            self.drag_position = event.globalPos() - self.mapToGlobal(self.pos())
            self.not_titlebtn_zone = 1
        else:
            self.not_titlebtn_zone = 0

    event.accept()


def mouseMoveEvent_Dragging(self, event_manager, event):
    if event.buttons() == Qt.LeftButton and event.y() <= self.height() and self.not_titlebtn_zone:
        if (event.x() >= self.btn_minimize.x() and event.y() <= self.btn_minimize.height()) == False:
            event_manager.emit_event('dragging', event.globalPos() - self.drag_position)

    event.accept()


def mouseReleaseEvent_Dragging(self, event):
    self.not_titlebtn_zone = 0
    event.accept()

def mousePressEvent_WidthR(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeWidthR_widget.start_pos_x = event.globalPos().x()

    event.accept()


def mouseMoveEvent_WidthR(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_width(self, self.resizeWidthR_widget, event)

    event.accept()


def mousePressEvent_WidthL(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeWidthL_widget.start_pos_x = event.globalPos().x()
        self.resizeWidthL_widget.start_width = self.width()

    event.accept()

def mouseMoveEvent_WidthL(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_width(self, self.resizeWidthL_widget, event)

    event.accept()


def mousePressEvent_HeigthLow(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeHeigthLow_widget.start_pos_y = event.globalPos().y()

    event.accept()

def mouseMoveEvent_HeigthLow(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_height(self, self.resizeHeigthLow_widget, event)

    event.accept()


def mousePressEvent_HeigthTop(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeHeigthTop_widget.start_pos_y = event.globalPos().y()
        self.resizeHeigthTop_widget.start_height = self.height()

    event.accept()


def mouseMoveEvent_HeigthTop(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_height(self, self.resizeHeigthTop_widget, event)

    event.accept()


def mousePressEvent_Diag_TopLeft(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeDiag_TopLeft_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_TopLeft_widget.start_pos_y = event.globalPos().y()
        self.resizeDiag_TopLeft_widget.start_width = self.width()
        self.resizeDiag_TopLeft_widget.start_height = self.height()

    event.accept()


def mouseMoveEvent_Diag_TopLeft(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_width(self, self.resizeDiag_TopLeft_widget, event)
        resize_and_move_win_height(self, self.resizeDiag_TopLeft_widget, event)

    event.accept()


def mousePressEvent_Diag_TopRigth(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeDiag_TopRigth_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_TopRigth_widget.start_pos_y = event.globalPos().y()
        self.resizeDiag_TopRigth_widget.start_width = self.width()
        self.resizeDiag_TopRigth_widget.start_height = self.height()

    event.accept()


def mouseMoveEvent_Diag_TopRigth(self, event):
    if event.buttons() == Qt.LeftButton:
        delta_x = event.globalPos().x() - self.resizeDiag_TopRigth_widget.start_pos_x
        delta_y = event.globalPos().y() - self.resizeDiag_TopRigth_widget.start_pos_y
        new_width = self.resizeDiag_TopRigth_widget.start_width + delta_x
        new_height = self.resizeDiag_TopRigth_widget.start_height - delta_y
        self.setGeometry(self.x(), event.globalPos().y(), new_width, new_height)
        self.resizeDiag_TopRigth_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_TopRigth_widget.start_pos_y = event.globalPos().y()
        self.resizeDiag_TopRigth_widget.start_width = self.width()
        self.resizeDiag_TopRigth_widget.start_height = self.height()

    event.accept()


def mousePressEvent_Diag_BotLeft(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeDiag_BotLeft_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_BotLeft_widget.start_pos_y = event.globalPos().y()
        self.resizeDiag_BotLeft_widget.start_width = self.width()
        self.resizeDiag_BotLeft_widget.start_height = self.height()

    event.accept()


def mouseMoveEvent_Diag_BotLeft(self, event):
    if event.buttons() == Qt.LeftButton:
        delta_x = event.globalPos().x() - self.resizeDiag_BotLeft_widget.start_pos_x
        delta_y = event.globalPos().y() - self.resizeDiag_BotLeft_widget.start_pos_y
        new_width = self.resizeDiag_BotLeft_widget.start_width - delta_x
        new_height = self.resizeDiag_BotLeft_widget.start_height + delta_y
        self.setGeometry(event.globalPos().x(), self.y(), new_width, new_height)
        self.resizeDiag_BotLeft_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_BotLeft_widget.start_pos_y = event.globalPos().y()
        self.resizeDiag_BotLeft_widget.start_width = self.width()
        self.resizeDiag_BotLeft_widget.start_height = self.height()

    event.accept()


def mousePressEvent_Diag_BotRigth(self, event):
    if event.button() == Qt.LeftButton:
        self.resizeDiag_BotRigth_widget.start_pos_x = event.globalPos().x()
        self.resizeDiag_BotRigth_widget.start_pos_y = event.globalPos().y()

    event.accept()

def mouseMoveEvent_Diag_BotRigth(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_height(self, self.resizeDiag_BotRigth_widget, event)
        resize_window_width(self, self.resizeDiag_BotRigth_widget, event)

    event.accept()