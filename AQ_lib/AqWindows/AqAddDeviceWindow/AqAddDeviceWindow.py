from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QDialog, QWidget, QCheckBox

from AQ_AddDevicesRotatingGears import AQ_RotatingGearsWidget
from AQ_AddDevicesWindow import ConnectDeviceThread
from AqEventManager import AqEventManager


class AqAddDeviceWidget(QDialog):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

        self.selected_devices_list = []
        # self.event_manager = event_manager
        # Рєєструємо обробники подій
        AqEventManager.register_event_handler('Find_device', self.on_find_button_clicked)
        AqEventManager.register_event_handler('Add_device', self.add_selected_devices_to_session)

        # Створюємо віджет з рухомими шестернями
        self.rotating_gears = AQ_RotatingGearsWidget(self.ui.RotatingGearsFrame)

        # Створюємо порожній список для всіх знайдених девайсів
        self.all_finded_devices = []

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


class AqAddDeviceTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
