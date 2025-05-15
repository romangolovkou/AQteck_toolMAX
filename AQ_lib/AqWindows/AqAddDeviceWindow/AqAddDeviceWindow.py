import os
import threading

import serial
from PySide6.QtCore import Qt, QSettings, QThread, Signal, QEvent, QPoint, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QTableWidget, QCheckBox, QTableWidgetItem, QFrame, QWidget, QLabel, QLineEdit

import AqBaseDevice
import AqDeviceFabrica
from AQ_EventManager import AQ_EventManager
from AqIsValidIpFunc import is_valid_ip
from AqAddDevicesConnectErrorLabel import AqAddDeviceConnectErrorLabel
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
from AqWindowTemplate import AqDialogTemplate, AqWindowTemplate
from ui_AqEnterPassWidget import Ui_AqEnterPassWidget


class AqAddDeviceWidget(AqDialogTemplate):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False
        self.pass_widget = None

        # Створюємо та скидаємо евент примусової зупинки сканування мережі
        # для секції ScanNetwork (надає змогу передчасно зупинити потік сканування)
        self.scan_stop_event = QEvent(QEvent.User)
        self.scan_stop_event.setAccepted(False)

        self.name = AqTranslateManager.tr('Add devices')
        self.event_manager = AQ_EventManager.get_global_event_manager()

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
        # Прив'язуємо radiobattons до сторінок у внутрішьному стекед віджеті для ком-порту
        self.ui.deviceRadioBtn.toggled.connect(self.change_page_by_device_scan_mode_selection)
        self.ui.deviceRadioBtn.setChecked(True)
        self.ui.scanRadioBtn.toggled.connect(self.change_page_by_device_scan_mode_selection)
        self.ui.insideStackedWidget.setCurrentIndex(0)

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
        AqSettingsManager.load_last_combobox_state(self.ui.protocol_combo_box)
        AqSettingsManager.load_last_combobox_state(self.ui.device_combo_box)
        AqSettingsManager.load_last_combobox_state(self.ui.interface_combo_box)
        AqSettingsManager.load_last_ip_list(self.ui.ip_line_edit)
        AqSettingsManager.load_last_combobox_state(self.ui.boudrate_combo_box)
        AqSettingsManager.load_last_combobox_state(self.ui.parity_combo_box)
        AqSettingsManager.load_last_combobox_state(self.ui.stopbits_combo_box)
        AqSettingsManager.load_last_text_value(self.ui.slave_id_line_edit)

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
        self.ui.stopScanBtn.clicked.connect(lambda: self.scan_stop_event.setAccepted(True))

        #Скриємо кнопку "додати" до першого відображення знайденого девайсу
        self.ui.addBtn.hide()

        # Скриваємо кнопку стоп скан до початку сканування
        self.ui.stopScanBtn.hide()

        # Налаштовуємо поведінку секції ScanNetwork
        self.ui.pageScanNetwork.prepare_ui()

        # Підв'язуємо функцію до кліку на таблиці знайдених віджетів
        self.ui.tableWidget.clickedRow.connect(self.clicked_on_table_widget)

    def change_page_by_interface_selection(self):
        selected_item = self.ui.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            widget = getattr(self.ui, "page_ip")
        elif selected_item == 'Offline':
            widget = getattr(self.ui, "page_offline")
        else:
            widget = getattr(self.ui, "page_com")

        size = widget.sizeHint()
        if size.height() > widget.maximumHeight():
            height = widget.maximumHeight()
        else:
            height = size.height() + 10

        self.ui.stackedWidget.setCurrentWidget(widget)
        self.ui.stackedWidget.setFixedHeight(height)

        self.change_protocol_set_by_interface_selection()

    def change_page_by_device_scan_mode_selection(self):
        if self.ui.deviceRadioBtn.isChecked():
            selected_mode = 'device'
        elif self.ui.scanRadioBtn.isChecked():
            selected_mode = 'scan'
        else:
            raise Exception(self.objectName() + ' error: unknown mode')

        if selected_mode == 'device':
            widget = getattr(self.ui, "pageDevice")
        else:
            widget = getattr(self.ui, "pageScanNetwork")

        size = widget.sizeHint()
        if size.height() > widget.maximumHeight():
            height = widget.maximumHeight()
        else:
            height = size.height()

        self.ui.insideStackedWidget.setCurrentWidget(widget)
        self.ui.insideStackedWidget.setFixedHeight(height)
        self.change_page_by_interface_selection()

    def change_protocol_set_by_interface_selection(self):
        selected_item = self.ui.interface_combo_box.currentText()
        protocol_list = AqDeviceFabrica.DeviceCreator.get_protocol_list(selected_item)

        self.ui.protocol_combo_box.clear()
        self.ui.protocol_combo_box.addItems(protocol_list)

        try:
            AqSettingsManager.load_last_combobox_state(self.ui.protocol_combo_box)
        except:
            self.ui.protocol_combo_box.setCurrentIndex(0)

        self.change_device_set_by_protocol_selection()

    def change_device_set_by_protocol_selection(self):
        protocol = self.ui.protocol_combo_box.currentText()
        devices = AqDeviceFabrica.DeviceCreator.get_device_list_by_protocol(protocol)
        if len(devices) > 0:
            self.ui.device_combo_box.show()
            self.ui.device_combo_box_label.show()
        else:
            # потрапляємо сюди якщо автодетекшн
            self.ui.device_combo_box.hide()
            self.ui.device_combo_box_label.hide()
        # Добавляем имена файлов в комбобокс
        self.ui.device_combo_box.clear()
        self.ui.device_combo_box.addItems(devices)
        try:
            AqSettingsManager.load_last_combobox_state(self.ui.device_combo_box)
        except:
            self.ui.device_combo_box.setCurrentIndex(0)


    def find_button_clicked(self):
        # Декативуємо кнопку для запобігання подвійного натискання до завершення пошуку
        self.ui.findBtn.setEnabled(False)

        if self.ui.scanRadioBtn.isChecked() is True and self.ui.scanRadioBtn.isVisible():
            self.start_scan()
        else:
            # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
            selected_item = self.ui.interface_combo_box.currentText()
            if selected_item == "Ethernet":
                ip = self.ui.ip_line_edit.text()
                if not is_valid_ip(ip):
                    self.ui.ip_line_edit.red_blink_timer.start()
                    self.ui.ip_line_edit.show_err_label()
                    self.ui.findBtn.setEnabled(True)
                    return
            elif selected_item == 'Offline':
                pass
            else:
                if self.ui.slave_id_line_edit.text() == '':
                    self.ui.slave_id_line_edit.red_blink_timer.start()
                    self.ui.slave_id_line_edit.show_err_label()
                    self.ui.findBtn.setEnabled(True)
                    return

            self.start_search()

    def start_search(self):
        self.ui.RotatingGearsWidget.start()
        # Запускаем функцию connect_to_device в отдельном потоке
        self.connect_thread = ConnectDeviceThread(self.connect_to_device)
        self.connect_thread.finished.connect(self.search_finished)
        self.connect_thread.error.connect(self.search_error)
        self.connect_thread.result_signal.connect(self.search_successful)
        self.connect_thread.start()

    def start_scan(self):
        self.ui.RotatingGearsWidget.start()
        # Запускаем функцию connect_to_device в отдельном потоке
        self.scan_thread = ScanNetworkThread(self.scan_network)
        self.scan_thread.finished.connect(self.search_finished)
        self.scan_thread.error.connect(self.search_error)
        self.scan_thread.result_signal.connect(self.scan_successful)
        self.scan_thread.start()

    def search_finished(self):
        self.ui.RotatingGearsWidget.stop()
        self.ui.findBtn.show()
        self.ui.findBtn.setEnabled(True)
        self.ui.stopScanBtn.hide()

    def search_error(self, error_message):
        # Выполняется в случае ошибки при выполнении connect_to_device
        # В этом слоте можно выполнить действия, которые должны произойти в случае ошибки
        self.show_connect_err_label()
        self.ui.RotatingGearsWidget.stop()

    def search_successful(self, found_devices):
        if len(found_devices) > 0:
            for device in found_devices:
                for found_device in self.all_found_devices:
                    if device.info('address') == found_device.info('address'):
                        return

            self.add_devices_to_table_widget(found_devices)
            self.add_found_devices_to_all_list(found_devices)
        else:
            self.show_connect_err_label()

    def scan_successful(self, found_devices):
        if len(found_devices) > 0:
            for device in found_devices:
                for found_device in self.all_found_devices:
                    if device.info('address') == found_device.info('address'):
                        return

            self.add_devices_to_table_widget(found_devices)
            self.add_found_devices_to_all_list(found_devices)
        else:
            self.ui.pageScanNetwork.show_not_found_error()

    def connect_to_device(self):
        found_devices_list = []
        network_settings_list = self.get_network_settings_list()
        for i in range(len(network_settings_list)):
            device = AqDeviceFabrica.DeviceCreator.from_param_dict(network_settings_list[i])
            if device is not None:
                device_status = device.status
                if device_status == 'ok' or device_status == 'decrypt_err'\
                        or device_status == 'parsing_err' or device_status == 'need_pass':
                    found_devices_list.append(device)
                else:
                    self.show_connect_err_label()
            # else:
            #     self.show_connect_err_label()

        return found_devices_list

    def scan_network(self):
        self.ui.findBtn.setEnabled(False)
        self.ui.findBtn.hide()
        self.ui.stopScanBtn.show()
        found_devices_list = []
        scan_network_list = self.get_scan_network_list()
        first_find_stop_flag = self.ui.firstFindCheckBox.isChecked()
        for i in range(len(scan_network_list)):
            if self.scan_stop_event.isAccepted():
                self.scan_stop_event.setAccepted(False)
                break
            network_settings = scan_network_list[i]
            boudrate = network_settings.get('boudrate', None)
            parity = network_settings.get('parity', None)
            stopbits = network_settings.get('stopbits', None)
            address = network_settings.get('address', None)
            print(f'Scan network: Try find -> Boudrate-{boudrate}, Parity-{parity}')
            print(f'                           Stopbits-{stopbits}, Address-{address}')
            try:
                device = AqDeviceFabrica.DeviceCreator.from_param_dict(scan_network_list[i])

            except Exception as e:
                device = None
                print('              Result: Not found')

            if device is not None:
                device_status = device.status
                if device_status == 'ok' or device_status == 'data_error':
                    found_devices_list.append(device)
                    print('              Result: Found!')
                    if first_find_stop_flag is True:
                        self.scan_stop_event.setAccepted(True)
            else:
                print('              Result: Not found')

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

        self.save_current_fields()

        return network_settings_list

    def get_scan_network_list(self):
        scan_network_list = []
        selected_protocol = self.ui.protocol_combo_box.currentText()
        selected_dev = self.ui.device_combo_box.currentText()
        selected_if = self.ui.interface_combo_box.currentText()
        # if selected_if == "Ethernet":
        #     ip = self.ui.ip_line_edit.text()
        #     network_setting = {'interface': selected_if,
        #                        'interface_type': 'ip',
        #                        'ip': ip,
        #                        'device': selected_dev}
        # elif selected_if == "Offline":
        #     network_setting = {'interface': selected_if,
        #                        'interface_type': 'Offline',
        #                        'device': selected_dev}
        # else:
        boudrate_list = self.get_scan_boudrate_list()
        address_list = self.get_scan_address_list()
        parity_list = self.get_scan_parity_list()
        stopbits_list = self.get_scan_stopbits_list()
        for boudrate in boudrate_list:
            for parity in parity_list:
                for stopbits in stopbits_list:
                    for address in address_list:
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

                        scan_network_list.append(network_setting)

        self.save_current_fields()

        return scan_network_list

    def get_scan_boudrate_list(self):
        boudrate_list = list()
        if self.ui.checkBox4800.isChecked():
            boudrate_list.append(4800)
        if self.ui.checkBox9600.isChecked():
            boudrate_list.append(9600)
        if self.ui.checkBox19200.isChecked():
            boudrate_list.append(19200)
        if self.ui.checkBox38400.isChecked():
            boudrate_list.append(38400)
        if self.ui.checkBox57600.isChecked():
            boudrate_list.append(57600)
        if self.ui.checkBox115200.isChecked():
            boudrate_list.append(115200)

        if len(boudrate_list) == 0:
            raise Exception('Scan network error: empty boudrate!')

        return boudrate_list

    def get_scan_address_list(self):
        start_address = int(self.ui.startLineEdit.text())
        end_address = int(self.ui.endLineEdit.text())
        if start_address > end_address:
            raise Exception('Scan network error: incorrect address!')

        address_list = list(range(start_address, end_address + 1))
        return address_list

    def get_scan_parity_list(self):
        parity_list = list()
        if self.ui.checkBoxNone.isChecked():
            parity_list.append('None')
        if self.ui.checkBoxEven.isChecked():
            parity_list.append('Even')
        if self.ui.checkBoxOdd.isChecked():
            parity_list.append('Odd')

        if len(parity_list) == 0:
            raise Exception('Scan network error: empty parity!')

        return parity_list

    def get_scan_stopbits_list(self):
        stopbits_list = list()
        if self.ui.checkBox1sb.isChecked():
            stopbits_list.append(1)
        if self.ui.checkBox2sb.isChecked():
            stopbits_list.append(2)

        if len(stopbits_list) == 0:
            raise Exception('Scan network error: empty stopbits!')

        return stopbits_list

    def save_current_fields(self):
        AqSettingsManager.save_combobox_current_state(self.ui.protocol_combo_box)
        AqSettingsManager.save_combobox_current_state(self.ui.device_combo_box)
        AqSettingsManager.save_combobox_current_state(self.ui.interface_combo_box)
        AqSettingsManager.save_combobox_current_state(self.ui.boudrate_combo_box)
        AqSettingsManager.save_combobox_current_state(self.ui.parity_combo_box)
        AqSettingsManager.save_combobox_current_state(self.ui.stopbits_combo_box)
        AqSettingsManager.save_current_ip_to_list(self.ui.ip_line_edit)
        AqSettingsManager.save_current_text_value(self.ui.slave_id_line_edit)

    def add_devices_to_table_widget(self, found_devices):
        for i in range(len(found_devices)):
            self.ui.tableWidget.append_device_row(found_devices[i])

        # Відображаємо кнопку "додати"
        if len(found_devices) > 0:
            self.ui.addBtn.show()

    def add_found_devices_to_all_list(self, found_devices):
        for i in range(len(found_devices)):
            self.all_found_devices.append(found_devices[i])

    def add_selected_devices_to_session(self):
        self.ui.addBtn.setEnabled(False)
        devices_count = len(self.all_found_devices)
        for i in range(devices_count):
            checkbox_item = self.ui.tableWidget.cellWidget(i, 0)
            if checkbox_item is not None and isinstance(checkbox_item, QCheckBox):
                if checkbox_item.checkState() == Qt.Checked:
                    self.selected_devices_list.append(self.all_found_devices[i])

        AqDeviceFabrica.DeviceCreator.add_device(self.selected_devices_list)
        self.close()

    def show_connect_err_label(self):
        self.connect_err_label = AqAddDeviceConnectErrorLabel(self.width(), 50, self.ui.mainWidget)
        self.connect_err_label.move(0, self.height()-86)
        self.connect_err_label.show()

    def clicked_on_table_widget(self, row, pos):
        if self.all_found_devices[row]._status == 'need_pass':
            self.pass_widget = AqPasswordWidget(self.all_found_devices[row], row,
                                                self.ui.tableWidget.replace_device_in_row)
            self.pass_widget.exec()


