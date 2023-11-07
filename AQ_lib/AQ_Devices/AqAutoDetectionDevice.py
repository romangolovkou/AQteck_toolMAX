import struct

from AQ_TreeViewItemModel import AQ_TreeItemModel
from AqBaseDevice import AqBaseDevice
from AqDeviceConfig import AqDeviceConfig
from SystemLibrary.AqModbusTips import swap_bytes_at_registers, remove_empty_bytes, \
    reverse_registers


from Crypto.Cipher import DES

from SystemLibrary.AqAutoDetectionLibrary import get_containers_count, \
    get_containers_offset, get_storage_container, parse_tree


class AqAutoDetectionDevice(AqBaseDevice):

    # Format: 'param_name': {start_reg, count, func}
    _system_string = {
        'name':         [0xF000, 16, 3],
        'version':      [0xF010, 16, 3],
        'serial_num':   [0xF086, 10, 3]
    }
    _system_param = {
        'ip':           [0x001A, 2]
    }

    # Format: 'file_name': [file_num, start_record_num, file_size (in bytes)]
    _system_file = {
        'reboot':       [0xDEAD, 0, 40],
        'status':       [0x0001, 0, 248],
        'default_prg':  [0xFFE0, 0, 248]  # file_size will be changed later in code
    }

    # Add to init all what we need
    def __init__(self, event_manager, connect, network_settings):
        super().__init__(event_manager, connect, network_settings)
        self._default_prg = None

    def init_device(self) -> bool:

        self._info['name'] = self.__read_string('name')
        self._info['version'] = self.__read_string('version')
        self._info['serial_num'] = self.__read_string('serial_num')
        self._info['password'] = None
        self._default_prg = self.__read_default_prg()

        if self._default_prg == 'decrypt_err':
            self._status = 'error'
            return False

        self._device_tree = self.__parse_default_prg()
        if self._device_tree == 'parsing_err' or \
                self._device_tree is None:
            self._status = 'error'
            return False

        # TODO: describe rules to chache which functions are supported
        # into AutoDetectionDevice
        # later should be json file inside device with definitions
        self._functions['read_write'] = True,
        self._functions['rtc'] = True
        self._functions['password'] = True
        self._functions['calibration'] = True
        self._functions['log'] = True
        self._functions['fw_update'] = True
        self._functions['restart'] = True

        self._status = 'ok'
        return True

    def __parse_default_prg(self):
        try:
            containers_count = get_containers_count(self._default_prg)
            containers_offset = get_containers_offset(self._default_prg)
            storage_container = get_storage_container(self._default_prg, containers_offset)
            device_tree = parse_tree(storage_container)
            return device_tree
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'parsing_err'

    def __read_string(self, name):
        try:
            # Выполняем запрос
            response = self.client.read_param(self._system_string[name][0],
                                              self._system_string[name][1],
                                              self._system_string[name][2])
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self._status = 'connect_err'
            return None

        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        byte_array = swap_bytes_at_registers(byte_array, self._system_string[name][1])
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        result_str = remove_empty_bytes(text)

        return result_str

    def __read_file(self, name):
        record_size = 124
        left_to_read = self._system_file[name][2] // 2
        # Не понял логику этих строк, надо отладить
        # if (file_size // 2) % 124 or file_size % 2:
        #     req_count = req_count + 1
        encrypt_file = bytearray()

        record_number = self._system_file[name][1]
        while left_to_read:
            read_size = record_size if left_to_read > record_size else left_to_read
            try:
                result = self.client.read_file_record(self._system_file[name][0], record_number, read_size)
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                self._status = 'connect_err'
                return None
            record_number += read_size
            left_to_read -= read_size
            encrypt_file += result.records[0].record_data

        try:
            # Перевірка на кратність 8 байтам, потрібно для DES
            if (len(encrypt_file) % 8) > 0:
                padding = 8 - (len(encrypt_file) % 8)
                encrypt_file = encrypt_file + bytes([padding] * padding)
            decrypt_file = self.__decrypt_data(encrypt_file)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self._status = 'decrypt_err'
            return None  # Помилка дешифрування

        return decrypt_file

    def __read_default_prg(self):
        # Read first page from file to determine file size
        first_page = self.__read_file('default_prg')

        file_size = int.from_bytes((first_page[4:8][::-1]), byteorder='big')
        self._system_file['default_prg'][2] = file_size

        # Read full file
        decrypt_file = self.__read_file('default_prg')

        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        filename = 'default.prg'
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
        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    def __get_key(self):
        # return self._info['password'] if self._info['password'] else b'superkey'
        return self.info('password') if self.info('password') else b'superkey'

    def __get_hash(self):
        # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
        return b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524"

    # TODO: refactor this huge function
    def read_parameter(self, item):
        """Read parameter from device"""
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        modbus_reg = param_attributes.get('modbus_reg', '')

        if param_type != '' and param_size != '' and modbus_reg != '':
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
            # TODO: read func should be get from param object
            response = self.client.read_param(modbus_reg, reg_count, 3)
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
                    byte_array = reverse_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]
                elif byte_size == 6:  # MAC address
                    byte_array = reverse_registers(byte_array)
                    param_value = byte_array  # struct.unpack('>I', byte_array)[0]
                elif byte_size == 8:
                    byte_array = reverse_registers(byte_array)
                    param_value = struct.unpack('>Q', byte_array)[0]
            elif param_type == 'signed':
                if byte_size == 1:
                    param_value = struct.unpack('b', byte_array[1])[0]
                elif byte_size == 2:
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                elif byte_size == 4 or byte_size == 8:
                    byte_array = reverse_registers(byte_array)
                    param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
            elif param_type == 'string':
                byte_array = swap_bytes_at_registers(byte_array, reg_count)
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
                byte_array = swap_bytes_at_registers(byte_array, reg_count)
                param_value = struct.unpack('f', byte_array)[0]
                param_value = round(param_value, 7)
            elif param_type == 'date_time':
                if byte_size == 4:
                    byte_array = reverse_registers(byte_array)
                    param_value = struct.unpack('>I', byte_array)[0]

            item.force_set_value(param_value)
            item.synchronized = True

    # TODO: refactor this huge function
    def write_parameter(self, item):
        param_attibutes = item.get_param_attributes()
        if param_attibutes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.write_parameter(child_item)
        else:
            if item.get_status() == 'changed':
                param_type = param_attibutes.get('type', '')
                param_size = param_attibutes.get('param_size', '')
                modbus_reg = param_attibutes.get('modbus_reg', '')
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
                            registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in
                                         range(0, len(packed_data), 2)]
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
                        self.client.write_param(modbus_reg, registers, 16)
                        item.synchro_last_value_and_value()
                    except Exception as e:
                        print(f"Error occurred: {str(e)}")

    def get_configuration(self) -> AqDeviceConfig:
        config = AqDeviceConfig()
        config.device_name = self.info('name')

        for devParam in self._params_list:
            param_attributes = devParam.get_param_attributes()
            config.saved_param_list.append({'UID': param_attributes.get('UID', 0),
                                            'modbus_reg': param_attributes.get('modbus_reg', 0),
                                            'value': devParam.value})

        return config

    def set_configuration(self, config: AqDeviceConfig):
        if  self.info('name') != config.device_name:
            return NotImplementedError
            #TODO: need generate custom exception or generate event to display error message

        for cfgParam in config.saved_param_list:
            for devParam in self._params_list:
                param_attributes = devParam.get_param_attributes()
                modbusReg = param_attributes.get('modbus_reg', 0)
                if cfgParam['modbus_reg'] == modbusReg:
                    devParam.value = cfgParam['value']
        #TODO: optimize this algorithm

        self.event_manager.emit_event('current_device_data_updated', self, self.changed_param_stack)