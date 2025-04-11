import csv
import os

from PySide2.QtCore import Qt, QSettings
from PySide2.QtGui import QStandardItem, QFont, QStandardItemModel, QColor
from PySide2.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit

from LegasyCode.AQ_Device import AQ_Device
from AQ_CustomWindowTemplates import AQ_Label
from AQ_ParamListTableView import AQ_ParamListTableView, AQ_ParamListInfoTableView
from AQ_ParamListTableViewItemModel import AQ_TableViewItemModel
from AqSettingsFunc import get_last_path, save_last_path


class AQ_ParamListManagerFrame(QFrame):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.device = device
        self.parent = parent
        self.setStyleSheet("background-color: transparent;")

        try:
            # Получаем текущий рабочий каталог (папку проекта)
            project_path = os.getcwd()
            # Объединяем путь к папке проекта с именем файла настроек
            settings_path = os.path.join(project_path, "auto_load_settings.ini")
            # Используем полученный путь в QSettings
            self.auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
        except:
            self.auto_load_settings = None
            print('File "auto_load_settings.ini" not found')

        # Створюємо нову модель для відображення параметрів
        self.param_list_table_model = self.create_param_list_for_view(self.device)

        # Створюємо нову модель для відображення інфо-бару
        self.info_bar_table_model = self.create_info_list_for_view(self.device)

        # Створюємо обробник події створення csv файлу з параметрами
        self.event_manager.register_event_handler('make_user_param_list_file', self.create_csv_file)

        # Створюємо головний лейаут
        self.param_list_layout = AQ_ParamListLayout(self.device, self.param_list_table_model,
                                                    self.info_bar_table_model, self.event_manager, self)

    def create_param_list_for_view(self, device: AQ_Device):
        device_data = device.get_device_data()
        device_tree = device_data.get('device_tree', None)
        if device_tree is not None:
            table_model_for_view = AQ_TableViewItemModel(device, self.event_manager)
            table_model_for_view.setColumnCount(8)
            table_model_for_view.setHorizontalHeaderLabels(
                ["Parameter", "Group", "Address (dec)", "Address (hex)", "Number of registers", "Read function",
                 "Write function", "Data type"])
            donor_root_item = device_tree.invisibleRootItem()
            new_root_item = table_model_for_view.invisibleRootItem()
            self.traverse_items_create_new_table_model_for_view(donor_root_item, new_root_item)
            return table_model_for_view

    def create_info_list_for_view(self, device):
        device_data = device.get_device_data()
        network_info_list = device_data.get('network_info', None)
        if network_info_list is not None:
            info_table_model_for_view = QStandardItemModel()
            info_table_model_for_view.setColumnCount(1)
            new_root_item = info_table_model_for_view.invisibleRootItem()
            for i in range(len(network_info_list)):
                item_row = QStandardItem(network_info_list[i])
                item_row.setFlags(item_row.flags() & ~Qt.ItemIsEditable)
                new_root_item.appendRow(item_row)

            return info_table_model_for_view

    def traverse_items_create_new_table_model_for_view(self, item, new_item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        self.traverse_items_create_new_table_model_for_view(child_item, new_item)
                    else:
                        new_item.appendRow(self.create_new_row_for_table_view(child_item))

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

    def create_csv_file(self):
        device_data = self.device.get_device_data()
        device_name = device_data.get('device_name', 'err_name')
        serial_number = device_data.get('serial_number', 'err_serial_number')
        dev_name = device_name + ' SN' + serial_number

        # Сохраняем данные в файл CSV
        def_name = 'Parameters available over network ' + dev_name + '.csv'
        # Начальный путь для диалога
        initial_path = get_last_path(self.auto_load_settings, 'param_list_csv_path')
        if initial_path == '':
            initial_path = "C:/"
        self.file_dialog = QFileDialog(self)
        options = self.file_dialog.options()
        # options |= self.file_dialog.DontUseNativeDialog

        # Открываем диалог для выбора файла и места сохранения
        filename, _ = self.file_dialog.getSaveFileName(self.parent, "Save parameters as CSV", initial_path + '/' +
                                                       def_name, "CSV Files (*.csv);;All Files (*)", options=options)
        if filename != '':
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')

                # Записуємо дані з моделі з мережевою інформацією
                for row in range(self.info_bar_table_model.rowCount()):
                    row_data = [self.info_bar_table_model.item(row, col).text()
                                for col in range(self.info_bar_table_model.columnCount())]
                    writer.writerow(row_data)

                # Записываем заголовки (названия колонок)
                headers = [self.param_list_table_model.horizontalHeaderItem(col).text()
                           for col in range(self.param_list_table_model.columnCount())]
                writer.writerow(headers)

                # Записуємо дані з моделі з параметрами
                for row in range(self.param_list_table_model.rowCount()):
                    row_data = [self.param_list_table_model.item(row, col).text()
                                for col in range(self.param_list_table_model.columnCount())]
                    writer.writerow(row_data)
            # Извлекаем путь к каталогу
            directory_path = os.path.dirname(filename)
            save_last_path(self.auto_load_settings, 'param_list_csv_path', directory_path)


class AQ_ParamListLayout(QVBoxLayout):
    def __init__(self, device, param_table_model, info_bar_table_model, event_manager, parent):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.device = device
        self.info_bar_table_model = info_bar_table_model
        self.param_table_model = param_table_model
        self.setContentsMargins(20, 5, 20, 20)  # Устанавливаем отступы макета
        self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета


    # Создаем текстовую метку заголовка настроек соединения
        device_data = self.device.get_device_data()
        device_name = device_data.get('device_name', 'err_name')
        serial_number = device_data.get('serial_number', 'err_serial_number')
        self.name_label = QLabel(device_name + ' S/N' + serial_number)
        self.name_label.setStyleSheet("color: #D0D0D0; border-top:transparent; border-bottom: 1px solid #5bb192;")
        # self.name_label.setFixedHeight(35)
        self.name_label.setFont(QFont("Segoe UI", 14))  # Задаем шрифт и размер
        self.name_label.setAlignment(Qt.AlignLeft)

    # Створюємо інфо-бар таблицю
        self.info_table_view = AQ_ParamListInfoTableView(self.info_bar_table_model, parent)

    # Створюємо поле для пошуку
    #     self.search_box = AQ_ParamListSearchLine(parent)
    #     self.search_box.textChanged.connect(self.search)

    # Створюємо таблицю з параметрами
        self.param_table_view = AQ_ParamListTableView(self.param_table_model, parent)

    # Створюємо кнопку збереження параметрів у файл
        self.btn_save_as_file = AQ_ParamListSaveButton(self.event_manager, parent)

    # Додаємо всі створені віджети в порядку відображення
        self.addWidget(self.name_label)
        self.addWidget(self.info_table_view)
        # self.addWidget(self.search_box)
        self.addWidget(self.param_table_view)
        self.addWidget(self.btn_save_as_file)

    def search(self):
        search_text = self.search_box.text()
        if not search_text:
            self.reset_highlight()
            return

        for row in range(self.param_table_model.rowCount()):
            for col in range(self.param_table_model.columnCount()):
                item = self.param_table_model.item(row, col)
                if item is not None:
                    item.setBackground(QColor('white'))  # Reset previous highlighting

                index = self.param_table_model.index(row, col)
                text = index.data(Qt.DisplayRole)

                if text and search_text.lower() in text.lower():
                    item.setBackground(QColor('yellow'))  # Highlight matches

    def reset_highlight(self):
        for row in range(self.param_table_model.rowCount()):
            for col in range(self.param_table_model.columnCount()):
                item = self.param_table_model.item(row, col)
                if item is not None:
                    item.setBackground(QColor('white'))  # Reset highlighting


class AQ_CurrentIpParamsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.cur_ip_label = AQ_Label("Current IP:")
        self.cur_mask_label = AQ_Label("Current mask:")
        self.cur_gate_label = AQ_Label("Current gate:")
        self.addWidget(self.cur_ip_label)
        self.addWidget(self.cur_mask_label)
        self.addWidget(self.cur_gate_label)

class AQ_ProtocolParamsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.protocol_label = AQ_Label("Protocol: Modbus TCP")
        self.byte_order_label = AQ_Label("Byte order: Most significant byte first")
        self.reg_order_label = AQ_Label("Register order: Least significant register first")
        self.addWidget(self.protocol_label)
        self.addWidget(self.byte_order_label)
        self.addWidget(self.reg_order_label)

class AQ_InfoBarLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.ip_param_layout = AQ_CurrentIpParamsLayout()
        self.protocol_param_layout = AQ_ProtocolParamsLayout()
        self.addLayout(self.ip_param_layout)
        self.addLayout(self.protocol_param_layout)


class AQ_ParamListSaveButton(QPushButton):
    def __init__(self, event_manager, parent=None):
        text = 'Save as file (csv)'
        super().__init__(text, parent)
        self.event_manager = event_manager
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setFixedSize(150, 35)
        self.clicked.connect(lambda: self.event_manager.emit_event('make_user_param_list_file'))
        self.setStyleSheet("""
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

        self.show()

class AQ_ParamListSearchLine(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText('Search...')
        self.setStyleSheet('color: #D0D0D0; border: none;')
