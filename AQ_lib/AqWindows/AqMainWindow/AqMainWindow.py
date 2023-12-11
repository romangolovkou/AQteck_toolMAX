from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from AQ_MainWindowFrame import AQ_MainWindowFrame
from AQ_Session import AQ_CurrentSession
from AQ_EventManager import AQ_EventManager
from AppCore import Core
from AqLeftWidgetPanel import AqLeftDeviceWidget
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
        self.event_manager.register_event_handler("new_devices_added", self.add_dev_widgets_to_left_panel)
        self.event_manager.register_event_handler("delete_device", self.remove_dev_widget_from_left_panel)
        # Core.event_manager.register_event_handler('close_' + self.objectName(), self.close)
        # Core.event_manager.register_event_handler('minimize_' + main_name, self.showMinimized)
        # Core.event_manager.register_event_handler('maximize_' + main_name, self.showMaximized)
        # Core.event_manager.register_event_handler('normalize_' + main_name, self.showNormal)
        # Core.event_manager.register_event_handler('dragging_' + main_name, self.move)
        # Core.event_manager.register_event_handler('resize_' + main_name, self.resize_MainWindow)
        #
        # #MainWindowFrame
        # self.main_window_frame = AQ_MainWindowFrame(Core.event_manager, main_name, self.AQicon, self)

    def add_dev_widgets_to_left_panel(self, new_devices):
        for device in new_devices:
            dev_widget = AqLeftDeviceWidget(device, self)
            self.ui.left_panel_layout.insertWidget(0, dev_widget)

    def remove_dev_widget_from_left_panel(self, device):
        delete_pos = None
        for i in range(self.ui.left_panel_layout.count()):
            widget = self.ui.left_panel_layout.itemAt(i).widget()
            if widget.device == device:
                self.ui.left_panel_layout.removeWidget(widget)
                widget.deleteLater()
                delete_pos = i
                break

        if delete_pos is not None:
            try:
                widget = self.ui.left_panel_layout.itemAt(delete_pos).widget()
                widget.set_active_cur_widget()
            except:
                try:
                    widget = self.ui.left_panel_layout.itemAt(delete_pos - 1).widget()
                    widget.set_active_cur_widget()
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    print(f"Немає жодного пристрою")


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
