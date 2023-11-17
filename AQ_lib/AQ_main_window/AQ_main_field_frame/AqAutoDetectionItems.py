import struct

from AQ_CustomTreeItems import AqUnsignedParamItem, AqModbusItem, AqEnumParamItem, AqSignedParamItem, \
    AqFloatParamItem, AqStringParamItem, AqDateTimeParamItem, AqBitParamItem, AqIpParamItem, AqMACParamItem
from AQ_ParseFunc import reverse_modbus_registers, swap_modbus_bytes, remove_empty_bytes
from AqModbusTips import reverse_registers


# TODO: сделать модбас итем зависящий от функции


class AqAutoDetectEnumParamItem(AqEnumParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        # костиль для enum з розміром два регістра
        if self.param_size == 4:
            packed_data = struct.pack('I', self.value)
            registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        elif self.param_size == 2:
            packed_data = struct.pack('H', self.value)
            registers = struct.unpack('H', packed_data)
        else:
            raise Exception('AqAutoDetectEnumParamItemError: "param_size" is incorrect')


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
            raise Exception('AqAutoDetectEnumParamItemError: "param_size" is incorrect')

        return param_value


class AqAutoDetectUnsignedParamItem(AqUnsignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

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
            raise Exception('AqAutoDetectUnsignedParamItemError: param size is incorrect')
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
            raise Exception('AqAutoDetectUnsignedParamItemError: param size is incorrect')

        return param_value


class AqAutoDetectSignedParamItem(AqSignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

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
            raise Exception('AqAutoDetectSignedParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

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
            raise Exception('AqAutoDetectSignedParamItemError: param size is incorrect')

        return param_value


class AqAutoDetectFloatParamItem(AqFloatParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        if self.param_size == 4:
            floats = struct.pack('f', self.value)
            registers = struct.unpack('HH', floats)  # Возвращает два short int значения
        elif self.param_size == 8:
            floats_doubble = struct.pack('d', self.value)
            registers = struct.unpack('HHHH', floats_doubble)  # Возвращает два short int значения
        else:
            raise Exception('AqAutoDetectFloatParamItemError: param size is incorrect')

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        byte_array = swap_modbus_bytes(byte_array, reg_count)
        param_value = struct.unpack('f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value


class AqAutoDetectStringParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

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


class AqAutoDetectDateTimeParamItem(AqDateTimeParamItem, AqModbusItem):
    def __init__(self, param_attributes):

        super().__init__(param_attributes)

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


class AqAutoDetectIpParamItem(AqIpParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        if self.param_size == 4:
            packed_data = struct.pack('I', self.value)
        else:
            raise Exception('AqAutoDetectIpParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)
        if self.param_size == 4:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        else:
            raise Exception('AqAutoDetectIpParamItemError: param size is incorrect')

        return param_value

class AqAutoDetectMACParamItem(AqMACParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        if self.param_size == 6:  # MAC address
            packed_data = struct.pack('H', self.value)
        else:
            raise Exception('AqAutoDetectMACParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        if self.param_size == 6:
            byte_array = reverse_registers(byte_array)
            param_value = byte_array
        else:
            raise Exception('AqAutoDetectMACParamItemError: param size is incorrect')

        return param_value


class AqAutoDetectDiscretParamItem(AqBitParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['param_size'] = 1
        super().__init__(param_attributes)

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
