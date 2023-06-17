from PyQt5.QtWidgets import QWidget, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont
from MouseEvent_func import mousePressEvent_Dragging, mouseMoveEvent_Dragging, mouseReleaseEvent_Dragging
from functools import partial

#MainFrame
class main_frame_QFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, parent.width(), parent.height()))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.setStyleSheet("background-color: #1e1f22;\n")
        self.setObjectName("main_window_frame")


#TitleBarFrame
class title_bar_frame_QFrame(QFrame):
    def __init__(self, window_parent, height, name, icon, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, parent.width(), height))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                          "border-top-left-radius: 0px;\n"
                                          "border-top-right-radius: 0px;\n"
                                          "border-bottom-left-radius: 0px;\n"
                                          "border-bottom-right-radius: 0px;")
        self.setObjectName("title_bar_frame")
        # Добавляем обработку событий мыши для перетаскивания окна
        self.mousePressEvent = partial(mousePressEvent_Dragging, window_parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Dragging, window_parent)
        self.mouseReleaseEvent = partial(mouseReleaseEvent_Dragging, window_parent)

        # Создаем метку с названием приложения
        self.title_name = QLabel(name, self)
        self.title_name.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.title_name.setStyleSheet("color: #D0D0D0;")  # Задаем цвет шрифта (серый)
        self.title_name.setAlignment(Qt.AlignHCenter)  # Выравнивание по горизонтали по центру
        self.title_name.setGeometry(0, 8, self.width(), 35)  # Устанавливаем геометрию метки

        # Создаем QLabel для отображения иконки приложения
        self.app_icon_label = QLabel(self)
        self.app_icon_label.setPixmap(icon.pixmap(30, 30))  # Устанавливаем иконку и масштабируем ее
        self.app_icon_label.setGeometry(2, 2, 30, 30)  # Устанавливаем координаты и размеры QLabel

    def custom_resize(self):
        self.title_name.setGeometry(0, 8, self.width(), 30)  # Устанавливаем геометрию метки



# ToolPanelFrame
class tool_panel_frame_QFrame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, shift_y + 2, parent.width(), 90))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                           "border-top-left-radius: 0px;\n"
                                           "border-top-right-radius: 0px;\n"
                                           "border-bottom-left-radius: 0px;\n"
                                           "border-bottom-right-radius: 0px;")
        self.setObjectName("tool_panel_frame")


# MainFieldFrame
class main_field_frame_QFrame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, (shift_y + 2),
                                          parent.width(), parent.height() - (shift_y + 2)))
        self.setStyleSheet("background-color: #1e1f22;\n")
        self.setObjectName("main_field_frame")