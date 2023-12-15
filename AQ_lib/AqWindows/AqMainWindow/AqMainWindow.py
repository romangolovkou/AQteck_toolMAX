import AqUiWorker
from AQ_ResizeWidgets import *
from Custom_Widgets import loadJsonStyle, QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
# from PySide6.QtWidgets import QMainWindow
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

        loadJsonStyle(self, self.ui)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.deviceInfoBtn.clicked.connect(AqUiWorker.show_device_info_window)
        self.ui.paramListBtn.clicked.connect(AqUiWorker.show_device_param_list)

        Core.init()

        self.ui.readParamMenuBtn.clicked.connect(Core.session.read_params_cur_active_device)
        self.ui.writeParamMenuBtn.clicked.connect(Core.session.write_params_cur_active_device)

        self.create_resize_frame()
        # # Менеджер подій
        # self.event_manager.register_event_handler("new_devices_added", self.add_dev_widgets_to_left_panel)
        # self.event_manager.register_event_handler("delete_device", self.remove_dev_widget_from_left_panel)
        # Core.event_manager.register_event_handler('close_' + self.objectName(), self.close)
        # Core.event_manager.register_event_handler('minimize_' + main_name, self.showMinimized)
        # Core.event_manager.register_event_handler('maximize_' + main_name, self.showMaximized)
        # Core.event_manager.register_event_handler('normalize_' + main_name, self.showNormal)
        # Core.event_manager.register_event_handler('dragging_' + main_name, self.move)

        #
        # #MainWindowFrame
        # self.main_window_frame = AQ_MainWindowFrame(Core.event_manager, main_name, self.AQicon, self)

    def create_resize_frame(self):
        Core.event_manager.register_event_handler('resize_' + self.objectName(), self.resize_MainWindow)
        # # Создаем виджеты для изменения размеров окна
        self.resizeLineWidth = 4
        self.resizeWidthR_widget = resizeWidthR_Qwidget(self.event_manager, self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self.event_manager, self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self.event_manager, self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self.event_manager, self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self.event_manager, self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self.event_manager, self)

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

        self.resizeWidthR_widget.setGeometry(self.width() - self.resizeLineWidth,
                                             self.resizeLineWidth, self.resizeLineWidth,
                                             self.height() - (self.resizeLineWidth * 2))
        self.resizeWidthL_widget.setGeometry(0, self.resizeLineWidth, self.resizeLineWidth,
                                             self.height() - (self.resizeLineWidth * 2))
        self.resizeHeigthLow_widget.setGeometry(self.resizeLineWidth, self.height() - self.resizeLineWidth,
                                                self.width() - (self.resizeLineWidth * 2),
                                                self.resizeLineWidth)
        self.resizeHeigthTop_widget.setGeometry(self.resizeLineWidth, 0,
                                                self.width() - (self.resizeLineWidth * 2),
                                                self.resizeLineWidth)
        self.resizeDiag_BotRigth_widget.move(self.width() - self.resizeLineWidth,
                                             self.height() - self.resizeLineWidth)
        self.resizeDiag_TopLeft_widget.move(0, 0)
        self.resizeDiag_TopRigth_widget.move(self.width() - self.resizeLineWidth, 0)
        self.resizeDiag_BotLeft_widget.move(0, self.height() - self.resizeLineWidth)

        event.accept()

    # def add_dev_widgets_to_left_panel(self, new_devices):
    #     for device in new_devices:
    #         dev_widget = AqLeftDeviceWidget(device, self)
    #         self.ui.left_panel_layout.insertWidget(0, dev_widget)
    #
    # def remove_dev_widget_from_left_panel(self, device):
    #     delete_pos = None
    #     for i in range(self.ui.left_panel_layout.count()):
    #         widget = self.ui.left_panel_layout.itemAt(i).widget()
    #         if widget.device == device:
    #             self.ui.left_panel_layout.removeWidget(widget)
    #             widget.deleteLater()
    #             delete_pos = i
    #             break
    #
    #     if delete_pos is not None:
    #         try:
    #             widget = self.ui.left_panel_layout.itemAt(delete_pos).widget()
    #             widget.set_active_cur_widget()
    #         except:
    #             try:
    #                 widget = self.ui.left_panel_layout.itemAt(delete_pos - 1).widget()
    #                 widget.set_active_cur_widget()
    #             except Exception as e:
    #                 print(f"Error occurred: {str(e)}")
    #                 print(f"Немає жодного пристрою")


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
