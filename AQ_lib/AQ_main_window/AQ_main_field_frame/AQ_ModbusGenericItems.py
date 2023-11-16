import struct

from AQ_CustomTreeItems import AqUnsignedParamItem, AqModbusItem, AqEnumParamItem, AqSignedParamItem, \
    AqFloatParamItem, AqStringParamItem, AqDateTimeParamItem, AqSignedToFloatParamItem, AqUnsignedToFloatParamItem, \
    AqFloatEnumParamItem, AqBitParamItem
from AQ_ParamsDelegateEditors import AqEnumTreeComboBox, AqEnumROnlyTreeLineEdit
from AQ_ParseFunc import reverse_modbus_registers, swap_modbus_bytes, remove_empty_bytes


# TODO: сделать модбас итем зависящий от функции

def get_param_attributes(attributes: list):
    param_attributes = dict()
    # Аттрибут з індексом 0 - ім'я параметру
    parameter_name = attributes[0]
    param_attributes['name'] = parameter_name
    # Аттрибут з індексом 2 - номер регістру
    param_attributes['modbus_reg'] = int(attributes[2])
    # Аттрибут з індексом 4 - номер функції для вичитки
    param_attributes['read_func'] = int(attributes[4])
    # Аттрибут з індексом 5 - номер функції для запису (необов'язковий)
    if attributes[5] == '-':
        param_attributes['R_Only'] = 1
        param_attributes['W_Only'] = 0
    else:
        param_attributes['R_Only'] = 0
        param_attributes['W_Only'] = 0
        param_attributes['write_func'] = int(attributes[5])

    # Аттрибут з індексом 7 - мінимально можливе значення (необов'язковий)
    if attributes[7] != '' and attributes[7] != '-':
        param_attributes['min_limit'] = int(attributes[7])
    # Аттрибут з індексом 8 - максимально можливе значення (необов'язковий)
    if attributes[8] != '' and attributes[8] != '-':
        param_attributes['max_limit'] = int(attributes[8])
    # Аттрибут з індексом 9 - умовні одиниці виміру параметру.
    # Має декоративне значення (необов'язковий). Приклад 'mV' '%' 'мкА' 'сек'
    param_attributes['unit'] = attributes[9]
    # # Аттрибут з індексом 6 - ім'я классу параметру та розмір параметру у бітах
    # parts = attributes[6].split(' ')
    # param_type = parts[0]
    # if param_type == 'enum' or param_type == 'string':
    #     param_size = int(parts[1])
    # else:
    #     param_size = int(parts[1]) // 8
    # param_attributes['type'] = param_type
    # param_attributes['param_size'] = param_size

    if attributes[10] != '' and attributes[10] != '-':
        if param_type == 'float':
            param_attributes['def_value'] = float(attributes[10])
        else:
            param_attributes['def_value'] = int(attributes[10])

    if param_type == 'enum' or param_type == 'float_enum':
        enum_strings = attributes[11].split('/')

        enum_str_dict = {}
        for row in range(len(enum_strings)):
            string_key = enum_strings[row].split('=')
            enum_str_dict[int(string_key[0])] = string_key[1]

        param_attributes['enum_strings'] = enum_str_dict

    if param_type == 'signed_to_float' or param_type == 'unsigned_to_float':
        if attributes[11] != '':
            enum_strings = attributes[11].split('/')

            enum_str_dict = {}
            for row in range(len(enum_strings)):
                string_key = enum_strings[row].split('=')
                enum_str_dict[int(string_key[0])] = string_key[1]

            param_attributes['enum_strings'] = enum_str_dict

        multiply = float(attributes[12])
        param_attributes['multiply'] = multiply


