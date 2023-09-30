import os
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QFrame, QLabel
from AQ_CustomWindowTemplates import AQ_ComboBox, AQ_Label, AQ_IpLineEdit, AQ_SlaveIdLineEdit
import serial.tools.list_ports
from AQ_IsValidIpFunc import is_valid_ip
from AQ_SettingsFunc import save_current_text_value, save_combobox_current_state, load_last_text_value, \
                             load_last_combobox_state


class AQ_NetworkSettingsFrame(QFrame):
    def __init__(self, event_manager, parent):
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

        self.network_settings_layout = AQ_NetworkSettingsLayout(event_manager, self, self.auto_load_settings)

    def get_network_settings_list(self):
        network_settings_list = self.network_settings_layout.get_network_settings_list()
        # Якщо хтось викликав цю функцію, то одразу запам'ятовуємо введені в поля дані до "auto_load_settings.ini"
        self.save_current_settings()

        return network_settings_list

    def save_current_settings(self):
        self.network_settings_layout.save_current_fields()


class AQ_NetworkSettingsLayout(QVBoxLayout):
    def __init__(self, event_manager, parent, auto_load_settings=None):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.auto_load_settings = auto_load_settings
        self.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета
        self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета
        self.path = '110_device_conf/'


    # Создаем текстовую метку заголовка настроек соединения
        self.title_text = QLabel("Network parameters")
        self.title_text.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
        self.title_text.setFixedHeight(35)
        self.title_text.setFont(QFont("Verdana", 12))  # Задаем шрифт и размер
        self.title_text.setAlignment(Qt.AlignCenter)

    # Создание комбо-бокса вибору пристрою
        self.device_combo_box = AQ_ComboBox()
        self.device_combo_box.setObjectName(self.parent.objectName() + "_" + "device_combo_box")
        # Получаем список файлов в указанной директории
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

        # Добавляем имена файлов в комбобокс
        self.device_combo_box.addItems(files)

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
        # Связываем сигнал activated с обработчиком handle_combobox_selection
        self.interface_combo_box.activated.connect(self.change_view_by_combobox_selection)
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_combobox_state(self.auto_load_settings, self.interface_combo_box)

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
        self.find_btn = QPushButton("Find device", self.parent)
        self.find_btn.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.find_btn.setFixedSize(100, 35)
        self.find_btn.setStyleSheet("""
                    QPushButton {
                        border-left: 1px solid #9ef1d3;
                        border-top: 1px solid #9ef1d3;
                        border-bottom: 1px solid #5bb192;
                        border-right: 1px solid #5bb192;
                        color: #D0D0D0;
                        background-color: #2b2d30;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #3c3e41;
                    }
                    QPushButton:pressed {
                        background-color: #429061;
                    }
                """)
        self.find_btn.clicked.connect(self.find_button_clicked)

    # Додаємо все створені віджеті в порядку відображення
        self.addWidget(self.title_text)
        self.addWidget(self.device_combo_box)
        self.addWidget(self.interface_combo_box_label)
        self.addWidget(self.interface_combo_box)
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
            self.ip_line_edit_label.setVisible(True)
            self.ip_line_edit.setVisible(True)
            self.slave_id_line_edit_label.setVisible(False)
            self.slave_id_line_edit.setVisible(False)
        else:
            self.ip_line_edit_label.setVisible(False)
            self.ip_line_edit.setVisible(False)
            self.slave_id_line_edit_label.setVisible(True)
            self.slave_id_line_edit.setVisible(True)

    def get_network_settings_list(self):
        network_settings_list = []
        selected_dev = self.device_combo_box.currentText()
        selected_if = self.interface_combo_box.currentText()
        if selected_if == "Ethernet":
            address = self.ip_line_edit.text()
        else:
            address = int(self.slave_id_line_edit.text())

        network_setting = (selected_if, address, selected_dev)
        network_settings_list.append(network_setting)

        return network_settings_list

    def save_current_fields(self):
        save_combobox_current_state(self.parent.auto_load_settings, self.interface_combo_box)
        save_current_text_value(self.parent.auto_load_settings, self.ip_line_edit)
        save_current_text_value(self.parent.auto_load_settings, self.slave_id_line_edit)

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
