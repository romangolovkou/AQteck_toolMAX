import os
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QFrame, QGraphicsView, QGraphicsScene, \
                            QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QCheckBox, QLabel
from custom_window_templates import AQDialog, AQComboBox, AQLabel, IP_AQLineEdit, Slave_ID_AQLineEdit
from custom_exception import Connect_err
import serial.tools.list_ports
from AQ_communication_func import is_valid_ip
from AQ_settings_func import save_current_text_value, save_combobox_current_state, load_last_text_value, \
                             load_last_combobox_state


class AQ_network_settings_frame(QFrame):
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

        self.network_settings_layout = AQ_network_settings_layout(event_manager, self, self.auto_load_settings)


class AQ_network_settings_layout(QVBoxLayout):
    def __init__(self, event_manager, parent, auto_load_settings=None):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.auto_load_settings = auto_load_settings
        self.setContentsMargins(0, 0, 0, 0)  # Устанавливаем отступы макета
        self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета


    # Создаем текстовую метку заголовка настроек соединения
        self.title_text = QLabel("Network parameters")
        self.title_text.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
        self.title_text.setFixedHeight(35)
        self.title_text.setFont(QFont("Verdana", 12))  # Задаем шрифт и размер
        self.title_text.setAlignment(Qt.AlignCenter)

    # Создаем текстовую метку выбора интерфейса
        self.interface_combo_box_label = AQLabel("Interface")

    # Создание комбо-бокса
        self.interface_combo_box = AQComboBox()
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
        self.ip_line_edit_label = AQLabel("IP Address")
        self.ip_line_edit = IP_AQLineEdit()
        self.ip_line_edit.setObjectName(self.parent.objectName() + "_" + "ip_line_edit")
        # Встановлюємо попередне обране значення, якщо воно існує
        if self.auto_load_settings is not None:
            load_last_text_value(self.auto_load_settings, self.ip_line_edit)

    # Создаем поле ввода Slave ID
        self.slave_id_line_edit_label = AQLabel("Slave ID")
        self.slave_id_line_edit = Slave_ID_AQLineEdit()
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
        self.find_btn.clicked.connect(lambda: self.event_manager.emit_event('Find_device'))

    # Додаємо все створені віджеті в порядку відображення
        self.addWidget(self.title_text)
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
