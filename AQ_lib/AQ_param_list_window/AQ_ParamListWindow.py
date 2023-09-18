from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QStandardItem
from PyQt5.QtWidgets import QApplication, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout, QTableView

from AQ_AddDevicesConnectErrorLabel import AQ_ConnectErrorLabel
from AQ_AddDevicesAddButton import AQ_addButton
from AQ_AddDevicesRotatingGears import AQ_RotatingGearsWidget
from AQ_AddDevicesTableWidget import AQ_addDevice_TableWidget
from AQ_CustomWindowTemplates import AQ_SimplifiedDialog, AQ_ComboBox, AQ_Label
from AQ_AddDevicesNetworkFrame import AQ_NetworkSettingsFrame
from AQ_Device import AQ_Device
from AQ_ParamListManagerFrame import AQ_ParamListManagerFrame
from AQ_TableViewItemModel import AQ_TableViewItemModel
from AQ_TreeViewItemModel import AQ_TreeViewItemModel


class AQ_DialogParamList(AQ_SimplifiedDialog):
    def __init__(self, device, event_manager, parent):
        window_name = 'Parameter list'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_parameter_list")
        self.parent = parent
        self.event_manager = event_manager
        self.device = device
        self.setGeometry(0, 0, 900, 800)
        self.main_window_frame.setGeometry(1, 0, self.width() - 2,
                                           self.height() - 1)
        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('minimize_' + window_name, self.showMinimized)
        self.event_manager.register_event_handler('close_' + window_name, self.close)
        self.event_manager.register_event_handler('dragging_' + window_name, self.move)

        #Створюємо головний фрейм
        self.param_list_manager_frame = AQ_ParamListManagerFrame(self.device, self.event_manager, self)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())
        self.param_list_manager_frame.setGeometry(0, self.title_bar_frame.height(), self.width(),
                                                  self.height() - self.title_bar_frame.height())
        event.accept()






