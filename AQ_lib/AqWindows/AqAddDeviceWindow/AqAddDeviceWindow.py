import os

import serial
from PySide6.QtCore import Qt, QSettings, QThread, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidget, QDialog, QCheckBox, QTableWidgetItem, QFrame

import AqBaseDevice
import AqDeviceFabrica
from AQ_EventManager import AQ_EventManager
from AQ_IsValidIpFunc import is_valid_ip
from AqAddDevicesConnectErrorLabel import AqAddDeviceConnectErrorLabel
from AqSettingsFunc import load_last_combobox_state, load_last_text_value, save_combobox_current_state, \
    save_current_text_value


class AqAddDeviceWidget(QDialog):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        self.setObjectName("AqAddDeviceWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
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
        self.event_manager.register_event_handler('Add_device', self.add_selected_devices_to_session)

        # Створюємо порожній список для всіх знайдених девайсів
        self.all_found_devices = []

        # Підготовка необхідних полів UI
        self.prepare_ui_objects()

        # При старті одразу викликаємо оновлення стек-віджету та списку девайсів
        self.change_device_set_by_protocol_selection()
        self.change_page_by_interface_selection()

    def prepare_ui_objects(self):
        # Встановлюємо комбіновані імена в поля налаштувань (для збереження автозаповнення,
        # унікальні імена полів - це ключ для значення у auto_load_settings.ini)
        self.ui.protocol_combo_box.setObjectName(self.objectName() + "_" + self.ui.protocol_combo_box.objectName())
        self.ui.device_combo_box.setObjectName(self.objectName() + "_" + self.ui.device_combo_box.objectName())
        self.ui.interface_combo_box.setObjectName(self.objectName() + "_" + self.ui.interface_combo_box.objectName())
        self.ui.ip_line_edit.setObjectName(self.objectName() + "_" + self.ui.ip_line_edit.objectName())
        self.ui.boudrate_combo_box.setObjectName(self.objectName() + "_" + self.ui.boudrate_combo_box.objectName())
        self.ui.parity_combo_box.setObjectName(self.objectName() + "_" + self.ui.parity_combo_box.objectName())
        self.ui.stopbits_combo_box.setObjectName(self.objectName() + "_" + self.ui.stopbits_combo_box.objectName())
        self.ui.slave_id_line_edit.setObjectName(self.objectName() + "_" + self.ui.slave_id_line_edit.objectName())

        # Налаштовуємо комбо-бокс протоколів.
        self.ui.protocol_combo_box.activated.connect(self.change_device_set_by_protocol_selection)
        self.ui.protocol_combo_box.clear()
        self.ui.protocol_combo_box.addItems(AqDeviceFabrica.DeviceCreator.get_protocol_list())

        # Налаштовуємо комбо-бокс інтерфейсів
        # Связываем сигнал activated с обработчиком handle_combobox_selection
        self.ui.interface_combo_box.activated.connect(self.change_page_by_interface_selection)
        self.ui.interface_combo_box.clear()
        self.ui.interface_combo_box.addItems(AqDeviceFabrica.DeviceCreator.get_interface_list())

        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.ui.protocol_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.device_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.interface_combo_box)
            load_last_text_value(self.auto_load_settings, self.ui.ip_line_edit)
            load_last_combobox_state(self.auto_load_settings, self.ui.boudrate_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.parity_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.ui.stopbits_combo_box)
            load_last_text_value(self.auto_load_settings, self.ui.slave_id_line_edit)

        # Устанавливаем ширину столбцов в таблице справа
        cur_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(cur_width * 0.05))
        self.ui.tableWidget.setColumnWidth(1, int(cur_width * 0.47))
        self.ui.tableWidget.setColumnWidth(2, int(cur_width * 0.24))
        self.ui.tableWidget.setColumnWidth(3, int(cur_width * 0.17))
        self.ui.tableWidget.setFixedHeight(30)

        # Прив'язуємо кнопки до слотів
        self.ui.findBtn.clicked.connect(self.find_button_clicked)
        self.ui.addBtn.clicked.connect(self.add_selected_devices_to_session)

        #Скриємо кнопку "додати" до першого відображення знайденого девайсу
        self.ui.addBtn.hide()

    def change_page_by_interface_selection(self):
        selected_item = self.ui.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            widget = getattr(self.ui, "page_ip")
        else:
            widget = getattr(self.ui, "page_com")

        size = widget.sizeHint()
        if size.height() > widget.maximumHeight():
            height = widget.maximumHeight()
        else:
            height = size.height()

        self.ui.stackedWidget.setCurrentWidget(widget)
        self.ui.stackedWidget.setFixedHeight(height)

    def change_device_set_by_protocol_selection(self):
        protocol = self.ui.protocol_combo_box.currentText()
        devices = AqDeviceFabrica.DeviceCreator.get_device_list_by_protocol(protocol)
        if len(devices) > 0:
            self.ui.device_combo_box.show()
            self.ui.device_combo_box_label.show()
        else:
            self.ui.device_combo_box.hide()
            self.ui.device_combo_box_label.hide()
        # Добавляем имена файлов в комбобокс
        self.ui.device_combo_box.clear()
        self.ui.device_combo_box.addItems(devices)
        try:
            load_last_combobox_state(self.auto_load_settings, self.ui.device_combo_box)
        except:
            self.ui.device_combo_box.setCurrentIndex(0)

    def find_button_clicked(self):
        # Декативуємо кнопку для запобігання подвійного натискання до завершення пошуку
        self.ui.findBtn.setEnabled(False)
        # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
        selected_item = self.ui.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            ip = self.ui.ip_line_edit.text()
            if not is_valid_ip(ip):
                self.ui.ip_line_edit.red_blink_timer.start()
                self.ui.ip_line_edit.show_err_label()
                return
        elif selected_item == 'Offline':
            pass
        else:
            if self.ui.slave_id_line_edit.text() == '':
                self.ui.slave_id_line_edit.red_blink_timer.start()
                self.ui.slave_id_line_edit.show_err_label()
                return

        self.start_search()

    def start_search(self):
        self.ui.RotatingGearsWidget.start()
        # Запускаем функцию connect_to_device в отдельном потоке
        self.connect_thread = ConnectDeviceThread(self)
        self.connect_thread.finished.connect(self.search_finished)
        self.connect_thread.error.connect(self.search_error)
        self.connect_thread.result_signal.connect(self.search_successful)
        self.connect_thread.start()

    def search_finished(self):
        self.ui.RotatingGearsWidget.stop()
        self.ui.findBtn.setEnabled(True)

    def search_error(self, error_message):
        # Выполняется в случае ошибки при выполнении connect_to_device
        # В этом слоте можно выполнить действия, которые должны произойти в случае ошибки
        self.show_connect_err_label()
        self.ui.RotatingGearsWidget.stop()

    def search_successful(self, found_devices):
        self.add_devices_to_table_widget(found_devices)
        self.add_found_devices_to_all_list(found_devices)

    def connect_to_device(self):
        found_devices_list = []
        network_settings_list = self.get_network_settings_list()
        for i in range(len(network_settings_list)):
            device = AqDeviceFabrica.DeviceCreator.from_param_dict(network_settings_list[i])
            if device is not None:
                device_status = device.status
                if device_status == 'ok' or device_status == 'data_error':
                    found_devices_list.append(device)
                else:
                    self.show_connect_err_label()
            else:
                self.show_connect_err_label()

        return found_devices_list

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

        self.save_current_fields()

        return network_settings_list

    def save_current_fields(self):
        save_combobox_current_state(self.auto_load_settings, self.ui.protocol_combo_box)
        save_combobox_current_state(self.auto_load_settings, self.ui.device_combo_box)
        save_combobox_current_state(self.auto_load_settings, self.ui.interface_combo_box)
        save_combobox_current_state(self.auto_load_settings, self.ui.boudrate_combo_box)
        save_combobox_current_state(self.auto_load_settings, self.ui.parity_combo_box)
        save_combobox_current_state(self.auto_load_settings, self.ui.stopbits_combo_box)
        save_current_text_value(self.auto_load_settings, self.ui.ip_line_edit)
        save_current_text_value(self.auto_load_settings, self.ui.slave_id_line_edit)

    def add_devices_to_table_widget(self, found_devices):
        for i in range(len(found_devices)):
            self.ui.tableWidget.append_device_row(found_devices[i])

        # Відображаємо кнопку "додати"
        self.ui.addBtn.show()

    def add_found_devices_to_all_list(self, found_devices):
        for i in range(len(found_devices)):
            self.all_found_devices.append(found_devices[i])

    def add_selected_devices_to_session(self):
        devices_count = len(self.all_found_devices)
        for i in range(devices_count):
            checkbox_item = self.ui.tableWidget.cellWidget(i, 0)
            if checkbox_item is not None and isinstance(checkbox_item, QCheckBox):
                if checkbox_item.checkState() == Qt.Checked:
                    self.selected_devices_list.append(self.all_found_devices[i])

        self.event_manager.emit_event('add_new_devices', self.selected_devices_list)
        self.all_found_devices.clear()
        self.selected_devices_list.clear()
        self.close()

    def show_connect_err_label(self):
        self.connect_err_label = AqAddDeviceConnectErrorLabel(self.width(), 50, self.ui.mainWidget)
        self.connect_err_label.move(0, self.height() - 50)
        self.connect_err_label.show()


class AqAddDeviceTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
                                                           QTableWidget::item { padding-left: 3px; }""")

    def append_device_to_table(self, row, err_flag=0):
        if err_flag == 0:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#429061"))
        else:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#9d4d4f"))

        new_height = self.get_sum_of_rows_height() + 30
        self.setFixedHeight(new_height)

    def append_device_row(self, device: AqBaseDevice):
        if device.status == 'ok':
            err_flag = 0
        else:
            err_flag = 1

        new_row_index = self.rowCount()
        self.setRowCount(self.rowCount() + 1)
        # Создаем элементы таблицы для каждой строки
        checkbox_item = QTableWidgetItem()
        name_item = QTableWidgetItem(device.info('name'))
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        address_item = QTableWidgetItem(device.info('address'))
        address_item.setFlags(address_item.flags() & ~Qt.ItemIsEditable)
        version_item = QTableWidgetItem(device.info('version'))
        version_item.setFlags(version_item.flags() & ~Qt.ItemIsEditable)

        # Устанавливаем элементы таблицы
        self.setItem(new_row_index, 0, checkbox_item)
        self.setItem(new_row_index, 1, name_item)
        self.setItem(new_row_index, 2, address_item)
        self.setItem(new_row_index, 3, version_item)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if err_flag == 0:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.setCellWidget(new_row_index, 0, checkbox)
        item = self.item(new_row_index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.append_device_to_table(new_row_index, err_flag)

    def get_sum_of_rows_height(self):
        sum_height = 0
        for i in range(self.rowCount()):
            sum_height += self.rowHeight(i)

        return sum_height

class AqConnectionSettingsFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

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