class AqAddDeviceTableWidget(QTableWidget):
    clickedRow = Signal(int, QPoint)

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
        self.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self, row, col):
        item = self.item(row, col)
        if item:
            item_rect = self.visualItemRect(item)
            pos = self.viewport().mapTo(self.parent(), item_rect.topLeft())
            self.clickedRow.emit(row, pos)

    def append_device_to_table(self, row, status='ok'):
        if status == 'ok':
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#429061"))
        elif status == 'need_pass':
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#807c7c"))
        else:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#9d4d4f"))

        new_height = self.get_sum_of_rows_height() + 30
        self.setFixedHeight(new_height)

    def append_device_row(self, device: AqBaseDevice, new_row_index=None):
        status = device.status

        if new_row_index is None:
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

        if status == 'need_pass':
            tip_str = AqTranslateManager.tr('Enter password. CLick to enter')
            checkbox_item.setToolTip(tip_str)
            name_item.setToolTip(tip_str)
            address_item.setToolTip(tip_str)
            version_item.setToolTip(tip_str)

        # Устанавливаем элементы таблицы
        self.setItem(new_row_index, 0, checkbox_item)
        self.setItem(new_row_index, 1, name_item)
        self.setItem(new_row_index, 2, address_item)
        self.setItem(new_row_index, 3, version_item)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if status == 'ok':
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.setCellWidget(new_row_index, 0, checkbox)
        item = self.item(new_row_index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.append_device_to_table(new_row_index, status)

    def replace_device_in_row(self, device: AqBaseDevice, row: int):
        self.append_device_row(device, row)


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

    def __init__(self, connect_func):
        super().__init__()
        self.connect_func = connect_func

    def run(self):
        try:
            result_data = self.connect_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))


