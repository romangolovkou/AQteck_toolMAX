from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QCheckBox

from AQ_addDevice_ConnectErrorLabel import AQ_ConnectErrorLabel
from AQ_addDevices_addButton import AQ_addButton
from AQ_addDevice_RotatingGears import AQ_RotatingGearsWidget
from AQ_addDevice_TableWidget import AQ_addDevice_TableWidget
from custom_window_templates import AQDialog, AQComboBox, AQLabel
from AQ_AddDevices_network_frame import AQ_network_settings_frame
from AQ_Device import AQ_Device


class AQ_DialogAddDevices(AQDialog):
    def __init__(self, event_manager, devices_list, parent):
        super().__init__('Add Devices')

        self.setObjectName("AQ_Dialog_add_device")
        self.parent = parent
        self.event_manager = event_manager
        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('Find_device', self.on_find_button_clicked)
        self.event_manager.register_event_handler('AddDevice_connect_error', self.show_connect_err_label)
        self.event_manager.register_event_handler('Add_device', self.add_selected_devices_to_session)

        # Створюємо фрейм з налаштуваннями з'єднання
        self.network_settings_frame = AQ_network_settings_frame(event_manager, self.main_window_frame)
        self.network_settings_frame.setGeometry(25, self.title_bar_frame.height() + 2, int(self.width() * 0.4),
                                                self.height() - self.title_bar_frame.height() - 4)

        # Создаем QTableWidget с 4 столбцами
        self.table_widget = AQ_addDevice_TableWidget(self.main_window_frame)
        self.table_widget.move(self.network_settings_frame.width() + 50, self.title_bar_frame.height() + 5)

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
        devices_count = self.table_widget.rowCount()
        for i in range(devices_count):
            checkbox_item = self.table_widget.cellWidget(i, 0)
            if checkbox_item is not None and isinstance(checkbox_item, QCheckBox):
                if checkbox_item.checkState() == Qt.Checked:
                    item = self.table_widget.item(i, 2)
                    dev_address = item.text()
                    for j in range(len(self.parent.ready_to_add_devices)):
                        ready_device_data = self.parent.ready_to_add_devices[j]
                        if dev_address == ready_device_data.get('address', ''):
                            self.parent.devices.append(self.parent.ready_to_add_devices[j])
                            # Видаляємо зі списку ready доданий девайс
                            self.parent.ready_to_add_devices.pop(j)
                            self.parent.add_tree_view()
                            break
                else:
                    print("Галочка не установлена")


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

    def connect_to_device (self):
        finded_devices_list = []
        network_settings_list = self.network_settings_frame.get_network_settings_list()
        for i in range(len(network_settings_list)):
            device = AQ_Device(self.event_manager, network_settings_list[i])
            device_status = device.get_device_status()
            if device_status == 'ok' or device_status == 'data_error':
                finded_devices_list.append(device)

        return finded_devices_list

    def show_connect_err_label(self):
        self.connect_err_label = AQ_ConnectErrorLabel(self.width(), 50, self.main_window_frame)
        self.connect_err_label.move(0, self.height() - 50)
        self.connect_err_label.show()

class ConnectDeviceThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result_signal = pyqtSignal(object)  # Сигнал для передачи данных в главное окно
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



