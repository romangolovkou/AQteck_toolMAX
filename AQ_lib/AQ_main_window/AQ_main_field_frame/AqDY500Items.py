import struct

from AQ_ModbusGenericItems import AqModbusEnumParamItem, AqModbusUnsignedParamItem, AqModbusFloatParamItem, \
    AqModbusFloatEnumParamItem
from AQ_ParseFunc import swap_modbus_bytes


class AqDY500EnumParamItem(AqModbusEnumParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        # костиль для enum з розміром два регістра
        if self.param_size == 4:
            packed_data = struct.pack('>I', self.value)
            registers = [struct.unpack('>H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        elif self.param_size == 2:
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


class AqDY500UnsignedParamItem(AqModbusUnsignedParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

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
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('>H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
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
            # byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 8:
            # byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>Q', byte_array)[0]
        else:
            raise Exception('AQ_ModbusUnsignedParamItemError: param size is incorrect')

        return param_value

class AqDY500FloatParamItem(AqModbusFloatParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        if self.param_size == 4:
            floats = struct.pack('>f', self.value)
            registers = struct.unpack('>HH', floats)  # Возвращает два short int значения
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
        # byte_array = swap_modbus_bytes(byte_array, reg_count)
        param_value = struct.unpack('>f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value


class AqDY500FloatEnumParamItem(AqModbusFloatEnumParamItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)

    def pack(self):
        if self.param_size == 4:
            floats = struct.pack('>f', self.value)
            registers = struct.unpack('>HH', floats)  # Возвращает два short int значения
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
        # byte_array = swap_modbus_bytes(byte_array, reg_count)
        param_value = struct.unpack('>f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value
