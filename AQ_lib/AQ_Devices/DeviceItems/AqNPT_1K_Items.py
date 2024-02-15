import struct

from AqBaseTreeItems import AqStringParamItem, AqModbusItem, AqFloatParamItem, AqMACParamItem
from AqModbusTips import remove_empty_bytes


class AqNPT_1K_StringParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'string'
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
        # byte_array = swap_bytes_at_registers(byte_array, reg_count)
        # Расшифровуем в строку
        text = byte_array.decode('ANSI')
        param_value = text #remove_empty_bytes(text)

        return param_value


class AqNPT_1K_CalibResultParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        param_attributes['type'] = 'string'
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
        param_2_hex_string = hex_string[:8]
        param_1_hex_string = hex_string[8:16]
        res_hex_string = hex_string[16:]

        byte_array = bytes.fromhex(res_hex_string)

        param_value = int.from_bytes(byte_array, byteorder='big', signed=False)

        if param_value == 1:
            text = 'калибровка не завершена'
        else:
            res_str = str(param_value)
            if len(res_str) == 3:
                msg = res_str[:1]
                com = res_str[1:]
                if msg == '1':
                    msg = 'Калибровка выполнена'
                elif msg == '2':
                    msg = 'Ошибка калибровки 200'
                elif msg == '3':
                    msg = 'Ошибка калибровки 300'
                else:
                    msg = 'Неизвестная ошибка :' + msg

                text = msg + ' команда ' + com
            else:
                text = res_str


        reg_count = self.param_size // 2
        # byte_array = swap_bytes_at_registers(byte_array, reg_count)
        # Расшифровуем в строку
        # text = byte_array.decode('ANSI')
        param_value = text #remove_empty_bytes(text)

        return param_value
