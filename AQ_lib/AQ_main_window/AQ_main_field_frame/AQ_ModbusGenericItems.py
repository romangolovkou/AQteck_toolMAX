import struct

from AQ_CustomTreeItems import AQ_UnsignedParamItem, AQ_ModbusItem, AQ_EnumParamItem, AQ_SignedParamItem, \
    AQ_FloatParamItem, AQ_StringParamItem, AQ_DateTimeParamItem, AQ_SignedToFloatParamItem, AQ_UnsignedToFloatParamItem, \
    AQ_FloatEnumParamItem
from AQ_ParamsDelegateEditors import AQ_EnumTreeComboBox, AQ_EnumROnlyTreeLineEdit
from AQ_ParseFunc import reverse_modbus_registers, swap_modbus_bytes, remove_empty_bytes


# TODO: сделать модбас итем зависящий от функции


class AQ_ModbusEnumParamItem(AQ_EnumParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_EnumParamItem.__init__(param_attributes)

    def pack(self):
        # костиль для enum з розміром два регістра
        if self.param_size >= 16:
            packed_data = struct.pack('I', self.value)
            registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        else:
            packed_data = struct.pack('H', self.value)
            registers = struct.unpack('H', packed_data)

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        if self.param_size > 16:
            param_value = struct.unpack('>I', byte_array)[0]
        else:
            param_value = struct.unpack('>H', byte_array)[0]

        return param_value


class AQ_ModbusUnsignedParamItem(AQ_UnsignedParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_UnsignedParamItem.__init__(param_attributes)

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


class AQ_ModbusSignedParamItem(AQ_SignedParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_SignedParamItem.__init__(param_attributes)

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


class AQ_ModbusFloatParamItem(AQ_FloatParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_FloatParamItem.__init__(param_attributes)

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


class AQ_ModbusStringParamItem(AQ_StringParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_StringParamItem.__init__(param_attributes)

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


class AQ_ModbusDateTimeParamItem(AQ_DateTimeParamItem, AQ_ModbusItem):
    def __init__(self, param_attributes):
        AQ_ModbusItem.__init__(param_attributes)
        AQ_DateTimeParamItem.__init__(param_attributes)

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


class AQ_ModbusSignedToFloatParamItem(AQ_SignedToFloatParamItem, AQ_ModbusSignedParamItem):
    def __init__(self, param_attributes):
        AQ_ModbusSignedParamItem.__init__(param_attributes)
        AQ_SignedToFloatParamItem.__init__(param_attributes)


class AQ_ModbusSignedToFloatParamItem(AQ_UnsignedToFloatParamItem, AQ_ModbusUnsignedParamItem):
    def __init__(self, param_attributes):
        AQ_ModbusUnsignedParamItem.__init__(param_attributes)
        AQ_UnsignedToFloatParamItem.__init__(param_attributes)


class AQ_ModbusSignedToFloatParamItem(AQ_FloatEnumParamItem, AQ_ModbusEnumParamItem):
    def __init__(self, param_attributes):
        AQ_ModbusEnumParamItem.__init__(param_attributes)
        AQ_FloatEnumParamItem.__init__(param_attributes)
