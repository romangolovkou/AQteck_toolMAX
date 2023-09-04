from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from AQ_left_widget_panel import AQ_left_widget_panel_frame
from AQ_treeViewManager_frame import AQ_treeView_frame
from custom_window_templates import AQ_reduced_main_field_frame


class AQ_main_field_frame(AQ_reduced_main_field_frame):
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
        # Створюємо фрейм з менеджером відображення дерева
        self.tree_view_frame = AQ_treeView_frame(self.event_manager, self)
        self.tree_view_frame.setGeometry(self.left_panel.width() + 1, 0, self.width() - self.left_panel.width() - 1,
                                         self.height())

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
