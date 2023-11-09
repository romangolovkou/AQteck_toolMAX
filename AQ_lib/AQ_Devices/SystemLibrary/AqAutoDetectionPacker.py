import struct

from AqModbusTips import reverse_registers, swap_bytes_at_registers, remove_empty_bytes


# TODO: delete this shit file.
# Move all functionality to items
class AqAutoDetectionDevicePacker:
    def __init__(self):
        super().__init__()

    def pack(self, item, value):
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')
        if param_type != '' and param_size != '':
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

            return registers

    def unpack(self, item, data):
        param_attributes = item.get_param_attributes()

        param_type = param_attributes.get('type', '')
        param_size = param_attributes.get('param_size', '')

        if param_type != '' and param_size != '':
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
            # Конвертируем значения регистров в строку
            hex_string = ''.join(format(value, '04X') for value in data.registers)
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

            return param_value
