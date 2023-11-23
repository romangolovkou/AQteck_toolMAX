from functools import partial

from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QFrame, QLabel, QPushButton

from AQ_MouseEventFunc import mousePressEvent_Dragging, mouseMoveEvent_Dragging, mouseReleaseEvent_Dragging


class AQ_TitleBarFrame(QFrame):
    def __init__(self, event_manager, height, name, icon, parent=None):
        super().__init__(parent)
        self.name = name
        self.event_manager = event_manager
        self.setGeometry(QRect(0, 0, parent.width(), height))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                          "border-top-left-radius: 0px;\n"
                                          "border-top-right-radius: 0px;\n"
                                          "border-bottom-left-radius: 0px;\n"
                                          "border-bottom-right-radius: 0px;")
        self.setObjectName("title_bar_frame")
        # Добавляем обработку событий мыши для перетаскивания окна
        self.mousePressEvent = partial(mousePressEvent_Dragging, self)
        self.mouseMoveEvent = partial(mouseMoveEvent_Dragging, self, self.event_manager, 'dragging_' + self.name)
        self.mouseReleaseEvent = partial(mouseReleaseEvent_Dragging, self)

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

        # Создаем кнопку закрытия
        self.icoClose = QIcon('Icons/Close.png')

        self.btn_close = QPushButton('', self)
        self.btn_close.setIcon(QIcon(self.icoClose))  # установите свою иконку для кнопки
        self.btn_close.setGeometry(self.width() - 35, 0, 35,
                                   35)  # установите координаты и размеры кнопки
        # добавляем обработчик события нажатия на кнопку закрытия
        self.btn_close.clicked.connect(lambda: self.event_manager.emit_event('close_' + self.name))
        self.btn_close.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        # Создаем кнопку свернуть
        self.icoMinimize = QIcon('Icons/Minimize.png')
        self.btn_minimize = QPushButton('', self)
        self.btn_minimize.setIcon(QIcon(self.icoMinimize))  # установите свою иконку для кнопки
        self.btn_minimize.setGeometry(self.width() - 105, 0, 35,
                                      35)  # установите координаты и размеры кнопки
        self.btn_minimize.clicked.connect(lambda: self.event_manager.emit_event('minimize_' + self.name))
        self.btn_minimize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        # Создаем кнопку развернуть/нормализировать
        self.icoMaximize = QIcon('Icons/Maximize.png')
        self.icoNormalize = QIcon('Icons/_Normalize.png')
        self.isMaximized = False  # Флаг, указывающий на текущее состояние окна
        self.btn_maximize = QPushButton('', self)
        self.btn_maximize.setIcon(QIcon(self.icoMaximize))  # установите свою иконку для кнопки
        self.btn_maximize.setGeometry(self.width() - 70, 0, 35,
                                      35)  # установите координаты и размеры кнопки
        self.btn_maximize.clicked.connect(self.toggleMaximize)
        self.btn_maximize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

    def toggleMaximize(self):
        try:
            if self.isMaximized:
                self.event_manager.emit_event('normalize_' + self.name)
                self.btn_maximize.setIcon(QIcon(self.icoMaximize))
                self.isMaximized = False
            else:
                self.event_manager.emit_event('maximize_' + self.name)
                self.btn_maximize.setIcon(QIcon(self.icoNormalize))
                self.isMaximized = True
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def custom_resize(self):
        self.title_name.setGeometry(0, 8, self.width(), 30)  # Устанавливаем геометрию метки

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_maximize.move(self.width() - 70, 0)
        self.btn_minimize.move(self.width() - 105, 0)
        self.btn_close.move(self.width() - 35, 0)
        self.custom_resize()
        event.accept()
