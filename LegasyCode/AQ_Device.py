import socket
import struct

from Crypto.Cipher import DES
from PySide6.QtCore import QObject
from pymodbus.client import serial
import serial.tools.list_ports

from AqBaseTreeItems import AqParamItem
from AQ_EventManager import AQ_EventManager
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AqIsValidIpFunc import is_valid_ip
from AQ_ParseFunc import swap_modbus_bytes, remove_empty_bytes, get_conteiners_count, get_containers_offset, \
    get_storage_container, parse_tree, reverse_modbus_registers


class AQ_Device_Config:
    #TODO: need to check device_ID (need add into devices too)
    def __init__(self):
        super().__init__()
        self.device_name = ""
        self.saved_param_list = []

class AQ_Device(QObject):

    def __init__(self, event_manager, address_tuple, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.local_event_manager = AQ_EventManager()
        self.device_name = None
        self.serial_number = None
        self.version = None
        self.address = None
        self.device_tree = None
        self.params_list = []
        self.password = None
        self.network_settings = address_tuple
        self.changed_param_stack = []
        self.update_param_stack = []
        self.client = self.create_client(address_tuple)
        self.client.open()
        self.device_data = self._read_device_data()
        if self.device_data != 'connect_err':
            default_prg = self.device_data.get('default_prg')
            if default_prg != 'decrypt_err':
                self.device_tree = self.__parse_default_prg(default_prg)
                if self.device_tree != 'parsing_err' and self.device_tree is not None \
                    and isinstance(self.device_tree, AQ_TreeItemModel):
                    self.device_tree.set_device(self)
                    self.device_data['status'] = 'ok'
                    self.device_data['device_tree'] = self.device_tree
                    self.__param_convert_tree_to_list()
                else:
                    self.device_data['status'] = 'data_error'
            else:
                self.device_data['status'] = 'data_error'
        else:
            self.device_data['status'] = 'connect_error'

        self._add_address_string_to_device_data(address_tuple)
        # self.device_data['network_info'] = self.make_network_info_list()

        # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C34694
        # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C34694ACFDF674DB57A4B9 - b'I will restart the device now!\x00\x00\x1e\x00\x00\x00Y\xdbZ^'
        # 0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C346945474D02935FDF5A2 - b'I will restart the device now!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        # hex_string = '0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C3E4AB'
        # hex_string = '0D403EAF19E7DA52CC2504F97AAA07A3E86C04B685C7EA96614844FC13C346945474D02935FDF5A2'
        # self.decrypt_data(b'superkey', bytes.fromhex(hex_string))
        self.local_event_manager.register_event_handler('add_param_to_changed_stack', self.add_param_to_changed_stack)
        self.local_event_manager.register_event_handler('add_param_to_update_stack', self.add_param_to_update_stack)

    def add_param_to_changed_stack(self, item):
        if item not in self.changed_param_stack:
            self.changed_param_stack.append(item)

    def add_param_to_update_stack(self, item):
        self.update_param_stack.append(item)

    def get_status(self):
        return self.device_data.get('status', None)

    #This is BULLSHIT
    #Внешние модули не должны парсить твоё инфо
    #Всё отдаём через интерфейс
    def get_device_data(self):
        return self.device_data

    def _add_address_string_to_device_data(self, address_tuple):
        interface = address_tuple[0]
        address = address_tuple[1]
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
        response = self.client.read_holding_registers(modbus_reg, reg_count)
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

    def create_client(self, address_tuple):
        interface = address_tuple[0]
        address = address_tuple[1]
        if interface == "Ethernet":
            if is_valid_ip(address):
                client = AQ_modbusTCP_connect(address)
                return client
        else:
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device
                    client = AQ_modbusRTU_connect(selected_port, 9600, address)
                    return client

        return None

    def _read_device_data(self):
        try:
            self.device_name = self._read_device_name()
            self.version = self._read_version()
            self.serial_number = self._read_serial_number()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            # "Ошибка при подключении к COM
            return 'connect_err'

        device_data = {}
        default_prg = self.__read_default_prg()
        device_data['device_name'] = self.device_name
        device_data['version'] = self.version
        device_data['serial_number'] = self.serial_number
        device_data['default_prg'] = default_prg
        return device_data


    def _read_device_name(self):
        # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
        text = self.__read_string(0xF000, 16)
        device_name = remove_empty_bytes(text)

        return device_name

    def _read_version(self):
        # Читаем 16 регистров начиная с адреса 0xF010 (soft version)
        text = self.__read_string(0xF010, 16)
        version = remove_empty_bytes(text)

        return version

    def _read_serial_number(self):
        # Читаем 16 регистров начиная с адреса 0xF086 (serial_number)
        text = self.__read_string(0xF086, 16)
        # Обрезаем длину до 20 символов
        text = text[:20]
        serial_number = remove_empty_bytes(text)

        return serial_number

    def __read_string(self, start, num):
        # Выполняем запрос
        response = self.client.read_holding_registers(start, num)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = swap_modbus_bytes(byte_array, num)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        return text


    def __read_default_prg(self):
        # Установка значений полей структуры
        file_number = 0xFFE0
        record_number = 0
        record_length = 124

        result = self.client.read_file_record(file_number, record_number, record_length)

        encrypt_res = result.records[0].record_data

        try:
            decrypt_res = self.__decrypt_data(encrypt_res)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        # Получаем длину default_prg зашитую во вторые 4 байта заголовка
        file_size = int.from_bytes((decrypt_res[4:8][::-1]), byteorder='big')
        # Получаем колличество необходимых запросов по 124 записи
        req_count = ((file_size // 2) // 124)
        if (file_size // 2) % 124 or file_size % 2:
            req_count = req_count + 1

        encrypt_file = bytearray()

        for i in range(req_count):
            record_number = i * 124  # Установка значения record_number

            result = self.client.read_file_record(file_number, record_number, record_length)
            encrypt_file += result.records[0].record_data
            # Обрезаем длину файла до вычитанной из заголовка, в конце последнего пакета мусор
            encrypt_file = encrypt_file[:file_size]

        try:
            # Перевірка на кратність 8 байтам, потрібно для DES
            if (len(encrypt_file) % 8) > 0:
                padding = 8 - (len(encrypt_file) % 8)
                encrypt_file = encrypt_file + bytes([padding] * padding)
            decrypt_file = self.__decrypt_data(encrypt_file)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        filename = 'default.prg'  # Имя файла с расширением .prg
        with open(filename, 'wb') as file:
            file.write(decrypt_file)

        return decrypt_file

    def __decrypt_data(self, encrypted_data):
        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.__get_key())
        decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные

        return decrypted_data

    def __encrypt_data(self, data):

        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.__get_key())

        # Шифрование данных
        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    def __get_hash(self):
        # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
        return b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524"

    def __get_key(self):
        if self.password == None:
            return b'superkey'
        else:
            return self.password

    def __parse_default_prg(self, default_prg):
        try:
            containers_count = get_conteiners_count(default_prg)
            containers_offset = get_containers_offset(default_prg)
            storage_container = get_storage_container(default_prg, containers_offset)
            device_tree = parse_tree(storage_container)
            return device_tree
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'parsing_err'

    def read_status_file(self):
        # Установка значений полей структуры
        file_number = 0x0001
        record_number = 0
        record_length = 124

        result = self.client.read_file_record(file_number, record_number, record_length)

        encrypt_res = result.records[0].record_data

        try:
            decrypt_res = self.__decrypt_data(encrypt_res)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        return decrypt_res

    def read_parameters(self, items=None):
        if items is None:
            self.read_all_parameters()
        elif isinstance(items, AqParamItem):
            self.__read_item(items)
        elif isinstance(items, list):
            for i in range(len(items)):
                self.__read_parameter(items[i])

        if len(self.update_param_stack) > 0:
            self.event_manager.emit_event('current_device_data_updated', self, self.update_param_stack)
            self.update_param_stack.clear()

    def read_all_parameters(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__read_item(child_item)

        return

    def __read_item(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__read_item(child_item)
        else:
            self.__read_parameter(item)

    def __read_parameter(self, item):
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        modbus_reg = param_attributes.get('modbus_reg', '')

        if param_type != '' and param_size != ''and modbus_reg != '':
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
            # Выполняем запрос
            response = self.client.read_holding_registers(modbus_reg, reg_count)
            # Конвертируем значения регистров в строку
            hex_string = ''.join(format(value, '04X') for value in response.registers)
            # Конвертируем строку в массив байт
            byte_array = bytes.fromhex(hex_string)
            if param_type == 'unsigned':
                if byte_size == 1:
                    param_value = struct.unpack('>H', byte_array)[0]
                elif byte_size == 2:
                    param_value = struct.unpack('>H', byte_array)[0]
                elif byte_size == 4:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]
                elif byte_size == 6:  # MAC address
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = byte_array  # struct.unpack('>I', byte_array)[0]
                elif byte_size == 8:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>Q', byte_array)[0]
            elif param_type == 'signed':
                if byte_size == 1:
                    param_value = struct.unpack('b', byte_array[1])[0]
                elif byte_size == 2:
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                elif byte_size == 4 or byte_size == 8:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
            elif param_type == 'string':
                byte_array = swap_modbus_bytes(byte_array, reg_count)
                # Расшифровуем в строку
                text = byte_array.decode('ANSI')
                param_value = remove_empty_bytes(text)
            elif param_type == 'enum':
                # костиль для enum з розміром два регістра
                if byte_size == 4:
                    param_value = struct.unpack('>I', byte_array)[0]
                else:
                    param_value = struct.unpack('>H', byte_array)[0]

            elif param_type == 'float':
                byte_array = swap_modbus_bytes(byte_array, reg_count)
                param_value = struct.unpack('f', byte_array)[0]
                param_value = round(param_value, 7)
            elif param_type == 'date_time':
                if byte_size == 4:
                    byte_array = reverse_modbus_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]

            item.data_from_network(param_value)
            item.synchronized = True

    # def read_all_parameters(self):
    #     root = self.device_tree.invisibleRootItem()
    #
    #     # self.wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
    #     # self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
    #     #
    #     # max_value = 100  # Максимальное значение для прогресс-бара
    #     # row_count = root.rowCount()
    #     # step_value = max_value // row_count
    #     for row in range(root.rowCount()):
    #         child_item = root.child(row)
    #         self.read_parameter(child_item)
    #         # if result == 'read_error':
    #         #     self.wait_widget.hide()
    #         #     self.wait_widget.deleteLater()
    #         #     return
    #         # self.wait_widget.progress_bar.setValue((row + 1) * step_value)
    #
    #     self.event_manager.emit_event('current_device_data_updated', self)
    #
    #     # self.wait_widget.progress_bar.setValue(max_value)
    #     # self.wait_widget.hide()
    #     # self.wait_widget.deleteLater()

    def write_parameters(self, items=None):
        if items is None:
            self.write_all_parameters()
        elif isinstance(items, AqParamItem):
            self.write_item(items)
        elif isinstance(items, list):
            for i in range(len(items)):
                self.write_parameter(items[i])

        if len(self.update_param_stack) > 0:
            self.event_manager.emit_event('current_device_data_updated', self, self.update_param_stack)
            self.update_param_stack.clear()

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
        if item in self.changed_param_stack:
            param_attributes = item.get_param_attributes()

            param_type = param_attributes.get('type', '')
            param_size = param_attributes.get('param_size', '')
            modbus_reg = param_attributes.get('modbus_reg', '')
            value = item.value
            if param_type != '' and param_size != '' and modbus_reg != '':
                if param_type == 'unsigned':
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
                elif param_type == 'signed':
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
                    if param_size == 4:
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

                try:
                    result = self.client.write_registers(modbus_reg, registers)
                    if result != 'modbus_error':
                        item.synchronized = True
                        # Якщо запис успішний, видаляємо параметр зі стеку змінених параметрів
                        removed_index = self.changed_param_stack.index(item)
                        self.changed_param_stack.pop(removed_index)
                except Exception as e:
                    print(f"Error occurred: {str(e)}")


    # def write_all_parameters(self):
    #     root = self.device_tree.invisibleRootItem()
    #
    #     # self.wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
    #     # self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
    #     #
    #     # max_value = 100  # Максимальное значение для прогресс-бара
    #     # row_count = root.rowCount()
    #     # step_value = max_value // row_count
    #     for row in range(root.rowCount()):
    #         child_item = root.child(row)
    #         self.write_parameter(child_item)
    #         # if result == 'read_error':
    #         #     self.wait_widget.hide()
    #         #     self.wait_widget.deleteLater()
    #         #     return
    #         # self.wait_widget.progress_bar.setValue((row + 1) * step_value)
    #
    #     self.event_manager.emit_event('current_device_data_written', self)

        # self.wait_widget.progress_bar.setValue(max_value)
        # self.wait_widget.hide()
        # self.wait_widget.deleteLater()

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
        encrypted_record_data = self.encrypt_data(record_data)
        self.client.write_file_record(file_number, record_number, record_length, encrypted_record_data)
        record_number = 20
        record_length = 0
        self.client.write_file_record(file_number, record_number, record_length, b'\x00')

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

