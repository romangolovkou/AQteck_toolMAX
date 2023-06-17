

def resize_window_width(self, widget, event):
    delta_x = event.globalPos().x() - widget.start_pos_x
    new_width = self.width() + delta_x
    self.resize(new_width, self.height())
    widget.start_pos_x = event.globalPos().x()


def resize_window_height(self, widget, event):
    delta_y = event.globalPos().y() - widget.start_pos_y
    new_heigth = self.height() + delta_y
    self.resize(self.width(), new_heigth)
    widget.start_pos_y = event.globalPos().y()


def resize_and_move_win_width(self, widget, event):
    delta_x = event.globalPos().x() - widget.start_pos_x
    new_width = widget.start_width - delta_x
    new_x = self.x() + delta_x
    self.setGeometry(new_x, self.y(), new_width, self.height())
    widget.start_pos_x = event.globalPos().x()
    widget.start_width = self.width()


def resize_and_move_win_height(self, widget, event):
    delta_y = event.globalPos().y() - widget.start_pos_y
    new_height = widget.start_height - delta_y
    new_y = self.y() + delta_y
    self.setGeometry(self.x(), new_y, self.width(), new_height)
    widget.start_pos_y = event.globalPos().y()
    widget.start_height = self.height()