class ScanNetworkThread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно

    def __init__(self, scan_func):
        super().__init__()
        self.scan_func = scan_func

    def run(self):
        try:
            result_data = self.scan_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))


class AqPasswordWidget(AqDialogTemplate):
    def __init__(self, device, row, callback, parent=None):
        super().__init__(parent)
        self.device = device
        self.current_row = row
        self.callback = callback
        self.password = None
        self.ui = Ui_AqEnterPassWidget()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False
        self.minimizeBtnEnable = False
        # self.resizeFrameEnable = [True, 5]
        self.name = 'Enter password'
        self.adjustSize()
        self.ui.okBtn.clicked.connect(self.try_password)
        self.ui.cancelBtn.clicked.connect(self.close)
        self.ui.passLineFrame.prepare_ui()

    def try_password(self):
        self.ui.okBtn.setEnabled(False)
        self.password = self.ui.passLineEdit.text()
        if self.password != '':
            self.start_reinit_with_pass()
        else:
            self.show_err_label()

    def start_reinit_with_pass(self):
        # Запускаем функцию connect_to_device в отдельном потоке
        self.reinit_thread = ReinitDeviceWithPassThread(lambda: self.device.reinit_device_with_pass(self.password))
        self.reinit_thread.finished.connect(self.reinit_finished)
        self.reinit_thread.error.connect(self.reinit_error)
        self.reinit_thread.result_signal.connect(self.reinit_successful)
        self.reinit_thread.start()

    def reinit_successful(self, status):
        self.ui.okBtn.setEnabled(True)
        if status == 'ok':
            self.callback(self.device, self.current_row)
            self.close()
        else:
            self.show_err_label()

    def reinit_finished(self):
        self.ui.okBtn.setEnabled(True)
        pass

    def reinit_error(self):
        self.ui.okBtn.setEnabled(True)
        pass

    def show_err_label(self):
        # Получаем координаты поля ввода относительно окна
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.err_label = QLabel(AqTranslateManager.tr('Wrong password'), self)
        self.err_label.setStyleSheet("color: #fe2d2d; background-color: transparent; border-radius: 3px;\n")
        self.err_label.setFont(QFont("Segoe UI", 10))
        self.err_label.move(35, 60)
        self.err_label.setFixedWidth(self.width() * 0.9)
        self.err_label.show()

        QTimer.singleShot(3000, self.err_label.deleteLater)

    # def leaveEvent(self, event):
    #     self.hide()
    #     super().leaveEvent(event)
    #     self.deleteLater()


class ReinitDeviceWithPassThread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно

    def __init__(self, reinit_func):
        super().__init__()
        self.reinit_func = reinit_func

    def run(self):
        try:
            result_data = self.reinit_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))


# class InitDeviceParamsThread(QThread):
#     finished = Signal()
#     error = Signal(str)
#     result_signal = Signal(object)  # Сигнал для передачи данных в главное окно
#
#     def __init__(self, devices_list, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.devices_list = devices_list
#
#     def run(self):
#         try:
#             for i in range(len(self.devices_list)):
#                 self.devices_list[-1].init_parameters()
#             # По завершении успешного выполнения
#             self.finished.emit()
#         except Exception as e:
#             # В случае ошибки передаем текст ошибки обратно в главный поток
#             self.error.emit(str(e))
