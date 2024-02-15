import os
import threading

import serial
from PySide6.QtCore import Qt, QSettings, QThread, Signal, QEvent, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QTableWidget, QCheckBox, QTableWidgetItem, QFrame, QWidget, QLabel

import AqBaseDevice
import AqDeviceFabrica
from AQ_EventManager import AQ_EventManager
from AqIsValidIpFunc import is_valid_ip
from AqAddDevicesConnectErrorLabel import AqAddDeviceConnectErrorLabel
from AqSettingsFunc import load_last_combobox_state, load_last_text_value, save_combobox_current_state, \
    save_current_text_value
from AqWatchListCore import AqWatchListCore
from AqWindowTemplate import AqDialogTemplate


class AqSetSlaveIdWindow(AqDialogTemplate):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Set slave ID'

        self.watch_core_save_state = AqWatchListCore.is_stopped()
        AqWatchListCore.set_pause_flag(True)

        self.event_manager = AQ_EventManager.get_global_event_manager()
        try:
            # Получаем текущий рабочий каталог (папку проекта)
            project_path = os.getcwd()
            # Объединяем путь к папке проекта с именем файла настроек
            settings_path = os.path.join(project_path, "auto_load_settings.ini")
            # Используем полученный путь в QSettings
            self.auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
        except:
            print('File "auto_load_settings.ini" not found')

        self.selected_devices_list = []
        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('set_slave_id_connect_error', self.show_connect_err_label)
        self.event_manager.register_event_handler('set_slave_id_connect_ok', self.show_success_write_label)

        # Підготовка необхідних полів UI
        self.prepare_ui_objects()

        # Викликаємо заповнення комбобоксу девайсів
        self.change_device_set_by_protocol_selection()


    def prepare_ui_objects(self):
        self.ui.setIdBtn.clicked.connect(self.find_button_clicked)

        self.ui.userMessageLabel.hide()

        # Встановлюємо комбіновані імена в поля налаштувань (для збереження автозаповнення,
        # унікальні імена полів - це ключ для значення у auto_load_settings.ini)
        self.ui.protocol_combo_box.setObjectName(self.objectName() + "_" + self.ui.protocol_combo_box.objectName())
        self.ui.device_combo_box.setObjectName(self.objectName() + "_" + self.ui.device_combo_box.objectName())
        self.ui.interface_combo_box.setObjectName(self.objectName() + "_" + self.ui.interface_combo_box.objectName())
        # self.ui.ip_line_edit.setObjectName(self.objectName() + "_" + self.ui.ip_line_edit.objectName())
        self.ui.boudrate_combo_box.setObjectName(self.objectName() + "_" + self.ui.boudrate_combo_box.objectName())
        self.ui.parity_combo_box.setObjectName(self.objectName() + "_" + self.ui.parity_combo_box.objectName())
        self.ui.stopbits_combo_box.setObjectName(self.objectName() + "_" + self.ui.stopbits_combo_box.objectName())
        self.ui.slave_id_line_edit.setObjectName(self.objectName() + "_" + self.ui.slave_id_line_edit.objectName())

        # Налаштовуємо комбо-бокс протоколів.
        self.ui.protocol_combo_box.activated.connect(self.change_device_set_by_protocol_selection)
        self.ui.protocol_combo_box.clear()
        self.ui.protocol_combo_box.addItem('Modbus')
        self.ui.protocol_combo_box.setCurrentText('Modbus')
        # self.ui.protocol_combo_box.hide()
        # self.ui.protocol_combo_box_label.hide()

        # Налаштовуємо комбо-бокс інтерфейсів
        # Связываем сигнал activated с обработчиком handle_combobox_selection
        # self.ui.interface_combo_box.activated.connect(self.change_page_by_interface_selection)
        self.ui.interface_combo_box.clear()
        com_ports_list = list()
        com_ports = serial.tools.list_ports.comports()
        # Заполняем выпадающий список COM-портами
        for port in com_ports:
            com_ports_list.append(port.description)

        self.ui.interface_combo_box.addItems(com_ports_list)

        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            # load_last_combobox_state(self.auto_load_settings, self.ui.protocol_combo_box)
            # load_last_combobox_state(self.auto_load_settings, self.ui.device_combo_box)
            # load_last_combobox_state(self.auto_load_settings, self.ui.interface_combo_box)
            # load_last_text_value(self.auto_load_settings, self.ui.ip_line_edit)
            load_last_combobox_state(self.auto_load_settings, self.ui.boudrate_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.parity_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.stopbits_combo_box)
            load_last_text_value(self.auto_load_settings, self.ui.slave_id_line_edit)

    def change_device_set_by_protocol_selection(self):
        protocol = self.ui.protocol_combo_box.currentText()
        devices = AqDeviceFabrica.DeviceCreator.get_device_list_by_protocol(protocol)
        devices.remove('МВ110-24_1ТД.csv')
        if len(devices) > 0:
            self.ui.device_combo_box.show()
            self.ui.device_combo_box_label.show()
        else:
            self.ui.device_combo_box.hide()
            self.ui.device_combo_box_label.hide()
        # Добавляем имена файлов в комбобокс
        self.ui.device_combo_box.clear()
        self.ui.device_combo_box.addItems(devices)
        self.ui.device_combo_box.setCurrentIndex(0)

    def find_button_clicked(self):
        self.ui.userMessageLabel.hide()
        # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
        # selected_item = self.interface_combo_box.currentText()
        if self.ui.slave_id_line_edit.text() == '':
            self.ui.slave_id_line_edit.red_blink_timer.start()
            self.ui.slave_id_line_edit.show_err_label()
            return

        network_settings = self.get_network_settings_list()

        self.event_manager.emit_event('set_slave_id', network_settings)

    # def find_button_clicked(self):
    #     # Декативуємо кнопку для запобігання подвійного натискання до завершення пошуку
    #     self.ui.setIdBtn.setEnabled(False)
    #
    #     # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
    #     selected_item = self.ui.interface_combo_box.currentText()
    #     if selected_item == "Ethernet":
    #         ip = self.ui.ip_line_edit.text()
    #         if not is_valid_ip(ip):
    #             self.ui.ip_line_edit.red_blink_timer.start()
    #             self.ui.ip_line_edit.show_err_label()
    #             return
    #     elif selected_item == 'Offline':
    #         pass
    #     else:
    #         if self.ui.slave_id_line_edit.text() == '':
    #             self.ui.slave_id_line_edit.red_blink_timer.start()
    #             self.ui.slave_id_line_edit.show_err_label()
    #             return
    #
    #     self.start_search()

    # def start_search(self):
    #     self.ui.RotatingGearsWidget.start()
    #     # Запускаем функцию connect_to_device в отдельном потоке
    #     self.connect_thread = ConnectDeviceThread(self.connect_to_device)
    #     self.connect_thread.finished.connect(self.search_finished)
    #     self.connect_thread.error.connect(self.search_error)
    #     self.connect_thread.result_signal.connect(self.search_successful)
    #     self.connect_thread.start()
    #
    # def search_finished(self):
    #     self.ui.RotatingGearsWidget.stop()
    #     self.ui.findBtn.show()
    #     self.ui.findBtn.setEnabled(True)
    #     self.ui.stopScanBtn.hide()
    #
    # def search_error(self, error_message):
    #     # Выполняется в случае ошибки при выполнении connect_to_device
    #     # В этом слоте можно выполнить действия, которые должны произойти в случае ошибки
    #     self.show_connect_err_label()
    #     self.ui.RotatingGearsWidget.stop()

    # def search_successful(self, found_devices):
    #     self.add_devices_to_table_widget(found_devices)
    #     self.add_found_devices_to_all_list(found_devices)

    # def connect_to_device(self):
    #     found_devices_list = []
    #     network_settings_list = self.get_network_settings_list()
    #     for i in range(len(network_settings_list)):
    #         device = AqDeviceFabrica.DeviceCreator.from_param_dict(network_settings_list[i])
    #         if device is not None:
    #             device_status = device.status
    #             if device_status == 'ok' or device_status == 'data_error':
    #                 found_devices_list.append(device)
    #             else:
    #                 self.show_connect_err_label()
    #         # else:
    #         #     self.show_connect_err_label()
    #
    #     return found_devices_list

    def get_network_settings_list(self):
        network_settings_list = []
        selected_protocol = self.ui.protocol_combo_box.currentText()
        selected_dev = self.ui.device_combo_box.currentText()
        selected_if = self.ui.interface_combo_box.currentText()
        if selected_if == "Ethernet":
            ip = self.ui.ip_line_edit.text()
            network_setting = {'interface': selected_if,
                               'interface_type': 'ip',
                               'ip': ip,
                               'device': selected_dev}
        elif selected_if == "Offline":
            network_setting = {'interface': selected_if,
                               'interface_type': 'Offline',
                               'device': selected_dev}
        else:
            address = int(self.ui.slave_id_line_edit.text())
            boudrate = int(self.ui.boudrate_combo_box.currentText())
            parity = self.ui.parity_combo_box.currentText()
            stopbits = int(self.ui.stopbits_combo_box.currentText())
            network_setting = {'interface': selected_if,
                               'interface_type': 'com',
                               'address': address,
                               'device': selected_dev,
                               'boudrate': boudrate,
                               'parity': parity,
                               'stopbits': stopbits}

        if selected_protocol == 'Modbus':
            network_setting['device_type'] = 'AqFileDescriptionDevice'
        elif selected_protocol == 'AqAutoDetectionProtocol':
            network_setting['device_type'] = 'AqAutoDetectionDevice'
        else:
            print(self.__name__ + 'Error: unknown device type')
            raise Exception(self.__name__ + 'Error: unknown device type')

        network_settings_list.append(network_setting)

        # self.save_current_fields()

        return network_settings_list

    # def save_current_fields(self):
    #     save_combobox_current_state(self.auto_load_settings, self.ui.protocol_combo_box)
    #     save_combobox_current_state(self.auto_load_settings, self.ui.device_combo_box)
    #     save_combobox_current_state(self.auto_load_settings, self.ui.interface_combo_box)
    #     save_combobox_current_state(self.auto_load_settings, self.ui.boudrate_combo_box)
    #     save_combobox_current_state(self.auto_load_settings, self.ui.parity_combo_box)
    #     save_combobox_current_state(self.auto_load_settings, self.ui.stopbits_combo_box)
    #     save_current_text_value(self.auto_load_settings, self.ui.ip_line_edit)
    #     save_current_text_value(self.auto_load_settings, self.ui.slave_id_line_edit)

    def show_connect_err_label(self):
        # self.connect_err_label = AqAddDeviceConnectErrorLabel(self.width(), 50, self.ui.mainWidget)
        # self.connect_err_label.move(0, self.height()-86)
        # self.connect_err_label.show()
        self.ui.userMessageLabel.setText('Connect error. Slave ID not set.')
        self.ui.userMessageLabel.setStyleSheet("color: #fe2d2d; \n")
        self.ui.userMessageLabel.show()

    def show_success_write_label(self):
        # # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        # self.success_label_widget = AQ_success_label_widget("<html>Succesfully<br>Response: OK<b<html>", self)
        # self.success_label_widget.move(self.width() // 2 - self.success_label_widget.width() // 2,
        #                                self.height() // 3 - self.success_label_widget.height() // 2)
        # self.success_label_widget.show()
        # # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        # QTimer.singleShot(4000, self.success_label_widget.deleteLater)
        self.ui.userMessageLabel.setText('Successfully! Response: OK')
        self.ui.userMessageLabel.setStyleSheet("color: #429061; \n")
        self.ui.userMessageLabel.show()

    def close(self):
        AqWatchListCore.set_pause_flag(self.watch_core_save_state)
        super().close()
