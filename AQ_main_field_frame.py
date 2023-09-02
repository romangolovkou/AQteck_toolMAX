from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from AQ_left_widget_panel import AQ_left_widget_panel_frame
from custom_window_templates import main_field_frame_AQFrame


class AQ_main_field_frame(main_field_frame_AQFrame):
    def __init__(self, event_manager, shift_y, parent=None):
        super().__init__(shift_y, parent)
        self.event_manager = event_manager
        self.setGeometry(QRect(0, (shift_y + 2), parent.width(), parent.height() - (shift_y + 2)))

        # Создаем заставочную картинку для главного поля
        self.background_pic = QPixmap('Icons/industrial_pic.png')
        self.main_background_pic = QLabel(self)
        self.main_background_pic.setPixmap(self.background_pic)
        self.main_background_pic.setScaledContents(True)
        self.main_background_pic.setGeometry(0, 0, 450, 326)

        # Створюємо бокову панель зліва з віджетами доданих девайсів
        self.left_panel = AQ_left_widget_panel_frame(self.event_manager, self)
        self.left_panel.setGeometry(0, 0, 248, self.height())
