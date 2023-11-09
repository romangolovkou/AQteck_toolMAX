import asyncio
import csv
import socket
import struct
import threading

from Crypto.Cipher import DES
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QWidget, QFrame, QLabel
from pymodbus.client import serial
import serial.tools.list_ports

from AQ_CustomTreeItems import AQ_ParamItem, AQ_CatalogItem
from AQ_Device import AQ_Device
from AQ_EventManager import AQ_EventManager
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AQ_IsValidIpFunc import is_valid_ip
from AQ_Connect import AQ_modbusTCP_connect, AQ_modbusRTU_connect, AQ_COM_Connect_settings, AQ_IP_Connect_settings
from AQ_ParseFunc import swap_modbus_bytes, remove_empty_bytes, get_conteiners_count, get_containers_offset, \
    get_storage_container, parse_tree, reverse_modbus_registers, get_item_by_type
from AQ_CustomWindowTemplates import AQ_wait_progress_bar_widget
from AqParser import parse_config


class AQ_Device_Config:
    #TODO: need to check device_ID (need add into devices too)
    def __init__(self):
        super().__init__()
        self.device_name = ""
        self.saved_param_list = []


class AQ_Device110China(AQ_Device):
    def __init__(self, event_manager, connect, network_settings, parent=None):
        # super().__init__(event_manager, address_tuple, parent)
        self.event_manager = event_manager
        self.local_event_manager = AQ_EventManager()
        self.packer = AQ_Device_110chinaPacker()
        self.device_name = None
        self.serial_number = None
        self.version = None
        self.address = None
        self.device_tree = None
        self.params_list = []
        self.password = None
        self.request_count = list()
        self.network_settings = network_settings
        # self.changed_param_stack = []
        self.update_param_stack = []
        self.stack_to_read = []
        self.stack_to_write = []
        self.read_error_flag = False
        self.write_error_flag = False
        self.connect = connect
        self.params_inited = False
        self.core_cv = threading.Condition()
        # self.event_manager.emit_event('create_new_connect', self)
        if self.connect is not None and self.connect.open():
            self.device_data = self.read_device_data()
        else:
            self.device_data = 'connect_err'
        if self.device_data != 'connect_err':
            device_config = self.device_data.get('device_config')
            if device_config != 'decrypt_err':
                # self.device_tree = self.parse_device_config(device_config)
                self.device_tree = parse_config(device_config)
                if self.device_tree != 'parsing_err' and self.device_tree is not None \
                    and isinstance(self.device_tree, AQ_TreeItemModel):
                    self.device_tree.set_device(self)
                    self.device_data['status'] = 'ok'
                    self.device_data['device_tree'] = self.device_tree
                    self.__param_convert_tree_to_list()
                else:
                    self.device_data['status'] = 'data_error'
                    self.connect.close()
            else:
                self.device_data['status'] = 'data_error'
                self.connect.close()
        else:
            self.device_data['status'] = 'connect_error'
            self.connect.close()

        if self.device_data['status'] != 'connect_error':

            self.add_address_string_to_device_data(network_settings)
            # self.device_data['network_info'] = self.make_network_info_list()

            # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C34694
            # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C34694ACFDF674DB57A4B9 - b'I will restart the device now!\x00\x00\x1e\x00\x00\x00Y\xdbZ^'
            # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C346945474D02935FDF5A2 - b'I will restart the device now!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            # hex_string = '0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C3E4AB'
            # hex_string = '0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C346945474D02935FDF5A2'
            # self.decrypt_data(b'superkey', bytes.fromhex(hex_string))
            # self.local_event_manager.register_event_handler('add_param_to_changed_stack', self.add_param_to_changed_stack)
            self.local_event_manager.register_event_handler('add_param_to_update_stack', self.add_param_to_update_stack)
            self.event_manager.register_event_handler('current_device_data_updated', self.read_complete)

    def init_parameters(self):
        for i in self.params_list:
            self.read_parameters(i)
            with self.core_cv:
                self.core_cv.wait()
                # TODO: Установить значение по умолчанию или 0

        return True

    def read_complete(self, device, item):
        if device == self:
            with self.core_cv:
                self.core_cv.notify()

    # def add_param_to_changed_stack(self, item):
    #     if item not in self.changed_param_stack:
    #         self.changed_param_stack.append(item)

    def add_param_to_update_stack(self, item):
        if item not in self.update_param_stack:
            self.update_param_stack.append(item)
            if len(self.update_param_stack) == self.request_count[0]:
                self.request_count.pop(0)
                self.event_manager.emit_event('current_device_data_updated', self, self.update_param_stack)
                self.update_param_stack.clear()

                # # Якщо запис успішний, видаляємо параметр зі стеку змінених параметрів
                # removed_index = self.changed_param_stack.index(item)
                # self.changed_param_stack.pop(removed_index)

    def get_device_status(self):
        return self.device_data.get('status', None)

    def get_device_data(self):
        return self.device_data

    def get_connect_settings(self, network_settings):
        if network_settings.get('ip', False):
            ip = network_settings.get('ip', None)
            if ip is not None and is_valid_ip(ip):
                self.connect_settings = AQ_IP_Connect_settings(_ip=ip)
            else:
                self.connect_settings = None
        elif network_settings.get('boudrate', False):
            interface = network_settings.get('interface', None)
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device

            boudrate = network_settings.get('boudrate', None)
            parity = network_settings.get('parity', None)
            stopbits = network_settings.get('stopbits', None)

            if selected_port is not None and \
                    boudrate is not None and \
                    parity is not None and \
                    stopbits is not None:
                self.connect_settings = AQ_COM_Connect_settings(_port=selected_port,
                                                                _baudrate=boudrate,
                                                                _parity=parity,
                                                                _stopbits=stopbits)
            else:
                self.connect_settings = None

    def add_address_string_to_device_data(self, network_settings):
        interface = network_settings.get('interface', None)
        address = network_settings.get('address', None)
        if interface == "Ethernet":
            if is_valid_ip(address):
                self.device_data['address'] = str(address)
        else:
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device
                    self.device_data['address'] = str(address) + ' (' + str(selected_port) + ')'

        return None

    def make_network_info_list(self):
        # Выполняем запрос
        modbus_reg = 26  #у всіх приборах на кс2 для поточного IP повинен буди однаковий
        reg_count = 2
        response = self.connect.read_holding_registers(modbus_reg, reg_count)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = reverse_modbus_registers(byte_array)
        value = struct.unpack('>I', byte_array)[0]
        ip = socket.inet_ntoa(struct.pack('!L', value))
        if not is_valid_ip(ip):
            ip = ''

        info_list = ['Current IP: ' + ip, 'Protocol: ModbusTCP',
                     'Byte order: Most significant byte first',
                     'Registers order: Least significant register first']
        return info_list

    # def create_client(self, address_tuple):
    #     interface = address_tuple[0]
    #     address = address_tuple[1]
    #     if interface == "Ethernet":
    #         if is_valid_ip(address):
    #             client = AQ_modbusTCP_connect(address)
    #             return client
    #     else:
    #         # Получаем список доступных COM-портов
    #         com_ports = serial.tools.list_ports.comports()
    #         for port in com_ports:
    #             if port.description == interface:
    #                 selected_port = port.device
    #                 boudrate = address_tuple[3]
    #                 parity = address_tuple[4][:1]
    #                 stopbits = address_tuple[5]
    #                 client = AQ_modbusRTU_connect(selected_port, boudrate, parity, stopbits, address)
    #                 return client
    #
    #     return None

    def read_device_data(self):
        try:
            self.device_name = self.read_device_name()
            self.read_slave_id()
        #     self.version = self.read_version()
        #     self.serial_number = self.read_serial_number()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            # "Ошибка при подключении к COM
            return 'connect_err'

        device_data = {}
        device_config = self.read_configuration()
        device_data['device_name'] = self.device_name
        device_data['version'] = self.version
        device_data['serial_number'] = self.serial_number
        device_data['device_config'] = device_config
        return device_data


    def read_device_name(self):
        file_path = '110_device_conf/' + self.network_settings.get('device', None)
        data = []
        with open(file_path, 'r', newline='\n') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # Добавляем имена из каждой ячейки строки в список
                data.append(row[0])
                # Тут нас цікавить тільки перша строка файлу
                break

        # Разделение записи на поля по символу ';'
        fields = data[0].split(';')

        device_name = fields[0]

        return device_name

    def read_version(self):
        # Читаем 16 регистров начиная с адреса 0xF010 (soft version)
        start_address = 0xF010
        register_count = 16
        # Выполняем запрос
        response = self.connect.read_holding_registers(start_address, register_count)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = swap_modbus_bytes(byte_array, register_count)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        version = remove_empty_bytes(text)

        return version

    def read_serial_number(self):
        # Читаем 16 регистров начиная с адреса 0xF086 (serial_number)
        start_address = 0xF086
        register_count = 16
        # Выполняем запрос
        response = self.connect.read_holding_registers(start_address, register_count)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = swap_modbus_bytes(byte_array, register_count)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        # Обрезаем дляну до 20 символов
        text = text[:20]
        serial_number = remove_empty_bytes(text)

        return serial_number

    def read_slave_id(self):
        # Читаем 16 регистров начиная с адреса 0xF086 (serial_number)
        start_address = 100
        register_count = 1
        func = 3
        # Выполняем запрос
        response = self.connect.client.read_holding_registers(start_address, register_count, self.connect.slave_id)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        param_value = struct.unpack('>H', byte_array)[0]

        return param_value

    def connect_callback(self, response):
        self.response = response

    def read_configuration(self):
        file_path = '110_device_conf/' + self.network_settings.get('device', None)
        data = []
        count = 0
        with open(file_path, 'r', newline='\n') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # Добавляем имена из каждой ячейки строки в список
                # Перші дві строки пропускаємо
                count += 1
                if count > 2:
                    data.append(row[0])

        return data

    def decrypt_data(self, iv, encrypted_data):
        # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
        key = b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524

        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные

        return decrypted_data

    def encrypt_data(self, iv, data):
        # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
        key = b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524

        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(key, DES.MODE_CBC, iv)

        # Шифрование данных
        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    def parse_device_config(self, device_config):
        try:
            # Створюємо список імен каталогів
            catalogs_name_set = set()
            for i in range(len(device_config)):
                config_string = device_config[i]
                # Разделение записи на поля по символу ';'
                fields = config_string.split(';')
                catalogs_name_set.add(fields[1])
            # Сортировка элементов сета в алфавитном порядке
            sorted_list = sorted(catalogs_name_set)

            # створюємо список з каталог-ітемами
            catalogs = []
            for i in range(len(sorted_list)):
                catalog_item = AQ_CatalogItem(sorted_list[i])
                param_attributes = {}
                param_attributes['name'] = sorted_list[i]
                param_attributes['is_catalog'] = 1
                catalog_item.setData(param_attributes, Qt.UserRole)
                catalogs.append(catalog_item)

            # Додаємо до каталогів відповідні параметр-ітеми
            for i in range(len(catalogs)):
                cat_name = catalogs[i].text()
                for j in range(len(device_config)):
                    config_string = device_config[j]
                    # Разделение записи на поля по символу ';'
                    fields = config_string.split(';')
                    if fields[1] == cat_name:
                        param_attributes = {}
                        parameter_name = fields[0]
                        param_attributes['name'] = parameter_name
                        param_attributes['modbus_reg'] = int(fields[2])
                        param_attributes['read_func'] = int(fields[4])
                        if fields[5] == '-':
                            param_attributes['R_Only'] = 1
                            param_attributes['W_Only'] = 0
                        else:
                            param_attributes['write_func'] = int(fields[5])

                        if fields[7] != '' and fields[7] != '-':
                            param_attributes['min_limit'] = int(fields[7])
                        if fields[8] != '' and fields[8] != '-':
                            param_attributes['max_limit'] = int(fields[8])
                        param_attributes['unit'] = fields[9]
                        parts = fields[6].split(' ')
                        param_type = parts[0]
                        if param_type == 'enum' or param_type == 'string':
                            param_size = int(parts[1])
                        else:
                            param_size = int(parts[1]) // 8
                        param_attributes['type'] = param_type
                        param_attributes['param_size'] = param_size

                        if fields[10] != '' and fields[10] != '-':
                            if param_type == 'float':
                                param_attributes['def_value'] = float(fields[10])
                            else:
                                param_attributes['def_value'] = int(fields[10])

                        if param_type == 'enum' or param_type == 'float_enum':
                            enum_strings = fields[11].split('/')

                            enum_str_dict = {}
                            for row in range(len(enum_strings)):
                                string_key = enum_strings[row].split('=')
                                enum_str_dict[int(string_key[0])] = string_key[1]

                            param_attributes['enum_strings'] = enum_str_dict

                        if param_type == 'signed_to_float' or param_type == 'unsigned_to_float':
                            if fields[11] != '':
                                enum_strings = fields[11].split('/')

                                enum_str_dict = {}
                                for row in range(len(enum_strings)):
                                    string_key = enum_strings[row].split('=')
                                    enum_str_dict[int(string_key[0])] = string_key[1]

                                param_attributes['enum_strings'] = enum_str_dict

                            multiply = float(fields[12])
                            param_attributes['multiply'] = multiply

                        param_item = get_item_by_type(param_attributes.get('type', ''), parameter_name, self.packer)
                        param_item.setData(param_attributes, Qt.UserRole)
                        catalogs[i].appendRow(param_item)

            device_tree = AQ_TreeItemModel()
            root = device_tree.invisibleRootItem()
            for row in range(len(catalogs)):
                root.appendRow(catalogs[row])
            return device_tree
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'parsing_err'

    def read_status_file(self):
        # Установка значений полей структуры
        file_number = 0x0001
        record_number = 0
        record_length = 124

        result = self.connect.read_file_record(file_number, record_number, record_length)

        encrypt_res = result.records[0].record_data

        try:
            decrypt_res = self.decrypt_data(b'superkey', encrypt_res)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        return decrypt_res

    def read_parameters(self, items=None):
        if len(self.request_count) == 0:
            if items is None:
                self.read_all_parameters()
            elif isinstance(items, AQ_ParamItem):
                self.read_item(items)
            elif isinstance(items, list):
                for i in range(len(items)):
                    self.read_parameter(items[i])

            self.request_count.append(len(self.stack_to_read))

            self.connect.createParamRequest(self.stack_to_read)

    def read_all_parameters(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.read_item(child_item)

    def read_item(self,  item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.read_item(child_item)
        else:
            self.read_parameter(item)

    def read_parameter(self, item):
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        modbus_reg = param_attributes.get('modbus_reg', '')
        read_func = param_attributes.get('read_func', '')

        if param_type != '' and param_size != '' and modbus_reg != '':
            if param_type == 'enum':
                if param_size > 16:
                    reg_count = 2
                else:
                    reg_count = 1
            else:
                byte_size = param_size
                if byte_size < 2:
                    reg_count = 1
                else:
                    reg_count = byte_size // 2
            # Формируем запрос
            self.stack_to_read.append({'method': self.connect.read_param, 'func': read_func, 'start': modbus_reg,
                                         'count': reg_count, 'callback': item.data_from_network})

        # if self.read_error_flag is True:
        #     self.read_error_flag = False
        #     self.event_manager.emit_event('param_read_error')
        #     return 'read_err'
        #
        # return 'ok'

    def write_parameters(self, items=None):
        if len(self.request_count) == 0:
            if items is None:
                self.write_all_parameters()
            elif isinstance(items, AQ_ParamItem):
                self.write_item(items)
            elif isinstance(items, list):
                for i in range(len(items)):
                    self.write_parameter(items[i])

            self.request_count.append(len(self.stack_to_write))

            self.connect.createParamRequest(self.stack_to_write)

        # if len(self.update_param_stack) > 0:
        #     self.event_manager.emit_event('current_device_data_updated', self, self.update_param_stack)
        #     self.update_param_stack.clear()

    def write_all_parameters(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.write_item(child_item)

    def write_item(self,  item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.write_item(child_item)
        else:
            self.write_parameter(item)

    def write_parameter(self, item):
        # if item in self.changed_param_stack:
        if item.get_status() == 'changed':
            param_attributes = item.get_param_attributes()

            modbus_reg = param_attributes.get('modbus_reg', '')
            write_func = param_attributes.get('write_func', '')
            data = item.data_for_network()

            self.stack_to_write.append({'method': self.connect.write_param, 'func': write_func, 'start': modbus_reg,
                                       'data': data, 'callback': item.confirm_writing})

        # if self.write_error_flag is True:
        #     self.write_error_flag = False
        #     self.event_manager.emit_event('param_write_error')
        #     return 'write_err'
        #
        # return 'ok'




    def restart_device(self):
        # "I will restart the device now!"
        file_number = 0xDEAD
        record_number = 0
        record_length = 20
        text = "I will restart the device now!"
        record_data = text.encode('UTF-8')
        # Выравнивание длины исходных данных
        pad_length = 8 - (len(record_data) % 8)
        padded_data = record_data + bytes([0x00] * pad_length)
        strange_tail = b'\x1e\x00\x00\x00Y\xdbZ^'
        record_data = padded_data + strange_tail
        encrypted_record_data = self.encrypt_data(b'superkey', record_data)
        self.connect.write_file_record(file_number, record_number, record_length, encrypted_record_data)
        record_number = 20
        record_length = 0
        self.connect.write_file_record(file_number, record_number, record_length, b'\x00')

    def __param_convert_tree_to_list(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__convert_tree_branch_to_list(child_item)

    def __convert_tree_branch_to_list(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__convert_tree_branch_to_list(child_item)
        else:
            self.params_list.append(item)

    def save_config(self):
        config = AQ_Device_Config()
        config.device_name = self.device_name

        for devParam in self.params_list:
            param_attributes = devParam.get_param_attributes()
            config.saved_param_list.append({'UID': param_attributes.get('UID', 0), 'modbus_reg': param_attributes.get('modbus_reg', 0), 'value': devParam.value})

        return config

    def load_config(self, config: AQ_Device_Config):
        if self.device_name != config.device_name:
            self.event_manager.emit_event('load_cfg_error')
            return NotImplementedError
            #TODO: need generate custom exception or generate event to display error message

        for cfgParam in config.saved_param_list:
            for devParam in self.params_list:
                param_attributes = devParam.get_param_attributes()
                modbusReg = param_attributes.get('modbus_reg', 0)
                if cfgParam['modbus_reg'] == modbusReg:
                    devParam.value = cfgParam['value']
        #TODO: optimize this algorithm

        self.event_manager.emit_event('current_device_data_updated', self, self.changed_param_stack)


class AQ_Device_110chinaPacker:
    def __init__(self):
        super().__init__()

    def pack(self, item, value):
        param_value = None
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        read_func = param_attributes.get('read_func', '')
        if param_type != '' and param_size != '':
            write_func = param_attributes.get('write_func', None)
            if write_func == 16:
                if param_type == 'unsigned' or param_type == 'unsigned_to_float':
                    if param_size == 1:
                        packed_data = struct.pack('H', value)
                    elif param_size == 2:
                        packed_data = struct.pack('H', value)
                    elif param_size == 4:
                        packed_data = struct.pack('I', value)
                    elif param_size == 6:  # MAC address
                        packed_data = struct.pack('H', value)
                    elif param_size == 8:
                        packed_data = struct.pack('Q', value)
                    # Разбиваем упакованные данные на 16-битные значения (2 байта)
                    registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
                elif param_type == 'signed' or param_type == 'signed_to_float':
                    if param_size == 1:
                        packed_data = struct.pack('h', value)
                    elif param_size == 2:
                        packed_data = struct.pack('h', value)
                    elif param_size == 4:
                        packed_data = struct.pack('i', value)
                    elif param_size == 8:
                        packed_data = struct.pack('q', value)
                    # Разбиваем упакованные данные на 16-битные значения (2 байта)
                    registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
                elif param_type == 'string':
                    text_bytes = value.encode('ANSI')
                    # Добавляем нулевой байт в конец, если длина списка не кратна 2
                    if len(text_bytes) % 2 != 0:
                        text_bytes += b'\x00'
                    registers = [struct.unpack('H', text_bytes[i:i + 2])[0] for i in range(0, len(text_bytes), 2)]
                elif param_type == 'enum':
                    # костиль для enum з розміром два регістра
                    if param_size >= 16:
                        packed_data = struct.pack('I', value)
                        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
                    else:
                        packed_data = struct.pack('H', value)
                        registers = struct.unpack('H', packed_data)
                elif param_type == 'float':
                    if param_size == 4:
                        floats = struct.pack('f', value)
                        registers = struct.unpack('HH', floats)  # Возвращает два short int значения
                    elif param_size == 8:
                        floats_doubble = struct.pack('d', value)
                        registers = struct.unpack('HHHH', floats_doubble)  # Возвращает два short int значения
                # elif param_type == 'date_time':
                #     if byte_size == 4:
                #         byte_array = reverse_modbus_registers(byte_array)
                #         param_value = struct.unpack('>I', byte_array)[0]
                return  registers

            elif write_func == 5:
                if value == 1:
                    data = True
                else:
                    data = False
                return data

            elif write_func == 6:
                return value

    def unpack(self, item, data):
        param_value = None
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        read_func = param_attributes.get('read_func', '')
        if read_func == 3:
            # Конвертируем значения регистров в строку
            hex_string = ''.join(format(value, '04X') for value in data.registers)
            # Конвертируем строку в массив байт
            byte_array = bytes.fromhex(hex_string)
            if param_type == 'unsigned' or param_type == 'unsigned_to_float':
                if param_size == 1:
                    param_value = struct.unpack('>H', byte_array)[0]
                elif param_size == 2:
                    param_value = struct.unpack('>H', byte_array)[0]
                elif param_size == 4:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]
                elif param_size == 6:  # MAC address
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = byte_array  # struct.unpack('>I', byte_array)[0]
                elif param_size == 8:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>Q', byte_array)[0]
            elif param_type == 'signed' or param_type == 'signed_to_float':
                if param_size == 1:
                    # param_value = struct.unpack('>b', byte_array[1])[0]
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                elif param_size == 2:
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                elif param_size == 4 or param_size == 8:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
            elif param_type == 'string':
                reg_count = param_size // 2
                byte_array = swap_modbus_bytes(byte_array, reg_count)
                # Расшифровуем в строку
                text = byte_array.decode('ANSI')
                param_value = remove_empty_bytes(text)
            elif param_type == 'enum':
                if param_size > 16:
                    byte_size = 4
                else:
                    byte_size = 1
                # костиль для enum з розміром два регістра
                if byte_size == 4:
                    param_value = struct.unpack('>I', byte_array)[0]
                else:
                    param_value = struct.unpack('>H', byte_array)[0]

            elif param_type == 'float':
                reg_count = param_size // 2
                byte_array = swap_modbus_bytes(byte_array, reg_count)
                param_value = struct.unpack('>f', byte_array)[0]
                param_value = round(param_value, 7)
            elif param_type == 'date_time':
                if param_size == 4:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]
        elif read_func == 2 or read_func == 1:
            if data.bits[0] is True:
                param_value = 1
            else:
                param_value = 0

        return param_value
