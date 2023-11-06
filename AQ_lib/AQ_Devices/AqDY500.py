import csv
import struct

from AQ_CustomTreeItems import AQ_CatalogItem
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AqBaseDevice import AqBaseDevice
from AqAutoDetectionLibrary import get_item_by_type
from AqDeviceConfig import AqDeviceConfig
from SystemLibrary.AqModbusTips import remove_empty_bytes, reverse_registers
from PySide6.QtCore import Qt


class AqDY500(AqBaseDevice):
    def __init__(self, event_manager, connect, address_tuple):
        super().__init__(event_manager, connect, address_tuple)

        self._device_config = None
        self._read_error_flag = False
        self._write_error_flag = False

    def init_device(self) -> bool:
        self._info['name'] = self.__read_device_name()
        self._info['version'] = None
        self._info['serial_num'] = None

        self._device_config = self.__read_configuration()
        # TODO: move this function into external module
        self._device_tree = self.__parse_device_config()
        return True

    def __read_device_name(self):
        file_path = '110_device_conf/' + self._address_tuple[2]
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

    def __parse_device_config(self):
        try:
            # Створюємо список імен каталогів
            catalogs_name_set = set()
            for i in range(len(self._device_config)):
                config_string = self._device_config[i]
                # Разделение записи на поля по символу ';'
                fields = config_string.split(';')
                catalogs_name_set.add(fields[1])
            # Сортировка элементов сета в алфавитном порядке
            sorted_list = sorted(catalogs_name_set)

            # створюємо список з каталог-ітемами
            catalogs = []
            for i in range(len(sorted_list)):
                catalog_item = AQ_CatalogItem(sorted_list[i])
                param_attributes = dict()
                param_attributes['name'] = sorted_list[i]
                param_attributes['is_catalog'] = 1
                catalog_item.setData(param_attributes, Qt.UserRole)
                catalogs.append(catalog_item)

            # Додаємо до каталогів відповідні параметр-ітеми
            for i in range(len(catalogs)):
                cat_name = catalogs[i].text()
                for j in range(len(self._device_config)):
                    config_string = self._device_config[j]
                    # Разделение записи на поля по символу ';'
                    fields = config_string.split(';')
                    if fields[1] == cat_name:
                        param_attributes = dict()
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

                        param_item = get_item_by_type(param_attributes.get('type', ''), parameter_name)
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

    def __read_configuration(self):
        file_path = '110_device_conf/' + self._address_tuple[2]
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
                    byte_size = 4
                else:
                    reg_count = 2
                    byte_size = 1
            else:
                byte_size = param_size
                if byte_size < 2:
                    reg_count = 1
                else:
                    reg_count = byte_size // 2
            # Выполняем запрос
            response = self.client.read_param(modbus_reg, reg_count, read_func)
            if response != 'modbus_error':
                param_value = None
                if read_func == 3:
                    # Конвертируем значения регистров в строку
                    hex_string = ''.join(format(value, '04X') for value in response.registers)
                    # Конвертируем строку в массив байт
                    byte_array = bytes.fromhex(hex_string)
                    # byte_array = swap_modbus_registers(byte_array)

                    if param_type == 'unsigned':
                        if byte_size == 1:
                            param_value = struct.unpack('>HH', byte_array)[0]
                        elif byte_size == 2:
                            param_value = struct.unpack('>HH', byte_array)[0]
                        elif byte_size == 4:
                            # byte_array = reverse_modbus_registers(byte_array)
                            param_value = struct.unpack('>I', byte_array)[0]
                        elif byte_size == 6:  # MAC address
                            # byte_array = reverse_modbus_registers(byte_array)
                            param_value = byte_array  # struct.unpack('>I', byte_array)[0]
                        elif byte_size == 8:
                            # byte_array = reverse_modbus_registers(byte_array)
                            param_value = struct.unpack('>Q', byte_array)[0]
                    elif param_type == 'signed':
                        if byte_size == 1:
                            param_value = struct.unpack('b', byte_array[1])[0]
                        elif byte_size == 2:
                            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                        elif byte_size == 4 or byte_size == 8:
                            # byte_array = reverse_modbus_registers(byte_array)
                            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
                    elif param_type == 'string':
                        # byte_array = swap_modbus_bytes(byte_array, reg_count)
                        # Расшифровуем в строку
                        text = byte_array.decode('ANSI')
                        param_value = remove_empty_bytes(text)
                    elif param_type == 'enum':
                        # костиль для enum з розміром два регістра
                        if byte_size == 4:
                            param_value = struct.unpack('>I', byte_array)[0]
                        else:
                            param_value = struct.unpack('>I', byte_array)[0]
                            if modbus_reg == 101:
                                param_value = param_value - 1

                    elif param_type == 'float' or param_type == 'float_enum':
                        # byte_array = swap_modbus_bytes(byte_array, reg_count)
                        param_value = struct.unpack('>f', byte_array)[0]
                        param_value = round(param_value, 7)
                    elif param_type == 'date_time':
                        if byte_size == 4:
                            byte_array = reverse_registers(byte_array)
                            param_value = struct.unpack('>I', byte_array)[0]
                elif read_func == 2 or read_func == 1:
                    if response[0] is True:
                        param_value = 1
                    else:
                        param_value = 0

                item.force_set_value(param_value)
                item.synchronized = True
            else:
                self._read_error_flag = True

    def __read_slave_id(self):
        # Читаем 16 регистров начиная с адреса 0xF086 (serial_number)
        start_address = 40052
        register_count = 2
        read_func = 3
        # Выполняем запрос
        response = self.client.read_param(start_address, register_count, read_func)
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in response.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        param_value = struct.unpack('>HH', byte_array)[0]

        return param_value

    def write_parameter(self, item):
        param_attibutes = item.get_param_attributes()
        if param_attibutes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                result = self.write_parameter(child_item)
                if result == 'write_error':
                    return result
        else:
            if item.get_status() == 'changed':
                param_type = param_attibutes.get('type', '')
                param_size = param_attibutes.get('param_size', '')
                modbus_reg = param_attibutes.get('modbus_reg', '')
                value = item.value
                packed_data = None
                if param_type != '' and param_size != '' and modbus_reg != '':
                    write_func = param_attibutes.get('write_func', None)
                    if write_func == 16:
                        registers = None
                        if param_type == 'unsigned':
                            if param_size == 1:
                                packed_data = struct.pack('H', value)
                            elif param_size == 2:
                                packed_data = struct.pack('H', value)
                            elif param_size == 4:
                                packed_data = struct.pack('>I', value)
                            elif param_size == 6:  # MAC address
                                packed_data = struct.pack('H', value)
                            elif param_size == 8:
                                packed_data = struct.pack('Q', value)
                            # Разбиваем упакованные данные на 16-битные значения (2 байта)
                            registers = [struct.unpack('>H', packed_data[i:i + 2])[0]
                                         for i in range(0, len(packed_data), 2)]
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
                            registers = [struct.unpack('>H', packed_data[i:i + 2])[0]
                                         for i in range(0, len(packed_data), 2)]
                        elif param_type == 'string':
                            text_bytes = value.encode('ANSI')
                            # Добавляем нулевой байт в конец, если длина списка не кратна 2
                            if len(text_bytes) % 2 != 0:
                                text_bytes += b'\x00'
                            registers = [struct.unpack('H', text_bytes[i:i + 2])[0]
                                         for i in range(0, len(text_bytes), 2)]
                        elif param_type == 'enum':
                            # костиль для enum з розміром два регістра
                            if param_size == 4:
                                packed_data = struct.pack('I', value)
                                registers = [struct.unpack('H', packed_data[i:i + 2])[0]
                                             for i in range(0, len(packed_data), 2)]
                            else:
                                packed_data = struct.pack('H', value)
                                registers = struct.unpack('H', packed_data)
                        elif param_type == 'float' or param_type == 'float_enum':
                            if param_size == 4:
                                floats = struct.pack('>f', value)
                                registers = struct.unpack('>HH', floats)  # Возвращает два short int значения
                            elif param_size == 8:
                                floats_doubble = struct.pack('d', value)
                                registers = struct.unpack('HHHH', floats_doubble)  # Возвращает два short int значения
                        # elif param_type == 'date_time':
                        #     if byte_size == 4:
                        #         byte_array = reverse_modbus_registers(byte_array)
                        #         param_value = struct.unpack('>I', byte_array)[0]

                        try:
                            result = self.client.write_param(modbus_reg, registers, write_func)
                            if result != 'modbus_error':
                                item.synchro_last_value_and_value()
                            else:
                                self._write_error_flag = True
                        except Exception as e:
                            print(f"Error occurred: {str(e)}")
                    elif write_func == 5:
                        if value == 1:
                            value = True
                        elif value == 0:
                            value = False
                        result = self.client.write_param(modbus_reg, value, write_func)
                        if result != 'modbus_error':
                            item.synchro_last_value_and_value()
                        else:
                            self._write_error_flag = True
                    elif write_func == 6:
                        if modbus_reg == 101:
                            value += 1
                        result = self.client.write_param(modbus_reg, value, write_func)
                        if result != 'modbus_error':
                            item.synchro_last_value_and_value()
                        else:
                            self._write_error_flag = True

        if self._write_error_flag is True:
            self._write_error_flag = False
            self._event_manager.emit_event('param_write_error')
            return 'write_err'

        return 'ok'

    def get_configuration(self) -> AqDeviceConfig:
        config = AqDeviceConfig()
        config.device_name = self.info('name')

        for devParam in self._params_list:
            param_attributes = devParam.get_param_attributes()
            config.saved_param_list.append({'modbus_reg': param_attributes.get('modbus_reg', 0),
                                            'value': devParam.value})

        return config

    def set_configuration(self, config: AqDeviceConfig):
        if self.info('name') != config.device_name:
            return NotImplementedError
        # TODO: need generate custom exception or generate event to display error message

        for cfgParam in config.saved_param_list:
            for devParam in self._params_list:
                param_attributes = devParam.get_param_attributes()
                modbus_reg = param_attributes.get('modbus_reg', 0)
                if cfgParam['modbus_reg'] == modbus_reg:
                    devParam.value = cfgParam['value']
        # TODO: optimize this algorithm

        self._event_manager.emit_event('current_device_data_updated', self, self._changed_param_stack)