class AqModbusEnumParamItem(AqEnumParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_EnumParamItem.__init__(param_attributes)

    def pack(self):
        # костиль для enum з розміром два регістра
        if self.param_size == 2:
            packed_data = struct.pack('I', self.value)
            registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        elif self.param_size == 1:
            packed_data = struct.pack('H', self.value)
            registers = struct.unpack('H', packed_data)
        else:
            raise Exception('AqModbusEnumParamItemError: "param_size" is incorrect')


        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        if self.param_size == 4:
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 2:
            param_value = struct.unpack('>H', byte_array)[0]
        else:
            raise Exception('AqModbusEnumParamItemError: "param_size" is incorrect')

        return param_value


class AqModbusUnsignedParamItem(AqUnsignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_UnsignedParamItem.__init__(param_attributes)

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('H', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('H', self.value)
        elif self.param_size == 4:
            packed_data = struct.pack('I', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('Q', self.value)
        else:
            raise Exception('AQ_ModbusUnsignedParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        if self.param_size == 1:
            param_value = struct.unpack('>H', byte_array)[0]
        elif self.param_size == 2:
            param_value = struct.unpack('>H', byte_array)[0]
        elif self.param_size == 4:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 8:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>Q', byte_array)[0]
        else:
            raise Exception('AQ_ModbusUnsignedParamItemError: param size is incorrect')

        return param_value


class AqModbusSignedParamItem(AqSignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_SignedParamItem.__init__(param_attributes)

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('h', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('h', self.value)
        elif self.param_size == 4:
            packed_data = struct.pack('i', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('q', self.value)
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        if self.param_size == 1:
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        elif self.param_size == 2:
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        elif self.param_size == 4 or self.param_size == 8:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')

        return param_value


class AqModbusFloatParamItem(AqFloatParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_FloatParamItem.__init__(param_attributes)

    def pack(self):
        if self.param_size == 4:
            floats = struct.pack('f', self.value)
            registers = struct.unpack('HH', floats)  # Возвращает два short int значения
        elif self.param_size == 8:
            floats_doubble = struct.pack('d', self.value)
            registers = struct.unpack('HHHH', floats_doubble)  # Возвращает два short int значения
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        byte_array = swap_modbus_bytes(byte_array, reg_count)
        param_value = struct.unpack('>f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value


class AqModbusStringParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_StringParamItem.__init__(param_attributes)

    def pack(self):
        text_bytes = self.value.encode('ANSI')
        # Добавляем нулевой байт в конец, если длина списка не кратна 2
        if len(text_bytes) % 2 != 0:
            text_bytes += b'\x00'
        registers = [struct.unpack('H', text_bytes[i:i + 2])[0] for i in range(0, len(text_bytes), 2)]

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        byte_array = swap_modbus_bytes(byte_array, reg_count)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        param_value = remove_empty_bytes(text)

        return param_value


class AqModbusDateTimeParamItem(AqDateTimeParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AQ_ModbusItem.__init__(param_attributes)
        # AQ_DateTimeParamItem.__init__(param_attributes)

    def pack(self):
        packed_data = struct.pack('I', self.value)
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        byte_array = reverse_modbus_registers(byte_array)
        param_value = struct.unpack('>I', byte_array)[0]

        return param_value


class AqModbusSignedToFloatParamItem(AqSignedToFloatParamItem, AqModbusSignedParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AqModbusSignedParamItem.__init__(param_attributes)
        # AQ_SignedToFloatParamItem.__init__(param_attributes)


class AqModbusUnsignedToFloatParamItem(AqUnsignedToFloatParamItem, AqModbusUnsignedParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AqModbusUnsignedParamItem.__init__(param_attributes)
        # AQ_UnsignedToFloatParamItem.__init__(param_attributes)


class AqModbusFloatEnumParamItem(AqFloatEnumParamItem, AqModbusEnumParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        # AqModbusEnumParamItem.__init__(param_attributes)
        # AQ_FloatEnumParamItem.__init__(param_attributes)


class AqModbusDiscretParamItem(AqBitParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['param_size'] = 1
        super().__init__(param_attributes)
        # AqModbusEnumParamItem.__init__(param_attributes)
        # AQ_FloatEnumParamItem.__init__(param_attributes)

    def pack(self):
        if self.value == 1:
            data = True
        else:
            data = False
        return data

    def unpack(self, data):
        if data.bits[0] is True:
            param_value = 1
        else:
            param_value = 0
        return param_value
