import csv
import os

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QStandardItem, QFont, QStandardItemModel, QColor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTableView, QLineEdit

from AQ_CustomWindowTemplates import AQ_Label
from AQ_DeviceInfoTableView import AQ_DeviceInfoTableView


# from AQ_ParamListTableView import AQ_ParamListTableView, AQ_ParamListInfoTableView
# from AQ_ParamListTableViewItemModel import AQ_TableViewItemModel
# from AQ_SettingsFunc import get_last_path, save_last_path


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
                for j, item in enumerate(row):
                    if j < len(row) - 1:  # Убедимся, что мы не добавляем последнюю колонку
                        if j == 0:
                            # Замінюємо UID на ім'я параметру
                            name = self.get_param_name_by_UID(int(item, 16))
                            if name is not None:
                                item = name
                        model.setItem(i - 5, j, QStandardItem(item))

        return model

    def read_status_file(self):
        self.status_file = self.device.read_status_file()

    def get_param_name_by_UID(self, uid):
        device_data = self.device.get_device_data()
        device_tree = device_data.get('device_tree', None)
        name = None
        if device_tree is not None:
            root = device_tree.invisibleRootItem()
            name = self.traverse_items_find_param_name_by_uid(root, uid)

        return name

    def traverse_items_find_param_name_by_uid(self, item, uid):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        param_name = self.traverse_items_find_param_name_by_uid(child_item, uid)
                        if param_name is not None:
                            return param_name
                    else:
                        if parameter_attributes.get('UID', 0) == uid:
                            param_name = parameter_attributes.get('name', None)
                            return param_name
        # Якщо дійшли сюди, то співдпадінь немає
        return None

    def create_new_row_for_table_view(self, item):
        parameter_attributes = item.data(Qt.UserRole)

    # Parameter
        name = parameter_attributes.get('name', 'err_name')
        param_item = QStandardItem(name)

    # Group
        catalog_item = item.parent()
        cat_attributes = catalog_item.data(Qt.UserRole)
        group_name = cat_attributes.get('name', 'err_name')
        group_item = QStandardItem(group_name)

    # Address (dec)
        reg_num_dec = parameter_attributes.get('modbus_reg', 'reg_error')
        adr_dec_item = QStandardItem(str(reg_num_dec))

    # Address (hex)
        if reg_num_dec != 'reg_error':
            reg_num_hex = '0x{:04X}'.format(reg_num_dec)
        else:
            reg_num_hex = 'reg_error'
        adr_hex_item = QStandardItem(reg_num_hex)

    # Number of registers
        param_size = parameter_attributes.get('param_size', None)
        param_type = parameter_attributes.get('type', None)
        if param_type == 'enum':
            if param_size > 16:
                reg_count = 2
                byte_size = 4
            else:
                reg_count = 1
                byte_size = 1
        else:
            byte_size = param_size
            if byte_size < 2:
                reg_count = 1
            else:
                reg_count = byte_size // 2
        reg_count_item = QStandardItem(str(reg_count))

    # Read function
        read_func = '3'
        read_func_item = QStandardItem(read_func)

    # Write function
        if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
            write_func = '16'
        else:
            write_func = '-'
        write_func_item = QStandardItem(write_func)

    # Data type
        if param_type == 'enum':
            max_limit = parameter_attributes.get('max_limit', None)
            if max_limit is not None:
                bit_size = max_limit + 1
            else:
                bit_size = parameter_attributes.get('param_size', None)
                if bit_size is not None:
                    bit_size = 2 ** bit_size - 1
                else:
                    bit_size = 'err'
        else:
            byte_size = parameter_attributes.get('param_size', None)
            if byte_size is not None:
                bit_size = byte_size * 8
            else:
                bit_size = 'err'
        data_type_item = QStandardItem(param_type + ' ' + str(bit_size))

        param_item.setData(parameter_attributes, Qt.UserRole)
        # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
        param_item.setFlags(param_item.flags() & ~Qt.ItemIsEditable)
        group_item.setFlags(group_item.flags() & ~Qt.ItemIsEditable)
        adr_dec_item.setFlags(adr_dec_item.flags() & ~Qt.ItemIsEditable)
        adr_hex_item.setFlags(adr_hex_item.flags() & ~Qt.ItemIsEditable)
        reg_count_item.setFlags(reg_count_item.flags() & ~Qt.ItemIsEditable)
        read_func_item.setFlags(read_func_item.flags() & ~Qt.ItemIsEditable)
        write_func_item.setFlags(write_func_item.flags() & ~Qt.ItemIsEditable)
        data_type_item.setFlags(data_type_item.flags() & ~Qt.ItemIsEditable)

        return [param_item, group_item, adr_dec_item, adr_hex_item,
                reg_count_item, read_func_item, write_func_item, data_type_item]


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
