from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QCheckBox

from AQ_AddDevicesConnectErrorLabel import AQ_ConnectErrorLabel
from AQ_AddDevicesAddButton import AQ_addButton
from AQ_AddDevicesRotatingGears import AQ_RotatingGearsWidget
from AQ_AddDevicesTableWidget import AQ_addDevice_TableWidget
from AQ_CustomWindowTemplates import AQ_SimplifiedDialog, AQ_ComboBox, AQ_Label
from AQ_AddDevicesNetworkFrame import AQ_network_settings_frame
from AQ_Device import AQ_Device


class AQ_DialogParamList(AQ_SimplifiedDialog):
    def __init__(self, event_manager, parent):
        window_name = 'Parameter list'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_parameter_list")
        self.parent = parent
        self.event_manager = event_manager
        # self.selected_devices_list = []
        self.setGeometry(0, 0, 800, 900)
        self.main_window_frame.setGeometry(1, 0, self.width() - 2,
                                           self.height() - 1)
        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Рєєструємо обробники подій
        # self.event_manager.register_event_handler('Find_device', self.on_find_button_clicked)
        # self.event_manager.register_event_handler('AddDevice_connect_error', self.show_connect_err_label)
        # self.event_manager.register_event_handler('Add_device', self.add_selected_devices_to_session)
        self.event_manager.register_event_handler('minimize_' + window_name, self.showMinimized)
        self.event_manager.register_event_handler('close_' + window_name, self.close)
        self.event_manager.register_event_handler('dragging_' + window_name, self.move)

        # Створюємо фрейм з налаштуваннями з'єднання
        # self.network_settings_frame = AQ_network_settings_frame(event_manager, self.main_window_frame)
        # self.network_settings_frame.setGeometry(25, self.title_bar_frame.height() + 2, int(self.width() * 0.4),
        #                                         self.height() - self.title_bar_frame.height() - 4)

        # # Создаем QTableWidget с 4 столбцами
        # self.table_widget = AQ_addDevice_TableWidget(self.main_window_frame)
        # self.table_widget.move(self.network_settings_frame.width() + 50, self.title_bar_frame.height() + 5)

        # # Створюємо віджет з рухомими шестернями
        # self.rotating_gears = AQ_RotatingGearsWidget(self.main_window_frame)
        # self.rotating_gears.move(610, 500)
        #
        # # Створюємо порожній список для всіх знайдених девайсів
        # self.all_finded_devices = []





