import ipaddress
from AQ_parse_func import swap_modbus_bytes, remove_empty_bytes


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
    text = byte_array.decode('ANSI')
    device_name = remove_empty_bytes(text)

    client.close()

    return device_name


def read_version(client, slave_id):
    # Установка параметров подключения
    client.connect()
    # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
    start_address = 0xF010
    register_count = 16
    # Выполняем запрос
    response = client.read_holding_registers(start_address, register_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    byte_array = swap_modbus_bytes(byte_array, register_count)
    text = byte_array.decode('ANSI')
    version = remove_empty_bytes(text)

    client.close()

    return version


def read_serial_number(client, slave_id):
    # Установка параметров подключения
    client.connect()
    # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
    start_address = 0xF086
    register_count = 16
    # Выполняем запрос
    response = client.read_holding_registers(start_address, register_count, slave_id)
    # Конвертируем значения регистров в строку
    hex_string = ''.join(format(value, '04X') for value in response.registers)
    # Конвертируем строку в массив байт
    byte_array = bytes.fromhex(hex_string)
    byte_array = swap_modbus_bytes(byte_array, register_count)
    text = byte_array.decode('ANSI')
    text = text[:20]
    serial_number = remove_empty_bytes(text)

    client.close()

    return serial_number

def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False