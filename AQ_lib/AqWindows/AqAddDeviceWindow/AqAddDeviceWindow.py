import os

import serial
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidget, QDialog, QWidget, QCheckBox, QTableWidgetItem, QFrame, QVBoxLayout, \
    QComboBox

import AqBaseDevice
from AQ_AddDevicesRotatingGears import AQ_RotatingGearsWidget
from AQ_AddDevicesWindow import ConnectDeviceThread
from AQ_IsValidIpFunc import is_valid_ip
from AqEventManager import AqEventManager
from AqSettingsFunc import load_last_combobox_state, load_last_text_value


class AqAddDeviceWidget(QDialog):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        self.setObjectName("AqAddDeviceWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.path = '110_device_conf/'
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        getattr(self.ui, "findBtn").clicked.connect(self.find_button_clicked)
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
        # self.event_manager = event_manager
        # Рєєструємо обробники подій
        AqEventManager.register_event_handler('Find_device', self.on_find_button_clicked)
        AqEventManager.register_event_handler('Add_device', self.add_selected_devices_to_session)

        # Створюємо віджет з рухомими шестернями
        # self.ui.rotating_gears = AQ_RotatingGearsWidget(self.ui.RotatingGearsFrame)

        # Створюємо порожній список для всіх знайдених девайсів
        self.all_finded_devices = []

        # Отримуємо посилання на поля налаштувань
        self.protocol_combo_box = getattr(self.ui, 'protocol_combo_box')
        self.protocol_combo_box.setObjectName(self.objectName() + "_" + self.protocol_combo_box.objectName())
        self.device_combo_box = getattr(self.ui, 'device_combo_box')
        self.device_combo_box.setObjectName(self.objectName() + "_" + self.device_combo_box.objectName())
        self.interface_combo_box = getattr(self.ui, 'interface_combo_box')
        self.interface_combo_box.setObjectName(self.objectName() + "_" + self.interface_combo_box.objectName())
        self.ip_line_edit = getattr(self.ui, 'ip_line_edit')
        self.ip_line_edit.setObjectName(self.objectName() + "_" + self.ip_line_edit.objectName())
        self.boudrate_combo_box = getattr(self.ui, 'boudrate_combo_box')
        self.boudrate_combo_box.setObjectName(self.objectName() + "_" + self.boudrate_combo_box.objectName())
        self.parity_combo_box = getattr(self.ui, 'parity_combo_box')
        self.parity_combo_box.setObjectName(self.objectName() + "_" + self.parity_combo_box.objectName())
        self.stopbits_combo_box = getattr(self.ui, 'stopbits_combo_box')
        self.stopbits_combo_box.setObjectName(self.objectName() + "_" + self.stopbits_combo_box.objectName())
        self.slave_id_line_edit = getattr(self.ui, 'slave_id_line_edit')
        self.slave_id_line_edit.setObjectName(self.objectName() + "_" + self.slave_id_line_edit.objectName())
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.protocol_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.device_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.interface_combo_box)
            load_last_text_value(self.auto_load_settings, self.ip_line_edit)
            load_last_combobox_state(self.auto_load_settings, self.boudrate_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.parity_combo_box)
            load_last_combobox_state(self.auto_load_settings, self.stopbits_combo_box)
            load_last_text_value(self.auto_load_settings, self.slave_id_line_edit)

        # Налаштовуємо комбо-бокс протоколів.
        self.protocol_combo_box.activated.connect(self.change_device_set_by_protocol_selection)

        # Налаштовуємо комбо-бокс інтерфейсів
        # Наповнення комбо-боксу інтерфейсу, ком-портами
        # Получаем список доступных COM-портов
        self.com_ports = serial.tools.list_ports.comports()
        # Заполняем выпадающий список COM-портами
        for port in self.com_ports:
            self.interface_combo_box.addItem(port.description)
            # Связываем сигнал activated с обработчиком handle_combobox_selection
            self.interface_combo_box.activated.connect(self.change_page_by_interface_selection)

        # При старті одразу викликаємо оновлення стек-віджету та списку девайсів
        self.change_device_set_by_protocol_selection()
        self.change_page_by_interface_selection()

        self.all_finded_devices = []

    def change_page_by_interface_selection(self):
        communicate_settings_stacked_widget = getattr(self.ui, "stackedWidget")
        selected_item = self.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            widget = getattr(self.ui, "page_ip")
        else:
            widget = getattr(self.ui, "page_com")

        size = widget.sizeHint()
        if size.height() > widget.maximumHeight():
            height = widget.maximumHeight()
        else:
            height = size.height()

        communicate_settings_stacked_widget.setCurrentWidget(widget)
        communicate_settings_stacked_widget.setFixedHeight(height)

    def change_device_set_by_protocol_selection(self):
        # self.device_combo_box.setObjectName(self.parent.objectName() + "_" + "device_combo_box")
        if self.protocol_combo_box.currentText() == 'Modbus':
            # Получаем список файлов в указанной директории
            devices = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        elif self.protocol_combo_box.currentText() == 'AQ AutoDetectionProtocol':
            devices = ["AQ AutoDetectionDevice"]
        else:
            devices = []
        # Добавляем имена файлов в комбобокс
        self.device_combo_box.clear()
        self.device_combo_box.addItems(devices)
        try:
            load_last_combobox_state(self.auto_load_settngs, self.device_combo_box)
        except:
            self.device_combo_box.setCurrentIndex(0)

    def get_network_settings_list(self):
        network_settings_list = self.network_settings_layout.get_network_settings_list()
        # Якщо хтось викликав цю функцію, то одразу запам'ятовуємо введені в поля дані до "auto_load_settings.ini"
        self.save_current_settings()

        return network_settings_list

    def save_current_settings(self):
        self.network_settings_layout.save_current_fields()

    def find_button_clicked(self):
        # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
        selected_item = self.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            ip = self.ip_line_edit.text()
            if not is_valid_ip(ip):
                self.ip_line_edit.red_blink_timer.start()
                self.ip_line_edit.show_err_label()
                return
        elif selected_item == 'Offline':
            pass
        else:
            if self.slave_id_line_edit.text() == '':
                self.slave_id_line_edit.red_blink_timer.start()
                self.slave_id_line_edit.show_err_label()
                return

        self.event_manager.emit_event('Find_device')

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
        # Создаем QTableWidget с 4 столбцами
        self.setColumnCount(3)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)

        # Добавляем заголовки столбцов
        self.setHorizontalHeaderLabels(["", "Name", "Address"])
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        # Устанавливаем ширину столбцов
        cur_width = self.width()
        self.setColumnWidth(0, int(cur_width * 0.05))
        self.setColumnWidth(1, int(cur_width * 0.58))
        self.setColumnWidth(2, int(cur_width * 0.37))
        # self.setColumnWidth(3, int(cur_width * 0.20))
        # Установите высоту строк по умолчанию
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
                                                           QTableWidget::item { padding-left: 3px; }""")

    def set_style_table_widget_item(self, row, err_flag=0):
        if err_flag == 0:
            for i in range(3):
                self.item(row, i).setBackground(QColor("#429061"))
        else:
            for i in range(3):
                self.item(row, i).setBackground(QColor("#9d4d4f"))

        # TODO: Rename this func like "append_device_to_table"

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
        # version_item = QTableWidgetItem(device_data.get('version'))
        # version_item.setFlags(version_item.flags() & ~Qt.ItemIsEditable)

        # Устанавливаем элементы таблицы
        self.setItem(new_row_index, 0, checkbox_item)
        self.setItem(new_row_index, 1, name_item)
        self.setItem(new_row_index, 2, address_item)
        # self.setItem(new_row_index, 3, version_item)

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

        self.set_style_table_widget_item(new_row_index, err_flag)

    def get_sum_of_rows_height(self):
        sum_height = 0
        for i in range(self.rowCount()):
            sum_height += self.rowHeight(i)

        return sum_height

class AqConnectionSettingsFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("AQ_Dialog_network_frame")
        try:
            # Получаем текущий рабочий каталог (папку проекта)
            project_path = os.getcwd()
            # Объединяем путь к папке проекта с именем файла настроек
            settings_path = os.path.join(project_path, "auto_load_settings.ini")
            # Используем полученный путь в QSettings
            self.auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
        except:
            print('File "auto_load_settings.ini" not found')

        # self.network_settings_layout = AQ_NetworkSettingsLayout(event_manager, self, self.auto_load_settings)

    def get_network_settings_list(self):
        network_settings_list = []
        selected_dev = self.device_combo_box.currentText()
        selected_if = self.interface_combo_box.currentText()
        if selected_if == "Ethernet":
            ip = self.ip_line_edit.text()
            network_setting = {'interface': selected_if,
                               'ip': ip,
                               'device': selected_dev}
        else:
            address = int(self.slave_id_line_edit.text())
            boudrate = int(self.boudrate_combo_box.currentText())
            parity = self.parity_combo_box.currentText()
            stopbits = int(self.stopbits_combo_box.currentText())
            network_setting = {'interface': selected_if,
                               'address': address,
                               'device': selected_dev,
                               'boudrate': boudrate,
                               'parity': parity,
                               'stopbits': stopbits}

        network_settings_list.append(network_setting)

        return network_settings_list

    # def get_network_settings_list(self):
    #     network_settings_list = self.network_settings_layout.get_network_settings_list()
    #     # Якщо хтось викликав цю функцію, то одразу запам'ятовуємо введені в поля дані до "auto_load_settings.ini"
    #     self.save_current_settings()
    #
    #     return network_settings_list
    #
    # def save_current_settings(self):
    #     self.network_settings_layout.save_current_fields()


class AQ_NetworkSettingsLayout(QVBoxLayout):
    def __init__(self, event_manager, parent, auto_load_settings=None):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.auto_load_settings = auto_load_settings
        # self.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета
        # self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета
        self.path = '110_device_conf/'


    # # Создаем текстовую метку заголовка настроек соединения
    #     self.title_text = QLabel("Network parameters")
    #     self.title_text.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
    #     self.title_text.setFixedHeight(35)
    #     self.title_text.setFont(QFont("Verdana", 12))  # Задаем шрифт и размер
    #     self.title_text.setAlignment(Qt.AlignCenter)
    #
    # # Создаем текстовую метку выбора Device
    #     self.device_combo_box_label = AQ_Label("Device")

    # Создание комбо-бокса вибору пристрою
        self.device_combo_box = AQ_ComboBox()
        self.device_combo_box.setObjectName(self.parent.objectName() + "_" + "device_combo_box")
        # Получаем список файлов в указанной директории
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        files.append("AqAutoDetectionDevice")
        # Добавляем имена файлов в комбобокс
        self.device_combo_box.addItems(files)
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.device_combo_box)

    # Создаем текстовую метку выбора интерфейса
        self.interface_combo_box_label = AQ_Label("Interface")

    # Создание комбо-бокса інтерфейсу
        self.interface_combo_box = AQ_ComboBox()
        self.interface_combo_box.setObjectName(self.parent.objectName() + "_" + "interface_combo_box")
        self.interface_combo_box.addItem("Ethernet")  # Добавление опции "Ethernet"
        # Получаем список доступных COM-портов
        self.com_ports = serial.tools.list_ports.comports()
        # Заполняем выпадающий список COM-портами
        for port in self.com_ports:
            self.interface_combo_box.addItem(port.description)
        self.serial = None
        # Додавання опції Offline
        self.interface_combo_box.addItem("Offline")
        # Связываем сигнал activated с обработчиком handle_combobox_selection
        self.interface_combo_box.activated.connect(self.change_view_by_combobox_selection)
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.interface_combo_box)

    # Создаем текстовую метку выбора интерфейса
        self.boudrate_combo_box_label = AQ_Label("Boudrate")

    # Создание комбо-бокса швидкості
        self.boudrate_combo_box = AQ_ComboBox()
        self.boudrate_combo_box.setObjectName(self.parent.objectName() + "_" + "boudrate_combo_box")
        self.boudrate_combo_box.addItem("4800")
        self.boudrate_combo_box.addItem("9600")
        self.boudrate_combo_box.addItem("19200")
        self.boudrate_combo_box.addItem("38400")
        self.boudrate_combo_box.addItem("57600")
        self.boudrate_combo_box.addItem("115200")

        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.boudrate_combo_box)

    # Создаем текстовую метку выбора четности
        self.parity_combo_box_label = AQ_Label("Parity")

        # Создание комбо-бокса швидкості
        self.parity_combo_box = AQ_ComboBox()
        self.parity_combo_box.setObjectName(self.parent.objectName() + "_" + "parity_combo_box")
        self.parity_combo_box.addItem("None")
        self.parity_combo_box.addItem("Even")
        self.parity_combo_box.addItem("Odd")

        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.parity_combo_box)

    # Создаем текстовую метку выбора четности
        self.stopbits_combo_box_label = AQ_Label("Stop bits")

        # Создание комбо-бокса швидкості
        self.stopbits_combo_box = AQ_ComboBox()
        self.stopbits_combo_box.setObjectName(self.parent.objectName() + "_" + "stopbits_combo_box")
        self.stopbits_combo_box.addItem("1")
        self.stopbits_combo_box.addItem("2")

        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.stopbits_combo_box)

    # Создаем поле ввода IP адресса
        self.ip_line_edit_label = AQ_Label("IP Address")
        self.ip_line_edit = AQ_IpLineEdit()
        self.ip_line_edit.setObjectName(self.parent.objectName() + "_" + "ip_line_edit")
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_text_value(self.auto_load_settings, self.ip_line_edit)

    # Создаем поле ввода Slave ID
        self.slave_id_line_edit_label = AQ_Label("Slave ID")
        self.slave_id_line_edit = AQ_SlaveIdLineEdit()
        self.slave_id_line_edit.setObjectName(self.parent.objectName() + "_" + "slave_id_line_edit")
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_text_value(self.auto_load_settings, self.slave_id_line_edit)

    # Створюэмо кнопку знайти
    #     self.find_btn = QPushButton("Find device", self.parent)
    #     self.find_btn.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
    #     self.find_btn.setFixedSize(100, 35)
    #     self.find_btn.setStyleSheet("""
    #                 QPushButton {
    #                     border-left: 1px solid #9ef1d3;
    #                     border-top: 1px solid #9ef1d3;
    #                     border-bottom: 1px solid #5bb192;
    #                     border-right: 1px solid #5bb192;
    #                     color: #D0D0D0;
    #                     background-color: #2b2d30;
    #                     border-radius: 4px;
    #                 }
    #                 QPushButton:hover {
    #                     background-color: #3c3e41;
    #                 }
    #                 QPushButton:pressed {
    #                     background-color: #429061;
    #                 }
    #             """)
        self.find_btn.clicked.connect(self.find_button_clicked)

    # Додаємо все створені віджеті в порядку відображення
        self.addWidget(self.title_text)
        self.addWidget(self.device_combo_box_label)
        self.addWidget(self.device_combo_box)
        self.addWidget(self.interface_combo_box_label)
        self.addWidget(self.interface_combo_box)
        self.addWidget(self.boudrate_combo_box_label)
        self.addWidget(self.boudrate_combo_box)
        self.addWidget(self.parity_combo_box_label)
        self.addWidget(self.parity_combo_box)
        self.addWidget(self.stopbits_combo_box_label)
        self.addWidget(self.stopbits_combo_box)
        self.addWidget(self.ip_line_edit_label)
        self.addWidget(self.ip_line_edit)
        self.addWidget(self.slave_id_line_edit_label)
        self.addWidget(self.slave_id_line_edit)
        self.addWidget(self.find_btn)

    # Оновлюємо відображення полів вводу
        self.change_view_by_combobox_selection()

    def change_view_by_combobox_selection(self):
        selected_item = self.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            self.boudrate_combo_box_label.setVisible(False)
            self.boudrate_combo_box.setVisible(False)
            self.ip_line_edit_label.setVisible(True)
            self.ip_line_edit.setVisible(True)
            self.slave_id_line_edit_label.setVisible(False)
            self.slave_id_line_edit.setVisible(False)
            self.parity_combo_box_label.setVisible(False)
            self.parity_combo_box.setVisible(False)
            self.stopbits_combo_box_label.setVisible(False)
            self.stopbits_combo_box.setVisible(False)
        else:
            self.boudrate_combo_box_label.setVisible(True)
            self.boudrate_combo_box.setVisible(True)
            self.ip_line_edit_label.setVisible(False)
            self.ip_line_edit.setVisible(False)
            self.slave_id_line_edit_label.setVisible(True)
            self.slave_id_line_edit.setVisible(True)
            self.parity_combo_box_label.setVisible(True)
            self.parity_combo_box.setVisible(True)
            self.stopbits_combo_box_label.setVisible(True)
            self.stopbits_combo_box.setVisible(True)

    def get_network_settings_list(self):
        network_settings_list = []
        selected_dev = self.device_combo_box.currentText()
        selected_if = self.interface_combo_box.currentText()
        if selected_if == "Ethernet":
            ip = self.ip_line_edit.text()
            network_setting = {'interface': selected_if,
                               'ip': ip,
                               'device': selected_dev}
        else:
            address = int(self.slave_id_line_edit.text())
            boudrate = int(self.boudrate_combo_box.currentText())
            parity = self.parity_combo_box.currentText()
            stopbits = int(self.stopbits_combo_box.currentText())
            network_setting = {'interface': selected_if,
                               'address': address,
                               'device': selected_dev,
                               'boudrate': boudrate,
                               'parity': parity,
                               'stopbits': stopbits}

        network_settings_list.append(network_setting)

        return network_settings_list

    def save_current_fields(self):
        save_combobox_current_state(self.parent.auto_load_settings, self.interface_combo_box)
        save_current_text_value(self.parent.auto_load_settings, self.ip_line_edit)
        save_current_text_value(self.parent.auto_load_settings, self.slave_id_line_edit)
        save_combobox_current_state(self.parent.auto_load_settings, self.device_combo_box)
        save_combobox_current_state(self.parent.auto_load_settings, self.boudrate_combo_box)
        save_combobox_current_state(self.parent.auto_load_settings, self.parity_combo_box)
        save_combobox_current_state(self.parent.auto_load_settings, self.stopbits_combo_box)


    def find_button_clicked(self):
        # Перед викликом події перевіряємо чи не порожні поля, та корректні в них дані
        selected_item = self.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            ip = self.ip_line_edit.text()
            if not is_valid_ip(ip):
                self.ip_line_edit.red_blink_timer.start()
                self.ip_line_edit.show_err_label()
                return
        else:
            if self.slave_id_line_edit.text() == '':
                self.slave_id_line_edit.red_blink_timer.start()
                self.slave_id_line_edit.show_err_label()
                return

        self.event_manager.emit_event('Find_device')

# class AqInterfaceComboBox(QComboBox):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # self.interface_combo_box.setObjectName(self.parent.objectName() + "_" + "interface_combo_box")
#         # self.interface_combo_box.addItem("Ethernet")  # Добавление опции "Ethernet"
#         # Получаем список доступных COM-портов
#         self.com_ports = serial.tools.list_ports.comports()
#         # Заполняем выпадающий список COM-портами
#         for port in self.com_ports:
#             self.addItem(port.description)
#         # self.serial = None
#         # Додавання опції Offline
#         # self.interface_combo_box.addItem("Offline")
