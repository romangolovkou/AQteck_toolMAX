import array
def swap_modbus_bytes(data, num_pairs):
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
            # temp = data[start_index]
            # data[start_index] = data[end_index]
            # data[end_index] = temp

    if str_flag:
        data = data.hex()  # Преобразуем массив байт в строку
    if bytes_flag:
        data = bytes(data)

    return data


def remove_empty_bytes(string):
    # Используем метод rstrip() для удаления пустых байтов справа
    cleaned_string = string.rstrip('\x00')
    return cleaned_string


def get_conteiners_count(default_prg):
    conteiners_count = int.from_bytes((default_prg[16:20][::-1]), byteorder='big')
    return conteiners_count

def get_containers_offset(default_prg):
    # Позиция начала первого контейнера после заголовка
    pos = 20
    containers_count = get_conteiners_count(default_prg)
    containers_offset = array.array('l', [0] * 32)
    for i in range(0, containers_count):
        containers_offset[i] = pos
        container_size = int.from_bytes((default_prg[pos + 4:pos + 8][::-1]), byteorder='big')
        pos += container_size

    return containers_offset


def get_storage_container(default_prg, containers_offset):
    pos = get_last_nonzero_element(containers_offset)
    ID = int.from_bytes((default_prg[pos:pos + 4][::-1]), byteorder='big')
    container_size = int.from_bytes((default_prg[pos + 4:pos + 8][::-1]), byteorder='big')
    storage_container = default_prg[pos:pos + container_size]
    in_size = int.from_bytes((storage_container[16:20][::-1]), byteorder='big')
    out_size = int.from_bytes((storage_container[20:24][::-1]), byteorder='big')
    area_count = int.from_bytes((storage_container[36:40][::-1]), byteorder='big')
    # 40 - позиция начала поля area (в исходках контейнерной, см. storage_container),
    # 8 - размер стркутуры SYNC_TABLE_AREA (в исходках контейнерной, см. containers.h)
    header_pos = 40 + (8 * area_count) + out_size + in_size
    # 66 - размер EXP_CONF_HEADER (в исходках контейнерной, см. EXP_CONF.h)
    exp_conf_header = storage_container[header_pos:header_pos + 66]
    # +2 - размер значения размера области свойств
    pos_prop_area = header_pos + 66 + 2
    size_prop_area = int.from_bytes((storage_container[pos_prop_area:pos_prop_area + 2][::-1]), byteorder='big')
    node_offset = int.from_bytes((exp_conf_header[56:60][::-1]), byteorder='big')
    str_offset = int.from_bytes((exp_conf_header[60:64][::-1]), byteorder='big')
    pos_node_area = header_pos + node_offset + 2
    size_node_area = int.from_bytes((storage_container[pos_node_area - 2:pos_node_area][::-1]), byteorder='big')
    pos_descr_area = pos_node_area + size_node_area + 2
    size_descr_area = int.from_bytes((storage_container[pos_descr_area - 2:pos_descr_area][::-1]), byteorder='big')
    pos_string_area = header_pos + str_offset + 2
    size_string_area = int.from_bytes((storage_container[pos_string_area - 2:pos_string_area][::-1]), byteorder='big')

    test_area = storage_container[header_pos + 66:header_pos + 66 + 30]

    return storage_container


def get_last_nonzero_element(arr):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] != 0:
            return arr[i]

    # Если все элементы равны 0, возвращаем None или другое значение по умолчанию
    return None

