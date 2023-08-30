from PyQt5.QtCore import QObject
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from pymodbus.client import serial
import serial.tools.list_ports
from AQ_communication_func import is_valid_ip, decrypt_data
from AQ_connect import AQ_modbusTCP_connect, AQ_modbusRTU_connect
from AQ_parse_func import swap_modbus_bytes, remove_empty_bytes, get_conteiners_count, get_containers_offset, \
                          get_storage_container, parse_tree


class AQ_Device(QObject):
    def __init__(self, event_manager, address_tuple, parent=None):
        super().__init__()
        self.event_manager = event_manager
        self.device_name = None
        self.serial_number = None
        self.version = None
        self.address = None
        self.device_tree = None
        self.address_tuple = address_tuple
        self.client = self.create_client(address_tuple)
        self.client.open()
        self.device_data = self.read_device_data()
        if self.device_data != 'connect_err':
            default_prg = self.device_data.get('default_prg')
            if default_prg != 'decrypt_err':
                self.device_tree = self.parse_default_prg(default_prg)
                if self.device_tree != 'parsing_err' and self.device_tree is not None \
                    and isinstance(self.device_tree, QStandardItemModel):
                    self.device_data['status'] = 'ok'
                else:
                    self.device_data['status'] = 'data_error'
            else:
                self.device_data['status'] = 'data_error'
        else:
            self.device_data['status'] = 'connect_error'

        self.add_address_string_to_device_data(address_tuple)

    def get_device_status(self):
        return self.device_data.get('status', None)

    def get_device_data(self):
        return self.device_data

    def add_address_string_to_device_data(self, address_tuple):
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

    def read_device_data(self):
        try:
            self.device_name = self.read_device_name()
            self.version = self.read_version()
            self.serial_number = self.read_serial_number()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            # "Ошибка при подключении к COM
            return 'connect_err'

        device_data = {}
        default_prg = self.read_default_prg()
        device_data['device_name'] = self.device_name
        device_data['version'] = self.version
        device_data['serial_number'] = self.serial_number
        device_data['default_prg'] = default_prg
        return device_data


    def read_device_name(self):
        # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
        start_address = 0xF000
        register_count = 16
        # Выполняем запрос
        response = self.client.read_holding_registers(start_address, register_count)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = swap_modbus_bytes(byte_array, register_count)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        device_name = remove_empty_bytes(text)

        return device_name

    def read_version(self):
        # Читаем 16 регистров начиная с адреса 0xF010 (soft version)
        start_address = 0xF010
        register_count = 16
        # Выполняем запрос
        response = self.client.read_holding_registers(start_address, register_count)
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
        response = self.client.read_holding_registers(start_address, register_count)
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


    def read_default_prg(self):
        # Установка значений полей структуры
        file_number = 0xFFE0
        record_number = 0
        record_length = 124

        result = self.client.read_file_record(file_number, record_number, record_length)

        encrypt_res = result.records[0].record_data

        try:
            decrypt_res = decrypt_data(b'superkey', encrypt_res)
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
            decrypt_file = decrypt_data(b'superkey', encrypt_file)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        filename = 'default.prg'  # Имя файла с расширением .prg
        with open(filename, 'wb') as file:
            file.write(decrypt_file)

        return decrypt_file

    def parse_default_prg(self, default_prg):
        try:
            containers_count = get_conteiners_count(default_prg)
            containers_offset = get_containers_offset(default_prg)
            storage_container = get_storage_container(default_prg, containers_offset)
            device_tree = parse_tree(storage_container)
            return device_tree
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'parsing_err'

