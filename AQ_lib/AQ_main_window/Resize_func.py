

def resize_window_width(parent_frame, sender_widget, event):
    delta_x = event.globalPos().x() - sender_widget.start_pos_x
    new_width = parent_frame.width() + delta_x
    # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
    # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
    sender_widget.event_manager.emit_event('resize_main_window', '%', '%', new_width, '%')
    sender_widget.start_pos_x = event.globalPos().x()


def resize_window_height(parent_frame, sender_widget, event):
    delta_y = event.globalPos().y() - sender_widget.start_pos_y
    new_height = parent_frame.height() + delta_y
    # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
    # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
    sender_widget.event_manager.emit_event('resize_main_window', '%', '%', '%', new_height)
    sender_widget.start_pos_y = event.globalPos().y()


def resize_and_move_win_width(parent_frame, sender_widget, event):
    delta_x = event.globalPos().x() - sender_widget.start_pos_x
    new_width = sender_widget.start_width - delta_x
    new_x = parent_frame.mapToGlobal(parent_frame.pos()).x() + delta_x
    # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
    # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
    sender_widget.event_manager.emit_event('resize_main_window', new_x, '%', new_width, '%')
    sender_widget.start_pos_x = event.globalPos().x()
    sender_widget.start_width = parent_frame.width()


def resize_and_move_win_height(parent_frame, sender_widget, event):
    delta_y = event.globalPos().y() - sender_widget.start_pos_y
    new_height = sender_widget.start_height - delta_y
    new_y = parent_frame.mapToGlobal(parent_frame.pos()).y() + delta_y
    # self.setGeometry(self.x(), new_y, self.width(), new_height)
    # Формат передачі агрументів у евент ('resize_main_window', new_pos_x, new_pos_y, new_width, new_height)
    # Строка з символом % - ознака, що цей параметр у розмірі вікна змінювати не потрібно
    sender_widget.event_manager.emit_event('resize_main_window', '%', new_y , '%', new_height)
    sender_widget.start_pos_y = event.globalPos().y()
    sender_widget.start_height = parent_frame.height()
