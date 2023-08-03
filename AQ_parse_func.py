import array
import struct
from PyQt5.QtCore import Qt
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

    # Разбиваем байты на строки по символу '\x00' и преобразуем их в строки
    string_array = string_area.split(b'\x00')
    string_array = [string.decode('cp1251') for string in string_array]

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
    tree_model.setColumnCount(6)
    tree_model.setHorizontalHeaderLabels(["Name", "Value", "Lower limit", "Upper limit", "Unit", "Default value"])

    # Создание корневого элемента
    root_item = tree_model.invisibleRootItem()

    err_check = add_nodes(root_item, node_area, cache_descr_offsets, descr_area, prop_area, string_array)
    if err_check == -1:
        return -1

    return tree_model

def add_nodes(root_item, node_area, cache_descr_offsets, descr_area, prop_area, string_array):
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
    # Кількість єлементів у каталозі
    row_count = 0

    while pos < len(node_area):
        # Проверка на is_katalog
        is_catalog_check = int.from_bytes((node_area[pos:pos + 2][::-1]), byteorder='big')
        # 0xFFFF - признак конца каталога, 0x8000 - признак каталога (самый старший бит равен 1)
        if is_catalog_check & 0x8000 and is_catalog_check != 0xFFFF:
            num_descr = int.from_bytes((node_area[pos + 4:pos + 6][::-1]), byteorder='big')
            descr_offset = cache_descr_offsets[num_descr]
            descr_size = descr_area[descr_offset]
            param_descr = descr_area[descr_offset:descr_offset + descr_size + 1]
            prop_adr = int.from_bytes((node_area[pos:pos + 2][::-1]), byteorder='big')
            prop_pos = prop_adr * 4
            param_prop = prop_area[prop_pos:prop_pos + 4]
            hex_sequence = param_prop.hex()
            catalog_attributes = unpack_descr(param_descr, param_prop)
            catalog_attributes['is_catalog'] = 1
            # Перевірка на атрибут невидимості (3й біт - ознака невидимості)
            if catalog_attributes.get('invis_and_net', 0) & 0x4:
                pos = pos + 6
                invisible_catalog_flag += 1
                continue
            # Друга перевірка на невидимість (останні версії контейнерної не додають ім'я, якщо каталог невидимий)
            if catalog_attributes.get('name', 0) == 0:
                pos = pos + 6
                invisible_catalog_flag += 1
                continue
            # Примусове ігнорування контейнеру індус-клауд
            if catalog_attributes.get('name', 0) == 'OwenCloud':
                pos = pos + 6
                invisible_catalog_flag += 1
                continue
            # Создание элемента каталога
            current_catalog = QStandardItem(catalog_attributes.get('name', 'err_name'))
            current_catalog_levels.append(current_catalog)
            level += 1

            pos = pos + 6
        elif is_catalog_check == 0xFFFF:
            if invisible_catalog_flag:
                invisible_catalog_flag -= 1
            else:
                level -= 1
                # кінець дерева (доробити)
                if level < 0:
                    return 0
                if level == 0:
                    current_catalog_levels[level].setFlags(Qt.ItemIsEnabled)
                    catalogs.append(current_catalog_levels[level])  # Добавление каталога в конец массива
                    # Создаем элементы внутри второго каталога
                    root_item.appendRow(current_catalog_levels[level])
                    del current_catalog_levels[-1]
                    catalog_cnt += 1
                    row_count = 0
                else:
                    # name та cat_name змінні для зручної відладки, у паргсінгу участі не приймають
                    name = current_catalog_levels[level].text()
                    cat_name = current_catalog_levels[level - 1].text()
                    current_catalog_levels[level - 1].appendRow(current_catalog_levels[level])
                    row_count += 1
                    del current_catalog_levels[-1]

            pos = pos + 2
        else:
            if not invisible_catalog_flag:
                num_descr = int.from_bytes((node_area[pos + 4:pos + 6][::-1]), byteorder='big')
                descr_offset = cache_descr_offsets[num_descr]
                descr_size = descr_area[descr_offset]
                param_descr = descr_area[descr_offset:descr_offset + descr_size + 1]
                prop_adr = int.from_bytes((node_area[pos:pos + 2][::-1]), byteorder='big')
                prop_pos = prop_adr * 4
                param_prop = prop_area[prop_pos:prop_pos + 4]
                param_attributes = unpack_descr(param_descr, param_prop)
                if param_attributes == -1:
                    return -1 # Помилка
                # Перевірка на атрибут невидимості (3й біт - ознака невидимості)
                if param_attributes.get('invis_and_net', 0) & 0x4:
                    pos = pos + 8
                    continue
                # Друга перевірка на невидимість (останні версії контейнерної не додають ім'я, якщо каталог невидимий)
                if catalog_attributes.get('name', 0) == 0:
                    pos = pos + 8
                    continue
                parameter_name = param_attributes.get('name', 'err_name')
                current_parameter = QStandardItem(parameter_name)
                current_parameter.setData(param_attributes, Qt.UserRole)

                delegate_attributes = {}
                cur_par_value = QStandardItem()
                if param_attributes.get('type') == 'enum':
                    enum_srtings = []
                    string_num = param_attributes.get('string_num', '')
                    bit_size = param_attributes.get('param_size', 0)
                    max_lim_from_bits = 2**bit_size - 1
                    enum_max_lim = param_attributes.get('max_limit', 0)

                    if enum_max_lim > max_lim_from_bits or enum_max_lim == 0:
                        enum_max_lim = max_lim_from_bits
                    delegate_attributes['type'] = param_attributes.get('type')
                    delegate_attributes['enum_max_lim'] = enum_max_lim
                    for i in range(enum_max_lim + 1):
                        enum_str = string_array[string_num + i]
                        enum_srtings.append(enum_str)
                    delegate_attributes['enum_strings'] = enum_srtings
                    delegate_attributes['R_Only'] = param_attributes.get('R_Only')
                    delegate_attributes['W_Only'] = param_attributes.get('W_Only')
                    cur_par_value.setData(delegate_attributes, Qt.UserRole)


                if param_attributes.get('type', '') == 'enum' or param_attributes.get('visual_type', '') == 'ip_format':
                    cur_par_min = QStandardItem()
                else:
                    if param_attributes.get('min_limit', '') == '':
                        param_type = param_attributes.get('type', '')
                        size = param_attributes.get('param_size', 0)
                        if param_type == 'float':
                            if size == 4:
                                cur_par_min = QStandardItem('-3.402283E+38')
                            elif size == 8:
                                cur_par_min = QStandardItem('-1.7976931348623E+308')
                        elif param_type == 'signed':
                            if size == 1:
                                cur_par_min = QStandardItem('-127')
                            if size == 2:
                                cur_par_min = QStandardItem('-32768')
                            if size == 4:
                                cur_par_min = QStandardItem('-2147483648')
                            if size == 8:
                                cur_par_min = QStandardItem('-9223372036854775808')
                        elif param_type == 'unsigned':
                            cur_par_min = QStandardItem('0')
                        else:
                            cur_par_min = QStandardItem()
                    else:
                        cur_par_min = QStandardItem(str(param_attributes.get('min_limit', '')))

                if param_attributes.get('type', '') == 'enum'  or param_attributes.get('visual_type', '') == 'ip_format':
                    cur_par_max = QStandardItem()
                else:
                    if param_attributes.get('max_limit', '') == '':
                        param_type = param_attributes.get('type', '')
                        size = param_attributes.get('param_size', 0)
                        if param_type == 'float':
                            if size == 4:
                                cur_par_max = QStandardItem('3.402283E+38')
                            elif size == 8:
                                cur_par_max = QStandardItem('1.7976931348623E+308')
                        elif param_type == 'signed':
                            if size == 1:
                                cur_par_max = QStandardItem('128')
                            if size == 2:
                                cur_par_max = QStandardItem('32767')
                            if size == 4:
                                cur_par_max = QStandardItem('2147483647')
                            if size == 8:
                                cur_par_max = QStandardItem('9223372036854775807')
                        elif param_type == 'unsigned':
                            if size == 1:
                                cur_par_max = QStandardItem('255')
                            if size == 2:
                                cur_par_max = QStandardItem('65535')
                            if size == 4:
                                cur_par_max = QStandardItem('4294967295')
                            if size == 8:
                                cur_par_max = QStandardItem('18446744073709551615')
                        else:
                            cur_par_max = QStandardItem()
                    else:
                        cur_par_max = QStandardItem(str(param_attributes.get('max_limit', '')))

                string_num = param_attributes.get('string_num', '')
                if string_num == '' or param_attributes.get('type', '') == 'enum':
                    cur_par_unit = QStandardItem()
                else:
                    unit_str = string_array[string_num]
                    cur_par_unit = QStandardItem(unit_str)

                if param_attributes.get('type', '') == 'enum':
                    string_num = param_attributes.get('string_num', '')
                    r_only = param_attributes.get('R_Only', 0)
                    w_only = param_attributes.get('W_Only', 0)
                    if string_num == '' or (r_only == 1 and w_only == 0):
                        cur_par_default = QStandardItem()
                    else:
                        def_str = string_array[string_num]
                        cur_par_default = QStandardItem(def_str)
                elif param_attributes.get('visual_type', '') == 'ip_format':
                    cur_par_default = QStandardItem()
                else:
                    cur_par_default = QStandardItem(str(param_attributes.get('def_value', '')))

                current_parameter.setFlags(current_parameter.flags() & ~Qt.ItemIsEditable)
                cur_par_min.setFlags(cur_par_min.flags() & ~Qt.ItemIsEditable)
                cur_par_max.setFlags(cur_par_max.flags() & ~Qt.ItemIsEditable)
                cur_par_unit.setFlags(cur_par_unit.flags() & ~Qt.ItemIsEditable)
                cur_par_default.setFlags(cur_par_default.flags() & ~Qt.ItemIsEditable)

                # name та cat_name змінні для зручної відладки, у паргсінгу участі не приймають
                name = current_parameter.text()
                cat_name = current_catalog_levels[level - 1].text()
                current_catalog_levels[level - 1].appendRow([current_parameter, cur_par_value, cur_par_min, cur_par_max,
                                                             cur_par_unit, cur_par_default])

                pos = pos + 8
            else:
                pos = pos + 8


