from AQ_ResizeFunc import resize_window_width, resize_window_height, resize_and_move_win_width,\
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


def mouseMoveEvent_Dragging(self, event_manager, event_key, event):
    if event.buttons() == Qt.LeftButton and event.y() <= self.height() and self.not_titlebtn_zone:
        if (event.x() >= self.btn_minimize.x() and event.y() <= self.btn_minimize.height()) == False:
            event_manager.emit_event(event_key, event.globalPos() - self.drag_position)

    event.accept()


def mouseReleaseEvent_Dragging(self, event):
    self.not_titlebtn_zone = 0
    event.accept()

def mousePressEvent_WidthR(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()

    event.accept()


def mouseMoveEvent_WidthR(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_width(self.parent(), self, event)

    event.accept()


def mousePressEvent_WidthL(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()
        self.start_width = self.parent().width()

    event.accept()

def mouseMoveEvent_WidthL(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_width(self.parent(), self, event)

    event.accept()


def mousePressEvent_HeigthLow(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_y = event.globalPos().y()

    event.accept()

def mouseMoveEvent_HeigthLow(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_height(self.parent(), self, event)

    event.accept()


def mousePressEvent_HeigthTop(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_y = event.globalPos().y()
        self.start_height = self.parent().height()

    event.accept()


def mouseMoveEvent_HeigthTop(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_height(self.parent(), self, event)

    event.accept()


def mousePressEvent_Diag_TopLeft(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()
        self.start_width = self.parent().width()
        self.start_height = self.parent().height()

    event.accept()


def mouseMoveEvent_Diag_TopLeft(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_and_move_win_width(self.parent(), self, event)
        resize_and_move_win_height(self.parent(), self, event)

    event.accept()


def mousePressEvent_Diag_TopRigth(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()
        self.start_width = self.parent().width()
        self.start_height = self.parent().height()

    event.accept()


def mouseMoveEvent_Diag_TopRigth(self, event):
    if event.buttons() == Qt.LeftButton:
        delta_x = event.globalPos().x() - self.start_pos_x
        delta_y = event.globalPos().y() - self.start_pos_y
        new_width = self.start_width + delta_x
        new_height = self.start_height - delta_y
        # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
        # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
        self.event_manager.emit_event('resize_' + self.window_name, '%', event.globalPos().y(), new_width, new_height)
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()
        self.start_width = self.parent().width()
        self.start_height = self.parent().height()

    event.accept()


def mousePressEvent_Diag_BotLeft(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()
        self.start_width = self.parent().width()
        self.start_height = self.parent().height()

    event.accept()


def mouseMoveEvent_Diag_BotLeft(self, event):
    if event.buttons() == Qt.LeftButton:
        delta_x = event.globalPos().x() - self.start_pos_x
        delta_y = event.globalPos().y() - self.start_pos_y
        new_width = self.start_width - delta_x
        new_height = self.start_height + delta_y
        # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
        # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
        self.event_manager.emit_event('resize_' + self.window_name, event.globalPos().x(), '%', new_width, new_height)
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()
        self.start_width = self.parent().width()
        self.start_height = self.parent().height()

    event.accept()


def mousePressEvent_Diag_BotRigth(self, event):
    if event.button() == Qt.LeftButton:
        self.start_pos_x = event.globalPos().x()
        self.start_pos_y = event.globalPos().y()

    event.accept()

def mouseMoveEvent_Diag_BotRigth(self, event):
    if event.buttons() == Qt.LeftButton:
        resize_window_height(self.parent(), self, event)
        resize_window_width(self.parent(), self, event)

    event.accept()
