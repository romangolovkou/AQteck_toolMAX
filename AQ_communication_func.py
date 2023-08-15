import ipaddress
import struct
from AQ_parse_func import swap_modbus_bytes, remove_empty_bytes, reverse_modbus_registers
from pymodbus.file_message import ReadFileRecordRequest
from Crypto.Cipher import DES


def read_parameter(client, slave_id, modbus_reg, reg_count, param_type, byte_size):
    # Установка параметров подключения
    client.connect()

    # Выполняем запрос
    response = client.read_holding_registers(modbus_reg, reg_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    if param_type == 'unsigned':
        if byte_size == 1:
            param_value = struct.unpack('>H', byte_array)[0]
        elif byte_size == 2:
            param_value = struct.unpack('>H', byte_array)[0]
        elif byte_size == 4:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]
        elif byte_size == 6: # MAC address
            byte_array = reverse_modbus_registers(byte_array)
            param_value = byte_array # struct.unpack('>I', byte_array)[0]
        elif byte_size == 8:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>Q', byte_array)[0]
    elif param_type == 'signed':
        if byte_size == 1:
            param_value = struct.unpack('b', byte_array[1])[0]
        elif byte_size == 2:
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
        elif byte_size == 4 or byte_size == 8:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = int.from_bytes(byte_array, byteorder='big', signed=True)
    elif param_type == 'string':
        byte_array = swap_modbus_bytes(byte_array, reg_count)
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
        byte_array = swap_modbus_bytes(byte_array, reg_count)
        param_value = struct.unpack('f', byte_array)[0]
    elif param_type == 'date_time':
        if byte_size == 4:
            byte_array = reverse_modbus_registers(byte_array)
            param_value = struct.unpack('>I', byte_array)[0]

    client.close()

    return param_value


def write_parameter(client, slave_id, modbus_reg, param_type, visual_type, byte_size, value):
    # Установка параметров подключения
    client.connect()

    if param_type == 'unsigned':
        if byte_size == 1:
            packed_data = struct.pack('H', value)
        elif byte_size == 2:
            packed_data = struct.pack('H', value)
        elif byte_size == 4:
            if visual_type == 'ip_format':
                # Разделяем IP-адрес на октеты
                octets = value.split('.')
                # Преобразуем каждый октет в числовое значение
                int_octets = [int(octet) for octet in octets]
                # Получаем 32-битное целое число из октетов
                ip_as_integer = (int_octets[0] << 24) | (int_octets[1] << 16) | (int_octets[2] << 8) | int_octets[3]
                # Формируем регистры для передачи IP-адреса
                packed_data = struct.pack('I', ip_as_integer)
            else:
                packed_data = struct.pack('I', value)
        elif byte_size == 6: # MAC address
            packed_data = struct.pack('H', value)
        elif byte_size == 8:
            packed_data = struct.pack('Q', value)
        # Разбиваем упакованные данные на 16-битные значения (2 байта)
        registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
    elif param_type == 'signed':
        if byte_size == 1:
            packed_data = struct.pack('h', value)
        elif byte_size == 2:
            packed_data = struct.pack('h', value)
        elif byte_size == 4:
            packed_data = struct.pack('i', value)
        elif byte_size == 8:
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
        if byte_size == 4:
            packed_data = struct.pack('I', value)
            registers = [struct.unpack('H', packed_data[i:i + 2])[0] for i in range(0, len(packed_data), 2)]
        else:
            packed_data = struct.pack('H', value)
            registers = struct.unpack('H', packed_data)
    elif param_type == 'float':
        # Преобразование float в 16-битные значения (short int)
        # Здесь используется формат 'e' для представления float
        # в виде числа с плавающей запятой в формате IEEE 754
        if byte_size == 4:
            floats = struct.pack('f', value)
            registers = struct.unpack('HH', floats)  # Возвращает два short int значения
        elif byte_size == 8:
            floats_doubble = struct.pack('d', value)
            registers = struct.unpack('HHHH', floats_doubble)  # Возвращает два short int значения
    # elif param_type == 'date_time':
    #     if byte_size == 4:
    #         byte_array = reverse_modbus_registers(byte_array)
    #         param_value = struct.unpack('>I', byte_array)[0]

    client.write_registers(modbus_reg, registers, slave_id)

    client.close()


