from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow
from AQ_MainWindowFrame import AQ_MainWindowFrame
from AQ_Session import AQ_CurrentSession
from AQ_EventManager import AQ_EventManager
# Defines
PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'


class AQ_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_name = 'AQteckModules'
        PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'
        self.AQicon = QIcon('Icons/AQico_silver.png')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(main_name)
        self.setWindowIcon(self.AQicon)
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(300, 400)
        self.resizeLineWidth = 4
        self.spacing_between_frame = 2
        self.not_titlebtn_zone = 0

        # Менеджер подій
        self.event_manager = AQ_EventManager()
        self.event_manager.register_event_handler('close_' + main_name, self.close)
        self.event_manager.register_event_handler('minimize_' + main_name, self.showMinimized)
        self.event_manager.register_event_handler('maximize_' + main_name, self.showMaximized)
        self.event_manager.register_event_handler('normalize_' + main_name, self.showNormal)
        self.event_manager.register_event_handler('dragging_' + main_name, self.move)
        self.event_manager.register_event_handler('resize_' + main_name, self.resize_MainWindow)
        # Поточна сессія
        self.current_session = AQ_CurrentSession(self.event_manager, self)

        #MainWindowFrame
        self.main_window_frame = AQ_MainWindowFrame(self.event_manager, main_name, self.AQicon, self)

    def resize_MainWindow(self, pos_x, pos_y, width, height):
        if pos_x == '%':
            pos_x = self.pos().x()
        if pos_y == '%':
            pos_y = self.pos().y()
        if width == '%':
            width = self.width()
        if height == '%':
            height = self.height()

        self.setGeometry(pos_x, pos_y, width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.main_window_frame.resize(self.width(), self.height())
        event.accept()
