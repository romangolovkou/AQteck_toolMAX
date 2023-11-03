def swap_bytes_at_registers(data, num_pairs):
    """
    The function changes the bytes at each register
    It was      - ABABABAB
    It will be  - BABABABA
    :param data: string, bytes or bytearray with data to swap
    :param num_pairs: count registers to swap
    :return: swapped string
    """
    str_flag = 0
    bytes_flag = 0

    if isinstance(data, str):
        # Преобразование строки в массив байт
        str_flag = 1
        data = bytearray.fromhex(data)
    elif isinstance(data, bytes):
        # Преобразование неизменяемого массива байт в изменяемый
        bytes_flag = 1
        data = bytearray(data)
    elif not isinstance(data, bytearray):
        raise TypeError("Data must be a string, bytes, or bytearray")

    for i in range(num_pairs):
        start_index = i * 2
        end_index = start_index + 2

        # Проверяем, что индексы не выходят за пределы массива
        if end_index <= len(data):
            # Меняем местами пару байт
            data[start_index:end_index] = data[start_index:end_index][::-1]

    if str_flag:
        data = data.hex()  # Преобразуем массив байт в строку
    if bytes_flag:
        data = bytes(data)

    return data


def swap_registers(data):
    # Проверяем, что количество байтов четное, иначе возвращаем исходный массив без изменений
    if len(data) % 4 != 0:
        return data

    swapped_data = bytearray(data)
    for i in range(0, len(swapped_data), 4):
        # Меняем местами пары байтов
        swapped_data[i:i + 4] = swapped_data[i + 2:i + 4] + swapped_data[i:i + 2]

    return swapped_data


def reverse_registers(data):
    if len(data) % 2 != 0:
        raise ValueError("The data length must be even.")

    reversed_pairs = [data[i:i+2][::-1] for i in range(0, len(data), 2)]
    return b''.join(reversed_pairs)[::-1]


def remove_empty_bytes(string):
    # Используем метод rstrip() для удаления пустых байтов справа
    cleaned_string = string.rstrip('\x00')
    return cleaned_string


