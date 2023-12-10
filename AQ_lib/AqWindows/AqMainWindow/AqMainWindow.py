from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from AQ_MainWindowFrame import AQ_MainWindowFrame
from AQ_Session import AQ_CurrentSession
from AQ_EventManager import AQ_EventManager
from AppCore import Core
from ui_form import Ui_MainWindow


class AqMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

        Core.init()

        # # Менеджер подій
        # Core.event_manager.register_event_handler('close_' + self.objectName(), self.close)
        # Core.event_manager.register_event_handler('minimize_' + main_name, self.showMinimized)
        # Core.event_manager.register_event_handler('maximize_' + main_name, self.showMaximized)
        # Core.event_manager.register_event_handler('normalize_' + main_name, self.showNormal)
        # Core.event_manager.register_event_handler('dragging_' + main_name, self.move)
        # Core.event_manager.register_event_handler('resize_' + main_name, self.resize_MainWindow)
        #
        # #MainWindowFrame
        # self.main_window_frame = AQ_MainWindowFrame(Core.event_manager, main_name, self.AQicon, self)

    # def prepare_ui_objects(self):
        # Прив'язуємо кнопки до слотів
        # self.ui.findBtn.clicked.connect(lambda: self.event_manager.emit_event("open_AddDevices"))
        # self.ui.addBtn.clicked.connect(self.add_selected_devices_to_session)

    # def resize_MainWindow(self, pos_x, pos_y, width, height):
    #     if pos_x == '%':
    #         pos_x = self.pos().x()
    #     if pos_y == '%':
    #         pos_y = self.pos().y()
    #     if width == '%':
    #         width = self.width()
    #     if height == '%':
    #         height = self.height()
    #
    #     self.setGeometry(pos_x, pos_y, width, height)
    #
    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
    #     self.main_window_frame.resize(self.width(), self.height())
    #     event.accept()
