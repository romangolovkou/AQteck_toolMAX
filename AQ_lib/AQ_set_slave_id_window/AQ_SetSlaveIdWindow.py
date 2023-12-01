from PySide6.QtCore import QTimer
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtWidgets import QWidget, QFrame, QLabel

from AQ_AddDevicesConnectErrorLabel import AQ_ConnectErrorLabel
from AQ_CustomWindowTemplates import AQ_SimplifiedDialog
from AQ_SetSlaveIdNetworkFrame import AQ_SetSlaveIdNetworkSettingsFrame


class AQ_DialogSetSlaveId(AQ_SimplifiedDialog):
    def __init__(self, event_manager, parent):
        window_name = 'Set slave id'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_set_slave_id")
        self.parent = parent
        self.event_manager = event_manager
        self.selected_devices_list = []
        self.resize(550, 600)
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() // 2 - self.width() // 2,
                  screen_geometry.height() // 2 - self.height() // 2)

        # Рєєструємо обробники подій
        # self.event_manager.register_event_handler('set_slave_id', self.on_find_button_clicked)
        # self.event_manager.register_event_handler('AddDevice_connect_error', self.show_connect_err_label)
        # self.event_manager.register_event_handler('Add_device', self.add_selected_devices_to_session)
        self.event_manager.register_event_handler('set_slave_id_connect_error', self.show_connect_err_label)
        self.event_manager.register_event_handler('set_slave_id_connect_ok', self.show_success_write_label)

        # Створюємо фрейм з налаштуваннями з'єднання
        self.network_settings_frame = AQ_SetSlaveIdNetworkSettingsFrame(event_manager, self.main_window_frame)
        self.network_settings_frame.setGeometry(25, self.main_window_frame.title_bar_frame.height() + 2,
                                                self.width() - 50,
                                                self.height() - self.main_window_frame.title_bar_frame.height() - 4)
    # TODO: Make this function normally
    # def get_device_by_settings(self, event_manager, network_settings):
    #     if network_settings[2] == 'МВ110-24_1ТД.csv':
    #         device = AQ_DeviceDY500(event_manager, network_settings)
    #     elif len(network_settings) > 2:
    #         device = AQ_Device110China(event_manager, network_settings)
    #     else:
    #         device = AQ_Device(event_manager, network_settings)
    #
    #     return device

    def show_connect_err_label(self):
        self.connect_err_label = AQ_ConnectErrorLabel(self.width(), 50, self.main_window_frame)
        self.connect_err_label.move(0, self.height() - 50)
        self.connect_err_label.show()

    def show_success_write_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.success_label_widget = AQ_success_label_widget("<html>Succesfully<br>Response: OK<b<html>", self)
        self.success_label_widget.move(self.width() // 2 - self.success_label_widget.width() // 2,
                                   self.height() // 3 - self.success_label_widget.height() // 2)
        self.success_label_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.success_label_widget.deleteLater)

class AQ_success_label_widget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 230, 50)
        self.frame.setStyleSheet("border: 2px solid #429061; border-radius: 5px; background-color: #1e1f22")
        self.text_label = QLabel(text, self)
        self.text_label.setFont(QFont("Segoe UI", 12))
        self.text_label.move(10, 5)
        self.text_label.setStyleSheet("border: none; color: #E0E0E0; background-color: transparent")
        self.show()


# class ConnectDeviceThread(QThread):
#     finished = Signal()
#     error = Signal(str)
#     result_signal = Signal(object)  # Сигнал для передачи данных в главное окно
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#
#     def run(self):
#         try:
#             result_data = self.parent.connect_to_device()
#             self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
#             # По завершении успешного выполнения
#             self.finished.emit()
#         except Exception as e:
#             # В случае ошибки передаем текст ошибки обратно в главный поток
#             self.error.emit(str(e))



