from AqAutoDetectionItems import AqAutoDetectStringParamItem
from AqBaseDevice import AqBaseDevice
from AqDeviceConfig import AqDeviceConfig
from AqConnect import AqModbusConnect
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

    system_params_dict = dict()

    # Add to init all what we need
    def __init__(self, event_manager, connect: AqModbusConnect):
        super().__init__(event_manager, connect)
        self._default_prg = None
        self._connect = connect

    def init_device(self) -> bool:
        self._create_system_params()
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

    def _create_system_params(self):
        # Створюємо строкові системні ітеми
        keys_list = list(self._system_string.keys())
        for i in range(len(keys_list)):
            param_attributes = dict()
            param_attributes['name'] = keys_list[i]
            param_attributes['modbus_reg'] = self._system_string[keys_list[i]][0]
            param_attributes['param_size'] = 2*self._system_string[keys_list[i]][1]
            param_attributes['read_func'] = self._system_string[keys_list[i]][2]
            param_attributes['R_Only'] = 1
            param_attributes['W_Only'] = 0
            self.system_params_dict[keys_list[i]] = AqAutoDetectStringParamItem(param_attributes)

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
            response = self._connect.read_param(self.system_params_dict[name])
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self._status = 'connect_err'
            return None

        # # Конвертируем значения регистров в строку
        # hex_string = ''.join(format(value, '04X') for value in response.registers)
        # # Конвертируем строку в массив байт
        # byte_array = bytes.fromhex(hex_string)
        # byte_array = swap_bytes_at_registers(byte_array, self._system_string[name][1])
        # # Расшифровуем в строку
        # text = byte_array.decode('ANSI')
        # result_str = remove_empty_bytes(text)
        result_str = self.system_params_dict[name].value

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
                result = self._connect.read_file_record(self._system_file[name][0], record_number, read_size)
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

    # TODO: wait until we will have good items and refactor this
    def read_parameter(self, item):
        """Read parameter from device"""
        self._stack_to_read.append(item)
        # param_attributes = item.get_param_attributes()
        #
        # param_type = param_attributes.get('type', '')
        # param_size = param_attributes.get('param_size', '')
        # modbus_reg = param_attributes.get('modbus_reg', '')
        #
        # if param_type != '' and param_size != '' and modbus_reg != '':
        #     if param_type == 'enum':
        #         if param_size > 16:
        #             reg_count = 2
        #             byte_size = 4
        #         else:
        #             reg_count = 1
        #             byte_size = 1
        #     else:
        #         byte_size = param_size
        #         if byte_size < 2:
        #             reg_count = 1
        #         else:
        #             reg_count = byte_size // 2
        #     # Формируем запрос
        #     self._stack_to_read.append({'method': self._connect.read_param, 'func': 3, 'start': modbus_reg,
        #                                'count': reg_count, 'callback': item.data_from_network})

    # TODO: refactor this huge function
    def write_parameter(self, item):
        if item.get_status() == 'changed':
            # param_attributes = item.get_param_attributes()
            #
            # modbus_reg = param_attributes.get('modbus_reg', '')
            # write_func = param_attributes.get('write_func', '')
            # data = item.data_for_network()

            self._stack_to_write.append(item)

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

        self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