def read_device_name(client, slave_id):
    # Установка параметров подключения
    client.connect()
    # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
    start_address = 0xF000
    register_count = 16
    # Выполняем запрос
    response = client.read_holding_registers(start_address, register_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    byte_array = swap_modbus_bytes(byte_array, register_count)
    # Расшифровуем в строку
    text = byte_array.decode('ANSI')
    device_name = remove_empty_bytes(text)

    client.close()

    return device_name


def read_version(client, slave_id):
    # Установка параметров подключения
    client.connect()
    # Читаем 16 регистров начиная с адреса 0xF010 (soft version)
    start_address = 0xF010
    register_count = 16
    # Выполняем запрос
    response = client.read_holding_registers(start_address, register_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    byte_array = swap_modbus_bytes(byte_array, register_count)
    # Расшифровуем в строку
    text = byte_array.decode('ANSI')
    version = remove_empty_bytes(text)

    client.close()

    return version


def read_serial_number(client, slave_id):
    # Установка параметров подключения
    client.connect()
    # Читаем 16 регистров начиная с адреса 0xF086 (serial_number)
    start_address = 0xF086
    register_count = 16
    # Выполняем запрос
    response = client.read_holding_registers(start_address, register_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    byte_array = swap_modbus_bytes(byte_array, register_count)
    # Расшифровуем в строку
    text = byte_array.decode('ANSI')
    # Обрезаем дляну до 20 символов
    text = text[:20]
    serial_number = remove_empty_bytes(text)

    client.close()

    return serial_number


def read_default_prg(client, slave_id):
    # Создание экземпляра структуры ReadFileRecordRequest
    request = ReadFileRecordRequest(slave_id)
    # Установка значений полей структуры
    request.file_number = 0xFFE0
    request.record_number = 0
    request.record_length = 124

    result = client.read_file_record(slave_id, [request])

    # Закрытие соединения с Modbus-устройством
    # client.close()

    encrypt_res = result.records[0].record_data

    try:
        decrypt_res = decrypt_data(b'superkey', encrypt_res)
    except:
        return 'decrypt_err' # Помилка дешифрування
    # Получаем длину default_prg зашитую во вторые 4 байта заголовка
    file_size = int.from_bytes((decrypt_res[4:8][::-1]), byteorder='big')
    # Получаем колличество необходимых запросов по 124 записи
    req_count = ((file_size // 2) // 124)
    if (file_size // 2) % 124 or file_size % 2:
        req_count = req_count + 1

    encrypt_file = bytearray()

    for i in range(req_count):
        request.record_number = i * 124  # Установка значения record_number

        result = client.read_file_record(1, [request])
        encrypt_file += result.records[0].record_data
        # Обрезаем длину файла до вычитанной из заголовка, в конце последнего пакета мусор
        encrypt_file = encrypt_file[:file_size]

    try:
        # Перевірка на кратність 8 байтам, потрібно для DES
        if (len(encrypt_file) % 8) > 0:
            padding = 8 - (len(encrypt_file) % 8)
            encrypt_file = encrypt_file + bytes([padding] * padding)
        decrypt_file = decrypt_data(b'superkey', encrypt_file)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    # except:
    #     return 'decrypt_err' # Помилка дешифрування

    filename = 'default.prg'  # Имя файла с расширением .prg
    with open(filename, 'wb') as file:
        file.write(decrypt_file)

    return decrypt_file


def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def decrypt_data(iv, encrypted_data):
    # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
    key = b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  #0x23B246FCA76F5524

    # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные

    return decrypted_data