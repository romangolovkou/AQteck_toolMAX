from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, Signal
from PySide6.QtGui import QScreen, QGuiApplication
from PySide6.QtWidgets import QApplication, QCheckBox

from AQ_AddDevicesConnectErrorLabel import AQ_ConnectErrorLabel
from AQ_AddDevicesAddButton import AQ_addButton
from AQ_AddDevicesRotatingGears import AQ_RotatingGearsWidget
from AQ_AddDevicesTableWidget import AQ_addDevice_TableWidget
from AQ_CustomWindowTemplates import AQ_SimplifiedDialog, AQ_ComboBox, AQ_Label
from AQ_AddDevicesNetworkFrame import AQ_NetworkSettingsFrame
from AQ_Device import AQ_Device
from AQ_Device_110china import AQ_Device110China


class AQ_DialogAddDevices(AQ_SimplifiedDialog):
    def __init__(self, event_manager, parent):
        window_name = 'Add Devices'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_add_device")
        self.parent = parent
        self.event_manager = event_manager
        self.selected_devices_list = []
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() // 2 - self.width() // 2,
                  screen_geometry.height() // 2 - self.height() // 2)

        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('Find_device', self.on_find_button_clicked)
        self.event_manager.register_event_handler('AddDevice_connect_error', self.show_connect_err_label)
        self.event_manager.register_event_handler('Add_device', self.add_selected_devices_to_session)

        # Створюємо фрейм з налаштуваннями з'єднання
        self.network_settings_frame = AQ_NetworkSettingsFrame(event_manager, self.main_window_frame)
        self.network_settings_frame.setGeometry(25, self.main_window_frame.title_bar_frame.height() + 2, int(self.width() * 0.4),
                                                self.height() - self.main_window_frame.title_bar_frame.height() - 4)

        # Создаем QTableWidget с 4 столбцами
        self.table_widget = AQ_addDevice_TableWidget(self.main_window_frame)
        self.table_widget.move(self.network_settings_frame.width() + 50, self.main_window_frame.title_bar_frame.height() + 5)

        # Створюємо віджет з рухомими шестернями
        self.rotating_gears = AQ_RotatingGearsWidget(self.main_window_frame)
        self.rotating_gears.move(610, 500)

        # Створюємо порожній список для всіх знайдених девайсів
        self.all_finded_devices = []

    def add_devices_to_table_widget(self, finded_devices):
        for i in range(len(finded_devices)):
            self.table_widget.append_device_row(finded_devices[i].get_device_data())

        bottom_right_corner_table_widget = self.table_widget.mapTo(self.main_window_frame, self.table_widget.rect().bottomRight())
        summ_rows_height = self.table_widget.get_sum_of_rows_height()

        if hasattr(self, 'add_btn'):
            self.add_btn.move(bottom_right_corner_table_widget.x() - self.add_btn.width() - 3,
                              summ_rows_height + 70)
        else:
            self.add_btn = AQ_addButton(self.event_manager, 'Add device', self.main_window_frame)
            self.add_btn.move(bottom_right_corner_table_widget.x() - self.add_btn.width() - 3,
                              summ_rows_height + 70)

    def add_finded_devices_to_all_list(self, finded_devices):
        for i in range(len(finded_devices)):
            self.all_finded_devices.append(finded_devices[i])

    def add_selected_devices_to_session(self):
        devices_count = len(self.all_finded_devices)
        for i in range(devices_count):
            checkbox_item = self.table_widget.cellWidget(i, 0)
            if checkbox_item is not None and isinstance(checkbox_item, QCheckBox):
                if checkbox_item.checkState() == Qt.Checked:
                    self.selected_devices_list.append(self.all_finded_devices[i])

        self.event_manager.emit_event('add_new_devices', self.selected_devices_list)
        self.all_finded_devices.clear()
        self.selected_devices_list.clear()
        self.close()

    def on_find_button_clicked(self):
        self.rotating_gears.start()
        # Запускаем функцию connect_to_device в отдельном потоке
        self.connect_thread = ConnectDeviceThread(self)
        self.connect_thread.finished.connect(self.on_connect_thread_finished)
        self.connect_thread.error.connect(self.on_connect_thread_error)
        self.connect_thread.result_signal.connect(self.connect_finished)
        self.connect_thread.start()

    def on_connect_thread_finished(self):
        self.rotating_gears.stop()

    def on_connect_thread_error(self, error_message):
        # Выполняется в случае ошибки при выполнении connect_to_device
        # В этом слоте можно выполнить действия, которые должны произойти в случае ошибки
        self.show_connect_err_label()
        self.rotating_gears.stop()

    def connect_finished(self, finded_devices):
        self.add_devices_to_table_widget(finded_devices)
        self.add_finded_devices_to_all_list(finded_devices)

    def connect_to_device(self):
        finded_devices_list = []
        network_settings_list = self.network_settings_frame.get_network_settings_list()
        for i in range(len(network_settings_list)):
            device = self.get_device_by_settings(self.event_manager, network_settings_list[i])
            device_status = device.get_device_status()
            if device_status == 'ok' or device_status == 'data_error':
                finded_devices_list.append(device)
            else:
                self.show_connect_err_label()

        return finded_devices_list

    def get_device_by_settings(self, event_manager, network_settings):
        if len(network_settings) > 2:
            device = AQ_Device110China(event_manager, network_settings)
        else:
            device = AQ_Device(event_manager, network_settings)

        return device

    def show_connect_err_label(self):
        self.connect_err_label = AQ_ConnectErrorLabel(self.width(), 50, self.main_window_frame)
        self.connect_err_label.move(0, self.height() - 50)
        self.connect_err_label.show()

class ConnectDeviceThread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            result_data = self.parent.connect_to_device()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))



