import csv
import os

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QStandardItem, QFont, QStandardItemModel, QColor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTableView, QLineEdit

from AQ_CustomWindowTemplates import AQ_Label
from AQ_DeviceInfoTableView import AQ_DeviceInfoTableView



class AQ_DeviceInfoManagerFrame(QFrame):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.device = device
        self.parent = parent
        self.status_file = None
        self.setStyleSheet("background-color: transparent;")

        # Читаэмо статус файл з поточного активного приладу
        self.read_status_file()
        data = self.parse_status_file(self.status_file)

        # Загрузка данных в модель
        self.general_info_model = self.load_data_to_general_info_model(data)
        self.param_model = self.load_data_to_param_model(data)



        # # Створюємо нову модель для відображення параметрів
        # self.param_list_table_model = self.create_param_list_for_view(self.device)
        #
        # # Створюємо нову модель для відображення інфо-бару
        # self.info_bar_table_model = self.create_info_list_for_view(self.device)
        #
        # # Створюємо обробник події створення csv файлу з параметрами
        # self.event_manager.register_event_handler('make_user_param_list_file', self.create_csv_file)
        #
        # Створюємо головний лейаут
        self.param_list_layout = AQ_DeviceInfoLayout(self.device, self.general_info_model,
                                                     self.param_model, self.event_manager, self)

    def parse_status_file(self, status_file):
        data_string = status_file.decode('ANSI')
        # Разделение строк по переводу строки
        data_rows = data_string.split('\n')
        data = []
        for row in data_rows:
            # Разделение записи на поля по символу ';'
            fields = row.split(';')
            data.append(fields)

        return data

    def load_data_to_general_info_model(self, data):
        model = QStandardItemModel(4, 2)
        for i, row in enumerate(data):
            # Додаємо тільки строки з другої по п'яту
            if i > 0 and i < 5:
                for j, item in enumerate(row):
                    if j < len(row) - 1:  # Убедимся, что мы не добавляем последнюю колонку
                        model.setItem(i - 1, j, QStandardItem(item))
            # Додаємо тільки строки з другої по п'яту
            if i > 4:
                break
        return model

    def load_data_to_param_model(self, data):
        model = QStandardItemModel(len(data) - 7, 2)  # Изменили второй аргумент
        for i, row in enumerate(data):
            # Додаємо тільки строки з п'ятої по передостанню
            if i > 4 and i < len(data) - 1:
                for j, cell_str in enumerate(row):
                    if j < len(row) - 1:  # Убедимся, что мы не добавляем последнюю колонку
                        if j == 0:
                            # Замінюємо UID на ім'я параметру
                            param_attributes = self.get_param_attributes_by_UID(int(cell_str, 16))
                            if param_attributes is not None:
                                name = param_attributes.get('name', 'err_name')
                                item = QStandardItem(name)
                                item.setData(param_attributes, Qt.UserRole)
                            else:
                                item = QStandardItem(cell_str)
                        else:
                            item = QStandardItem()
                            item.setData(cell_str, Qt.UserRole)
                        model.setItem(i - 5, j, QStandardItem(item))

        return model

    def read_status_file(self):
        self.status_file = self.device.read_status_file()

    def get_param_attributes_by_UID(self, uid):
        device_data = self.device.get_device_data()
        device_tree = device_data.get('device_tree', None)
        param_attributes = None
        if device_tree is not None:
            root = device_tree.invisibleRootItem()
            param_attributes = self.traverse_items_find_param_attributes_by_uid(root, uid)

        return param_attributes

    def traverse_items_find_param_attributes_by_uid(self, item, uid):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        param_attributes = self.traverse_items_find_param_attributes_by_uid(child_item, uid)
                        if param_attributes is not None:
                            return param_attributes
                    else:
                        if parameter_attributes.get('UID', 0) == uid:
                            return parameter_attributes
        # Якщо дійшли сюди, то співдпадінь немає
        return None


class AQ_DeviceInfoLayout(QVBoxLayout):
    def __init__(self, device, gen_info_table_model, param_table_model, event_manager, parent):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.device = device
        self.info_bar_table_model = gen_info_table_model
        self.param_table_model = param_table_model
        self.setContentsMargins(20, 5, 20, 20)  # Устанавливаем отступы макета
        self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета


    # Создаем текстовую метку заголовка
        self.first_label = QLabel('General information')
        self.first_label.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
        self.first_label.setFont(QFont("Segoe UI", 14))  # Задаем шрифт и размер
        self.first_label.setAlignment(Qt.AlignLeft)
        self.first_label.setFixedHeight(35)

    # Створюємо інфо-бар таблицю
        self.info_table_view = AQ_DeviceInfoTableView(self.info_bar_table_model, parent)

    # Создаем текстовую метку заголовка
        self.second_label = QLabel('Parameters')
        self.second_label.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
        self.second_label.setFont(QFont("Segoe UI", 14))  # Задаем шрифт и размер
        self.second_label.setAlignment(Qt.AlignLeft)
        self.second_label.setFixedHeight(35)

    # Створюємо таблицю з параметрами
        self.param_table_view = AQ_DeviceInfoTableView(self.param_table_model, parent)

    # Додаємо всі створені віджети в порядку відображення
        self.addWidget(self.first_label)
        self.addWidget(self.info_table_view)
        self.addWidget(self.second_label)
        self.addWidget(self.param_table_view)
