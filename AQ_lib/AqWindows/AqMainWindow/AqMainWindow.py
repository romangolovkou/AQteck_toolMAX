import AqUiWorker
from AQ_ResizeWidgets import *
from Custom_Widgets import QMainWindow, loadJsonStyle
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

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.deviceInfoBtn.clicked.connect(AqUiWorker.show_device_info_window)
        self.ui.paramListBtn.clicked.connect(AqUiWorker.show_device_param_list)
        self.ui.watchListBtn.clicked.connect(AqUiWorker.show_watch_list_window)

        self.ui.readParamMenuBtn.clicked.connect(Core.session.read_params_cur_active_device)
        self.ui.writeParamMenuBtn.clicked.connect(Core.session.write_params_cur_active_device)
