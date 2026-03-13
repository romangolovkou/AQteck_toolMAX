import struct

from AqBaseTreeItems import AqUnsignedParamItem, AqModbusItem, AqEnumParamItem, AqSignedParamItem, \
    AqFloatParamItem, AqStringParamItem, AqDateTimeParamItem, AqSignedToFloatParamItem, AqUnsignedToFloatParamItem, \
    AqFloatEnumParamItem, AqBitParamItem, AqBitMaskParamItem
# from AQ_ParseFunc import reverse_modbus_registers, swap_modbus_bytes, remove_empty_bytes
from AqModbusTips import reverse_registers, swap_bytes_at_registers, remove_empty_bytes, swap_registers


# TODO: сделать модбас итем зависящий от функции


class AqModbusEnumParamItem(AqEnumParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'enum'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        # костиль для enum з розміром два регістра
        if self.param_size == 2:
            packed_data = struct.pack('>H', self.value)

            reg_count = self.param_size // 2
            if self.byte_order == 'little-endian':
                packed_data = swap_bytes_at_registers(packed_data, reg_count)

            if self.reg_order == 'little-endian':
                packed_data = swap_registers(packed_data)

            registers = [struct.unpack('>H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        elif self.param_size == 1:
            packed_data = struct.pack('>H', self.value)

            reg_count = self.param_size // 2
            if self.byte_order == 'little-endian':
                packed_data = swap_bytes_at_registers(packed_data, reg_count)

            registers = struct.unpack('>H', packed_data)
        else:
            raise Exception('AqModbusEnumParamItemError: "param_size" is incorrect')

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            byte_array = swap_bytes_at_registers(byte_array, reg_count)

        if self.param_size == 4:
            if self.reg_order == 'little-endian':
                byte_array = swap_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 2:
            param_value = struct.unpack('>H', byte_array)[0]
        else:
            raise Exception('AqModbusEnumParamItemError: "param_size" is incorrect')

        return param_value


class AqModbusUnsignedParamItem(AqUnsignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'unsigned'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('>H', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('>H', self.value)
        elif self.param_size == 4:
            packed_data = struct.pack('>I', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('>Q', self.value)
        else:
            raise Exception('AQ_ModbusUnsignedParamItemError: param size is incorrect')

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            packed_data = swap_bytes_at_registers(packed_data, reg_count)

        if self.reg_order == 'little-endian':
            packed_data = swap_registers(packed_data)

        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('>H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            byte_array = swap_bytes_at_registers(byte_array, reg_count)

        if self.param_size == 1:
            param_value = struct.unpack('>H', byte_array)[0]

        #TODO: have bug
        elif self.param_size == 2:
            param_value = struct.unpack('>H', byte_array)[0]
        elif self.param_size == 4:
            if self.reg_order == 'little-endian':
                byte_array = swap_registers(byte_array)
            # byte_array = reverse_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 8:
            if self.reg_order == 'little-endian':
                byte_array = swap_registers(byte_array)
            # byte_array = reverse_registers(byte_array)
            param_value = struct.unpack('>Q', byte_array)[0]
        else:
            raise Exception('AQ_ModbusUnsignedParamItemError: param size is incorrect')

        return param_value


class AqModbusSignedParamItem(AqSignedParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'signed'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('>h', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('>h', self.value)
        elif self.param_size == 4:
            packed_data = struct.pack('>i', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('>q', self.value)
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            packed_data = swap_bytes_at_registers(packed_data, reg_count)

        if self.reg_order == 'little-endian':
            packed_data = swap_registers(packed_data)

        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('>H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            byte_array = swap_bytes_at_registers(byte_array, reg_count)

        if self.param_size == 1:
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        elif self.param_size == 2:
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        elif self.param_size == 4 or self.param_size == 8:
            if self.reg_order == 'little-endian':
                byte_array = swap_registers(byte_array)
            # byte_array = reverse_registers(byte_array)
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')

        return param_value


class AqModbusFloatParamItem(AqFloatParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'float'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        if self.param_size == 4:
            floats = struct.pack('>f', self.value)

            if self.reg_order == 'little-endian':
                floats = swap_registers(floats)

            reg_count = self.param_size // 2
            if self.byte_order == 'little-endian':
                floats = swap_bytes_at_registers(floats, reg_count)

            registers = struct.unpack('>HH', floats)  # Возвращает два short int значения
        elif self.param_size == 8:
            floats_doubble = struct.pack('>d', self.value)
            registers = struct.unpack('>HHHH', floats_doubble)  # Возвращает два short int значения
        else:
            raise Exception('AQ_ModbusSignedParamItemError: param size is incorrect')

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2

        if self.reg_order == 'little-endian':
            byte_array = swap_registers(byte_array)

        if self.byte_order == 'little-endian':
            byte_array = swap_bytes_at_registers(byte_array, reg_count)

        param_value = struct.unpack('>f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value


class AqModbusStringParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'string'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        text_bytes = self.value.encode('ANSI')
        # Добавляем нулевой байт в конец, если длина списка не кратна 2
        if len(text_bytes) % 2 != 0:
            text_bytes += b'\x00'

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            text_bytes = swap_bytes_at_registers(text_bytes, reg_count)

        if self.reg_order == 'little-endian':
            text_bytes = swap_registers(text_bytes)

        registers = [struct.unpack('>H', text_bytes[i:i + 2])[0] for i in range(0, len(text_bytes), 2)]

        return registers

    def unpack(self, data):
        # Конвертируем значения регистров в строку
        hex_string = ''.join(format(value, '04X') for value in data.registers)
        # Конвертируем строку в массив байт
        byte_array = bytes.fromhex(hex_string)

        reg_count = self.param_size // 2
        if self.byte_order == 'little-endian':
            byte_array = swap_bytes_at_registers(byte_array, reg_count)

        if self.reg_order == 'little-endian':
            byte_array = swap_registers(byte_array)

        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        param_value = remove_empty_bytes(text)

        return param_value


class AqModbusDateTimeParamItem(AqDateTimeParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'date_time'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

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

        byte_array = reverse_registers(byte_array)
        param_value = struct.unpack('>I', byte_array)[0]

        return param_value


class AqModbusSignedToFloatParamItem(AqSignedToFloatParamItem, AqModbusSignedParamItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'signed_to_float'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('h', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('h', self.value)
            if len(packed_data) < self.param_size + 1:
                packed_data += b'\x00\x00'
        elif self.param_size == 4:
            packed_data = struct.pack('i', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('q', self.value)
        else:
            raise Exception('AQ_ModbusSignedToFloatParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers

class AqModbusUnsignedToFloatParamItem(AqUnsignedToFloatParamItem, AqModbusUnsignedParamItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'unsigned_to_float'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')

    def pack(self):
        if self.param_size == 1:
            packed_data = struct.pack('h', self.value)
        elif self.param_size == 2:
            packed_data = struct.pack('h', self.value)
            if len(packed_data) < self.param_size + 1:
                packed_data += b'\x00\x00'
        elif self.param_size == 4:
            packed_data = struct.pack('i', self.value)
        elif self.param_size == 8:
            packed_data = struct.pack('q', self.value)
        else:
            raise Exception('AQ_ModbusUnsignedToFloatParamItemError: param size is incorrect')
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        return registers


class AqModbusFloatEnumParamItem(AqFloatEnumParamItem, AqModbusEnumParamItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'float_to_enum'
        super().__init__(param_attributes)
        self.byte_order = param_attributes.get('byte_order', 'big-endian')
        self.reg_order = param_attributes.get('reg_order', 'big-endian')


class AqModbusDiscretParamItem(AqBitParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['param_size'] = 1
        param_attributes['type'] = 'discret_bit'
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


class AqModbusBitMaskParamItem(AqBitMaskParamItem, AqModbusUnsignedParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
