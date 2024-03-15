import os
import struct

from PySide6.QtCore import Qt

from AqBaseTreeItems import AqUnsignedParamItem, AqModbusItem, AqEnumParamItem, AqSignedParamItem, \
    AqFloatParamItem, AqStringParamItem, AqDateTimeParamItem, AqBitParamItem, AqIpParamItem, AqMACParamItem, \
    AqModbusFileItem
from AqCRC32 import Crc32
# from AQ_ParseFunc import reverse_modbus_registers, swap_modbus_bytes, remove_empty_bytes
from AqModbusTips import reverse_registers, swap_bytes_at_registers, remove_empty_bytes
# from AqModbusTips import reverse_registers

from Crypto.Cipher import DES


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
            byte_array = reverse_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif self.param_size == 8:
            byte_array = reverse_registers(byte_array)
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
            byte_array = reverse_registers(byte_array)
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
        byte_array = swap_bytes_at_registers(byte_array, reg_count)
        param_value = struct.unpack('f', byte_array)[0]
        param_value = round(param_value, 7)

        return param_value

class AqAutoDetectModbusFileItem(AqModbusFileItem):
    def __init__(self, param_attributes, get_password=None, msg_dict=None):
        super().__init__(param_attributes)
        self.key = b'superkey'
        self.__get_pass = get_password
        self._msg_dict = msg_dict
        self._msg_string = None

    def pack(self):
        record_data = self.value
        crc = Crc32().calculate(record_data)
        length = len(record_data)
        # Выравнивание длины исходных данных
        pad_length = 8 - (len(record_data) % 8)
        padded_data = record_data + bytes([0x00] * pad_length)

        data_to_write = padded_data + length.to_bytes(4, byteorder='little')
        data_to_write = data_to_write + crc.to_bytes(4, byteorder='little', signed=True)

        encrypted_record_data = self._encrypt_data(data_to_write)
        return encrypted_record_data

    def unpack(self, data):
        # TODO: тимчасове збереження файлу (потрібно для відладки)
        if self.get_param_attributes()['file_num'] == 0xFFE0:
            # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
            roaming_folder = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming')
            # Проверяем наличие папки Roaming, если её нет - создаем
            if not os.path.exists(roaming_folder):
                os.makedirs(roaming_folder)

            for file in os.listdir(roaming_folder):
                if '_default' in file:
                    remove_path = os.path.join(roaming_folder, file)
                    try:
                        os.remove(remove_path)
                        print(f'Файл {remove_path} удален.')
                    except OSError as e:
                        print(f'Ошибка удаления файла {remove_path}: {e}')

            filename = 'enc_default.prg'
            # Полный путь к файлу в папке Roaming
            full_filepath = os.path.join(roaming_folder, filename)
            with open(full_filepath, 'wb') as file:
                file.write(data)

        decrypt_file = None
        try:
            # Перевірка на кратність 8 байтам, потрібно для DES
            if (len(data) % 8) > 0:
                padding = 8 - (len(data) % 8)
                data = data + bytes([padding] * padding)
            decrypt_file = self.__decrypt_data(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        return decrypt_file

    def __decrypt_data(self, encrypted_data):
        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.key)
        decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные

        return decrypted_data

    def _encrypt_data(self, data):
        # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
        cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.key)
        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    def set_key(self, new_key):
        self.key = new_key

    def set_file_size(self, new_file_size):
        attr = self.get_param_attributes()
        attr['file_size'] = new_file_size
        self.setData(attr, Qt.UserRole)
        print(f'new_file_size: {new_file_size}')

    def __get_hash(self):
        userPass = self.__get_password()

        if userPass is None:
            # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
            return b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524"
        else:
            low = 0
            high = 0

            password_bytes = userPass.encode('cp1251')

            for i in range(0, len(password_bytes), 2):
                low += password_bytes[i]
                low -= (low << 13) | (low >> 19)
                low = low & 0xFFFFFFFF

                if i + 1 >= len(password_bytes):
                    break

                high += password_bytes[i + 1]
                high -= (high << 13) | (high >> 19)
                high = high & 0xFFFFFFFF

            low = bytes.fromhex(hex(low)[2:])[::-1]
            high = bytes.fromhex(hex(high)[2:])[::-1]
            hash = low + high
            return hash

    def __get_password(self):
        if self.__get_pass is not None:
            password = self.__get_pass()
        else:
            password = None

        return password


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            if self.value_in_device is None:
                self.value_in_device = new_value
            # else:
            #     if self.value_in_device == new_value:
            #         self.param_status = 'ok'
            #     else:
            self.param_status = 'changed'
            self.synchronized = False
            self._value = new_value
        else:
            self.param_status = 'error'

    def confirm_writing(self, result: bool, message=None):
        """
        The function must be called for each writing operation.
        :param result: True - success writing, False - writing fail.
        :param message: If need - error message.
        :return:
        """
        super().confirm_writing(result, message)
        self._msg_string = self._msg_dict.get(self.param_status, None)

    def get_msg_string(self):
        return self._msg_string


class AqAutoDetectPasswordFileItem(AqAutoDetectModbusFileItem):
    def __init__(self, param_attributes, get_password=None, msg_dict=None):
        super().__init__(param_attributes, get_password, msg_dict)

    def pack(self):
        record_data = self.value
        crc = Crc32().calculate(record_data)
        length = len(record_data)
        # Выравнивание длины исходных данных
        pad_length = 8 - (len(record_data) % 8)
        padded_data = record_data + bytes([0x00] * pad_length)

        # data_to_write = padded_data + length.to_bytes(4, byteorder='little')
        # data_to_write = data_to_write + crc.to_bytes(4, byteorder='little', signed=True)

        encrypted_record_data = self._encrypt_data(padded_data)
        return encrypted_record_data


class AqAutoDetectStringParamItem(AqStringParamItem, AqModbusItem):
    def __init__(self, param_attributes):
        super().__init__(param_attributes)
        self.value = ''

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
        byte_array = swap_bytes_at_registers(byte_array, reg_count)
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

        byte_array = reverse_registers(byte_array)
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
            byte_array = reverse_registers(byte_array)
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
