from PySide6.QtCore import QRect, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from AQ_LeftWidgetPanel import AQ_left_widget_panel_frame
from AQ_TreeViewManagerFrame import AQ_TreeViewFrame
from AQ_CustomWindowTemplates import AQ_ReducedMainFieldFrame, AQ_have_error_widget


class AQ_MainFieldFrame(AQ_ReducedMainFieldFrame):
    def __init__(self, event_manager, shift_y, parent=None):
        super().__init__(shift_y, parent)
        self.event_manager = event_manager
        self.event_manager.register_event_handler('set_active_device', self.show_hide_main_pic)
        self.event_manager.register_event_handler('no_devices', self.show_hide_main_pic)
        self.event_manager.register_event_handler('param_read_error', self.show_read_error_label)
        self.event_manager.register_event_handler('param_write_error', self.show_write_error_label)
        self.event_manager.register_event_handler('load_cfg_error', self.show_load_cfg_error_label)
        self.event_manager.register_event_handler('parsing_cfg_error', self.show_parsing_cfg_error_label)

        self.setGeometry(QRect(0, (shift_y + 2), parent.width(), parent.height() - (shift_y + 2)))

        # Создаем заставочную картинку для главного поля
        self.background_pic = QPixmap('Icons/industrial_pic.png')
        self.main_background_pic = QLabel(self)
        self.main_background_pic.setPixmap(self.background_pic)
        self.main_background_pic.setScaledContents(True)
        self.main_background_pic.setGeometry(0, 0, 450, 326)
        self.main_background_pic.hide()

        # Створюємо бокову панель зліва з віджетами доданих девайсів
        self.left_panel = AQ_left_widget_panel_frame(self.event_manager, self)
        self.left_panel.setGeometry(0, 0, 248, self.height())
        # Створюємо фрейм з менеджером відображення дерева
        self.tree_view_frame = AQ_TreeViewFrame(self.event_manager, self)
        self.tree_view_frame.setGeometry(self.left_panel.width() + 1, 0, self.width() - self.left_panel.width() - 1,
                                         self.height())

    def show_hide_main_pic(self, device=None):
        # if device is None:
        #     self.main_background_pic.show()
        # else:
        self.main_background_pic.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Получаем размеры картинки
        pic_size = self.main_background_pic.size()
        # Вычисляем координаты верхнего левого угла картинки
        x = (self.width() - pic_size.width()) // 2
        y = (self.height() - pic_size.height()) // 2
        # Устанавливаем положение картинки
        self.main_background_pic.move(x, y)

        self.left_panel.resize(self.left_panel.width(), self.height())
        self.tree_view_frame.resize(self.width() - self.left_panel.width() - 1, self.height())

        event.accept()

    def show_read_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.read_err_widget = AQ_have_error_widget("<html>Failed to read value.<br>One or more parameters<br>\
                                                        can't be read<html>", self.parent)
        self.read_err_widget.move(self.width() // 2 - self.read_err_widget.width() // 2,
                                  self.height() // 3 - self.read_err_widget.height() // 2)
        self.read_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.read_err_widget.deleteLater)

    def show_write_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.write_err_widget = AQ_have_error_widget("<html>Failed to write value.<br>One or more parameters<br>\
                                                        can't be write<html>", self.parent)
        self.write_err_widget.move(self.width() // 2 - self.write_err_widget.width() // 2,
                                   self.height() // 3 - self.write_err_widget.height() // 2)
        self.write_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.write_err_widget.deleteLater)

    def show_load_cfg_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.load_cfg_err_widget = AQ_have_error_widget("<html>Can`t load configuration.<br>You try load configuration<br>\
                                                        from another device.<html>", self.parent)
        self.load_cfg_err_widget.move(self.width() // 2 - self.load_cfg_err_widget.width() // 2,
                                  self.height() // 3 - self.load_cfg_err_widget.height() // 2)
        self.load_cfg_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.load_cfg_err_widget.deleteLater)

    def show_parsing_cfg_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.parsing_cfg_err_widget = AQ_have_error_widget("<html>Can`t load configuration.<br>The file is damaged<html>",
                                                        self.parent)
        self.parsing_cfg_err_widget.move(self.width() // 2 - self.parsing_cfg_err_widget.width() // 2,
                                      self.height() // 3 - self.parsing_cfg_err_widget.height() // 2)
        self.parsing_cfg_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.parsing_cfg_err_widget.deleteLater)
