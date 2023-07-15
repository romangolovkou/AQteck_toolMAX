import array
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
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
    # in_size = int.from_bytes((storage_container[16:20][::-1]), byteorder='big')
    # out_size = int.from_bytes((storage_container[20:24][::-1]), byteorder='big')
    # area_count = int.from_bytes((storage_container[36:40][::-1]), byteorder='big')
    # # 40 - позиция начала поля area (в исходках контейнерной, см. storage_container),
    # # 8 - размер стркутуры SYNC_TABLE_AREA (в исходках контейнерной, см. containers.h)
    # header_pos = 40 + (8 * area_count) + out_size + in_size
    # # 66 - размер EXP_CONF_HEADER (в исходках контейнерной, см. EXP_CONF.h)
    # exp_conf_header = storage_container[header_pos:header_pos + 66]
    # # +2 - размер значения размера области свойств
    # pos_prop_area = header_pos + 66 + 2
    # size_prop_area = int.from_bytes((storage_container[pos_prop_area:pos_prop_area + 2][::-1]), byteorder='big')
    # prop_area = storage_container[pos_prop_area + 2:pos_prop_area + 2 + size_prop_area]
    # node_offset = int.from_bytes((exp_conf_header[56:60][::-1]), byteorder='big')
    # str_offset = int.from_bytes((exp_conf_header[60:64][::-1]), byteorder='big')
    # pos_node_area = header_pos + node_offset + 2
    # size_node_area = int.from_bytes((storage_container[pos_node_area - 2:pos_node_area][::-1]), byteorder='big')
    # node_area = storage_container[pos_node_area:pos_node_area + size_node_area]
    # pos_descr_area = pos_node_area + size_node_area + 2
    # size_descr_area = int.from_bytes((storage_container[pos_descr_area - 2:pos_descr_area][::-1]), byteorder='big')
    # descr_area = storage_container[pos_descr_area:pos_descr_area + size_descr_area]
    # pos_string_area = header_pos + str_offset + 2
    # size_string_area = int.from_bytes((storage_container[pos_string_area - 2:pos_string_area][::-1]), byteorder='big')
    # string_area = storage_container[pos_string_area:pos_string_area + size_string_area]
    #
    # end_pos_descr_area = pos_descr_area + size_descr_area
    # descr = 0
    # count_descr = 0
    # while(descr < size_descr_area):
    #     count_descr += 1
    #     # +1 - байт содержащий размер конкретного дескриптора
    #     descr += descr_area[descr] + 1
    #
    # cache_descr_offsets = array.array('i', [0] * count_descr)
    # pos = 0
    # for i in range(1, count_descr):
    #     cache_descr_offsets[i] = cache_descr_offsets[i - 1] + descr_area[cache_descr_offsets[i - 1]] + 1

    # test_area = storage_container[header_pos + 66:header_pos + 66 + 30]

    return storage_container


def get_last_nonzero_element(arr):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] != 0:
            return arr[i]

    # Если все элементы равны 0, возвращаем None или другое значение по умолчанию
    return None

def parse_tree(storage_container):
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
    prop_area = storage_container[pos_prop_area + 2:pos_prop_area + 2 + size_prop_area]
    node_offset = int.from_bytes((exp_conf_header[56:60][::-1]), byteorder='big')
    str_offset = int.from_bytes((exp_conf_header[60:64][::-1]), byteorder='big')
    pos_node_area = header_pos + node_offset + 2
    size_node_area = int.from_bytes((storage_container[pos_node_area - 2:pos_node_area][::-1]), byteorder='big')
    node_area = storage_container[pos_node_area:pos_node_area + size_node_area]
    pos_descr_area = pos_node_area + size_node_area + 2
    size_descr_area = int.from_bytes((storage_container[pos_descr_area - 2:pos_descr_area][::-1]), byteorder='big')
    descr_area = storage_container[pos_descr_area:pos_descr_area + size_descr_area]
    filename = 'descr_area.prg'  # Имя файла с расширением .prg
    with open(filename, 'wb') as file:
        file.write(descr_area)

    pos_string_area = header_pos + str_offset + 2
    size_string_area = int.from_bytes((storage_container[pos_string_area - 2:pos_string_area][::-1]), byteorder='big')
    string_area = storage_container[pos_string_area:pos_string_area + size_string_area]

    end_pos_descr_area = pos_descr_area + size_descr_area
    descr = 0
    count_descr = 0
    while (descr < size_descr_area):
        count_descr += 1
        # +1 - байт содержащий размер конкретного дескриптора
        descr += descr_area[descr] + 1

    cache_descr_offsets = array.array('i', [0] * count_descr)
    pos = 0
    for i in range(1, count_descr):
        cache_descr_offsets[i] = cache_descr_offsets[i - 1] + descr_area[cache_descr_offsets[i - 1]] + 1

    tree_model = QStandardItemModel()
    # Создание корневого элемента
    root_item = tree_model.invisibleRootItem()

    add_nodes(root_item, node_area, cache_descr_offsets, descr_area)

    return tree_model

def add_nodes(root_item, node_area, cache_descr_offsets, descr_area):
    pos = 6
    catalog_cnt = 0
    invisible_catalog_flag = 0
    # Создание пустого массива каталогов
    catalogs = []
    # Создаем модель и корневой элемент
    TT_names = []
    current_catalog_levels = []
    current_catalog = 0
    # Рівень вкладенності каталогу
    level = 0
    # Кількість єлементів у кталозі
    row_count = 0

    while pos < len(node_area):
        # Проверка на is_katalog
        prop = int.from_bytes((node_area[pos:pos + 2][::-1]), byteorder='big')
        # 0xFFFF - признак конца каталога, 0x8000 - признак каталога (самый старший бит равен 1)
        if prop & 0x8000 and prop != 0xFFFF:
            # Создание элемента каталога
            # Получаем имя каталога
            num_descr = int.from_bytes((node_area[pos + 4:pos + 6][::-1]), byteorder='big')
            descr_offset = cache_descr_offsets[num_descr]
            # Проверка на длину дескриптора (костыль для пропуска неизвестных дескрипторов см. "Описание дескр. каталога")
            descr_size = descr_area[descr_offset]
            if descr_size < 10:
                pos = pos + 6
                invisible_catalog_flag += 1
                continue

            lang_code = descr_area[descr_offset + 1]
            name_length = descr_area[descr_offset + 2]
            catalog_name_b = descr_area[descr_offset + 3:descr_offset + 3 + name_length]
            catalog_name = catalog_name_b.decode('cp1251')
            TT_names.append(catalog_name)
            current_catalog = QStandardItem(catalog_name)
            current_catalog.setFlags(Qt.ItemIsEnabled)
            current_catalog_levels.append(current_catalog)
            level += 1



            pos = pos + 6
        elif prop == 0xFFFF:
            if invisible_catalog_flag:
                invisible_catalog_flag -= 1
            else:
                level -= 1
                # Перевірка на корректність рівня, -1 - помилка.
                if level < 0:
                    return -1
                if level == 0:
                    current_catalog_levels[level].setRowCount(row_count)  # Указываем количество дочерних элементов
                    current_catalog_levels[level].setFlags(Qt.ItemIsEnabled)
                    catalogs.append(current_catalog_levels[level])  # Добавление каталога в конец массива
                    root_item.appendRow(current_catalog_levels[level])
                    del current_catalog_levels[-1]
                    catalog_cnt += 1
                    row_count = 0
                else:
                    current_catalog_levels[level].appendRow(current_catalog)
                    row_count += 1
                    del current_catalog_levels[-1]

            pos = pos + 2
        else:
            pos = pos + 8