def unpack_descr (param_descr, param_prop):
    param_attributes = {}  # Создание пустого словаря
    base_types = int.from_bytes((param_prop[0:2][::-1]), byteorder='big')
    hex_sequence = param_prop[0:4][::-1].hex()
    type = base_types & 0xF
    if type == 0:
        type = 'float'
    elif type == 1:
        type = 'fix_point_float'
    elif type == 2:
        type = 'unsigned'
    elif type == 3:
        type = 'signed'
    elif type == 4:
        type = 'enum'
    elif type == 5:
        type = 'date_time'
    elif type == 6:
        type = 'date'
    elif type == 7:
        type = 'time'
    elif type == 8:
        type = 'string'
    elif type == 9:
        type = 'stream'
    else:
        return -1  # Помилка
    param_attributes['type'] = type
    param_size = (base_types & 0x7F0) >> 4
    param_attributes['param_size'] = param_size
    packed = (base_types & 0x800) >> 11
    param_attributes['packed'] = packed
    W_Only = (base_types & 0x1000) >> 12
    param_attributes['W_Only'] = W_Only
    R_Only = (base_types & 0x2000) >> 13
    param_attributes['R_Only'] = R_Only
    is_operative = (base_types & 0x4000) >> 14
    param_attributes['is_operative'] = is_operative
    is_complex_type = (base_types & 0x2000) >> 15
    param_attributes['is_complex_type'] = is_complex_type


    descr_size = param_descr[0]
    pos = 1
    while pos < descr_size:
        ID = param_descr[pos]
        pos = get_param_by_ID(param_descr, ID, pos + 1, param_attributes)
        if pos == -1:
            return -1 # Помилка - невідомий дескриптор

    return param_attributes



def get_param_by_ID (param_descr, ID, pos, param_attributes):
    if ID == 0:
        # Атрибути відображення та доступу по мережі
        attr = param_descr[pos]
        pos += 1
        param_attributes['invis_and_net'] = attr
        # Для атрибуту невидимості повертаємо його значення (обробка та ігнорування парметру реалізовуюється
        # тим, хто викликає get_param_by_ID)
        return pos
    elif ID == 1:
        # Хеш ім'я параметру (спадщина від індус-протокол)
        indus_hash = int.from_bytes((param_descr[pos:pos + 4][::-1]), byteorder='big')
        pos += 4
        param_attributes['indus_hash'] = indus_hash
        return pos
    elif ID == 2:
        # Індекс параметру (спадщина від індус-протокол)
        indus_index = int.from_bytes((param_descr[pos:pos + 2][::-1]), byteorder='big')
        pos += 2
        param_attributes['indus_index'] = indus_index
        return pos
    elif ID == 3:
        # Номер регістру Modbus
        modbus_reg = int.from_bytes((param_descr[pos:pos + 2][::-1]), byteorder='big')
        pos += 2
        param_attributes['modbus_reg'] = modbus_reg
        return pos
    elif ID == 4:
        # Пароль доступу до параметру (число від 1 до 65535)
        param_pass = int.from_bytes((param_descr[pos:pos + 2][::-1]), byteorder='big')
        pos += 2
        param_attributes['param_pass'] = param_pass
        return pos
    elif ID == 5:
        # Кількість знаків до/після коми (число від -127 до +128)
        decimal_point = param_descr[pos]
        pos += 1
        param_attributes['decimal_point'] = decimal_point
        return pos
    elif ID == 6:
        # Значення за замовчуванням
        if param_attributes.get('type', 0) == 0:
            return -1  # Помилка
        elif param_attributes.get('type', 0) == 'string': # 8 - string
            str_length = param_descr[pos]
            def_string_b = param_descr[pos + 1:pos + 1 + str_length]
            def_string = def_string_b.decode('cp1251')
            pos = pos + 1 + str_length
            param_attributes['def_value'] = def_string
        elif param_attributes.get('type', 0) == 'enum':
            def_index = param_descr[pos]
            pos = pos + 1
            param_attributes['def_value'] = def_index
        else:
            size = param_attributes.get('param_size', 0)
            param_type = param_attributes.get('type', 0)
            if size == 0:
                return -1  # Помилка

            def_value = get_float_signed_unsigned_by_size(param_descr, pos, size, param_type)
            pos += param_attributes.get('param_size', 0)
            param_attributes['def_value'] = def_value
        return pos
    elif ID == 7:
        # Мінімальне значення
        if param_attributes.get('type', 0) == 0:
            return -1  # Помилка
        elif param_attributes.get('type', 0) == 'enum':
            def_index = param_descr[pos]
            pos = pos + 1
            param_attributes['min_limit'] = def_index
        else:
            size = param_attributes.get('param_size', 0)
            param_type = param_attributes.get('type', 0)
            if size == 0:
                return -1  # Помилка

            min_limit = get_float_signed_unsigned_by_size(param_descr, pos, size, param_type)
            pos += size
            param_attributes['min_limit'] = min_limit
        return pos
    elif ID == 8:
        # Максимальне значення
        if param_attributes.get('type', 0) == 0:
            return -1  # Помилка
        elif param_attributes.get('type', 0) == 'enum':
            def_index = param_descr[pos]
            pos = pos + 1
            param_attributes['max_limit'] = def_index
        else:
            size = param_attributes.get('param_size', 0)
            param_type = param_attributes.get('type', 0)
            if size == 0:
                return -1  # Помилка

            max_limit = get_float_signed_unsigned_by_size(param_descr, pos, size, param_type)
            pos += param_attributes.get('param_size', 0)
            param_attributes['max_limit'] = max_limit
        return pos
    elif ID == 9:
        # Формат відображення
        visual_type = param_descr[pos]
        if visual_type == 0:
            visual_type = 'dec'
        elif visual_type == 1:
            visual_type = 'hex'
        elif visual_type == 2:
            visual_type = 'bin'
        elif visual_type == 3:
            visual_type = 'dec_with_err'
        elif visual_type == 4:
            visual_type = 'ip_format'
        else:
            return -1 # Помилка
        pos += 1
        param_attributes['visual_type'] = visual_type
        return pos
    elif ID == 0xA:
        # Номер строкового параматру
        string_num = int.from_bytes((param_descr[pos:pos + 2][::-1]), byteorder='big')
        pos += 2
        param_attributes['string_num'] = string_num
        return pos
    elif ID == 0xB:
        # Примусове додавання каналу CoDeSys (тимчасово просто зміщюемо pos)
        pos += 1
        return pos
    elif ID == 0xD:
        # UID
        pre_UID = param_descr[pos:pos + 4]
        UID = int.from_bytes(pre_UID[::-1], byteorder='big')
        pos += 4
        param_attributes['UID'] = UID
        return pos
    elif ID == 0xE:
        # Розширені атрибути доступу по мережі (MQTT)
        mqtt_mask = param_descr[pos]
        pos += 1
        param_attributes['mqtt_mask'] = mqtt_mask
        return pos
    elif ID == 0xF:
        # Ознака та пріорітет оперативного параметру зовнішнього модуля (ext_modules)
        ext_modul_prio = param_descr[pos]
        pos += 1
        param_attributes['ext_modul_prio'] = ext_modul_prio
        return pos
    elif ID == 0x81 or ID == 0x82 or ID == 0x83 or ID == 0x84:
        # Ім'я параметру
        name_length = param_descr[pos]
        parameter_name_b = param_descr[pos + 1:pos + 1 + name_length]
        parameter_name = parameter_name_b.decode('cp1251')
        pos = pos + 1 + name_length
        param_attributes['name'] = parameter_name
        return pos
    elif ID == 0xD0 or ID == 0xD1 or ID == 0xD2 or ID == 0xD3 or ID == 0xD4:
        # Посилання на ім'я вузла на різних мовах (невідомий дескриптор, поки що, пропускаємо)
        pos = pos + 2
        return pos
    elif ID == 0x20 or ID == 0x21 or ID == 0x22 or ID == 0x23:
        # Ім'я параметру для зовнішнього представлення MQTT та ін.
        mqtt_name_length = param_descr[pos]
        mqtt_parameter_name_b = param_descr[pos + 1:pos + 1 + mqtt_name_length]
        mqtt_parameter_name = mqtt_parameter_name_b.decode('cp1251')
        pos = pos + 1 + mqtt_name_length
        param_attributes['mqtt_name'] = mqtt_parameter_name
        return pos
    else:
        return -1 # Помилка, невідомий дескриптор


def get_float_signed_unsigned_by_size(param_descr, pos, size, param_type):
    if param_type == 'float':
        if size == 4:
            # Распаковка в формате "f" (float)
            result = struct.unpack('f', param_descr[pos:pos + size])
            value = result[0]
        if size == 8:
            # Распаковка в формате "d" (double)
            result = struct.unpack('d', param_descr[pos:pos + size])
            value = result[0]
    elif param_type == 'signed':
        if size == 1:
            # Распаковка в формате "b" (int8)
            result = struct.unpack('b', param_descr[pos:pos + size])
            value = result[0]
        if size == 2:
            # Распаковка в формате "h" (int16)
            result = struct.unpack('h', param_descr[pos:pos + size])
            value = result[0]
        if size == 4:
            # Распаковка в формате "i" (int32)
            result = struct.unpack('i', param_descr[pos:pos + size])
            value = result[0]
        if size == 8:
            # Распаковка в формате "q" (int64)
            result = struct.unpack('q', param_descr[pos:pos + size])
            value = result[0]
    else:
        value = int.from_bytes((param_descr[pos:pos + size][::-1]), byteorder='big')

    return value
