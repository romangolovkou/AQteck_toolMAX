import csv

from AQ_CustomTreeItems import AqCatalogItem
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AqParser import parse_parameter


def read_configuration_file(conf_filename):
    file_path = '110_device_conf/' + conf_filename
    data = []
    with open(file_path, 'r', newline='\n') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Добавляем имена из каждой ячейки строки в список
            data.append(row[0])

    dev_descr_dict = get_device_descr(data)
    system_params = get_systems_params(data)
    params_tree = get_params_tree(data)

    return {'device_descr': dev_descr_dict, 'system_params': system_params, 'params_tree': params_tree}


def get_device_descr(data: list):
    dev_descr_dict = dict()
    start = None
    end = None
    for i in range(len(data)):
        # Єлемент з індексом 0 - може містити хедер блоку (ключ початку та кінця блоку у файлі)
        config_string = data[i]
        fields = config_string.split(';')
        if fields[0] == '!Device_descr_area':
            start = i
        if fields[0] == '!/Device_descr_area':
            end = i
            break

    if start is None or end is None:
        raise Exception('AqGenericModbusError: Configuration can`t read. Can`t find "Device_descr_area" in file')

    for i in range(start + 1, end):
        config_string = data[i]
        # Разделение записи на поля по символу ';'
        fields = config_string.split(';')
        # єлемент з індексом 0 - ключ, єлемент з індексом 1 - значення
        dev_descr_dict[fields[0]] = fields[1]

    return dev_descr_dict


def get_systems_params(data: list):
    system_params_list = list()
    start = None
    end = None
    for i in range(len(data)):
        # Єлемент з індексом 0 - може містити хедер блоку (ключ початку та кінця блоку у файлі)
        config_string = data[i]
        fields = config_string.split(';')
        if fields[0] == '!System_params':
            start = i
        if fields[0] == '!/System_params':
            end = i
            break

    if start is None or end is None:
        raise Exception('AqGenericModbusError: Configuration can`t read. Can`t find "System_params" in file')

    for i in range(start + 1, end):
        config_string = data[i]

        param_item = parse_parameter(config_string)
        system_params_list.append(param_item)

    return system_params_list


def get_params_tree(data: list):
    try:
        params_tree = AQ_TreeItemModel()
        start = None
        end = None
        for i in range(len(data)):
            # Єлемент з індексом 0 - може містити хедер блоку (ключ початку та кінця блоку у файлі)
            config_string = data[i]
            fields = config_string.split(';')
            if fields[0] == '!Param_descr_area':
                start = i
            if fields[0] == '!/Param_descr_area':
                end = i
                break

        if start is None or end is None:
            raise Exception('AqGenericModbusError: Configuration can`t read. Can`t find "System_params" in file')

        # Створюємо список імен каталогів
        catalogs_name_set = set()
        for i in range(start + 1, end):
            config_string = data[i]
            # Разделение записи на поля по символу ';'
            fields = config_string.split(';')
            catalogs_name_set.add(fields[1])

        # Сортировка элементов сета в алфавитном порядке
        sorted_list = sorted(catalogs_name_set)

        # створюємо список з каталог-ітемами
        catalogs = []
        for i in range(len(sorted_list)):
            param_attributes = dict()
            param_attributes['name'] = sorted_list[i]
            param_attributes['is_catalog'] = 1
            catalog_item = AqCatalogItem(param_attributes)
            catalogs.append(catalog_item)

        # Додаємо до каталогів відповідні параметр-ітеми
        for i in range(len(catalogs)):
            cat_name = catalogs[i].text()
            for j in range(start + 1, end):
                config_string = data[j]
                # Разделение записи на поля по символу ';'
                fields = config_string.split(';')
                if fields[1] == cat_name:
                    param_item = parse_parameter(config_string)
                    catalogs[i].appendRow(param_item)

        root = params_tree.invisibleRootItem()
        for row in range(len(catalogs)):
            root.appendRow(catalogs[row])
        return params_tree
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 'parsing_err'



# def parse_device_config(device_config):
#     try:
#         # Створюємо список імен каталогів
#         catalogs_name_set = set()
#         for i in range(len(device_config)):
#             config_string = device_config[i]
#             # Разделение записи на поля по символу ';'
#             fields = config_string.split(';')
#             catalogs_name_set.add(fields[1])
#         # Сортировка элементов сета в алфавитном порядке
#         sorted_list = sorted(catalogs_name_set)
#
#         # створюємо список з каталог-ітемами
#         catalogs = []
#         for i in range(len(sorted_list)):
#             catalog_item = AqCatalogItem(sorted_list[i])
#             param_attributes = {}
#             param_attributes['name'] = sorted_list[i]
#             param_attributes['is_catalog'] = 1
#             catalog_item.setData(param_attributes, Qt.UserRole)
#             catalogs.append(catalog_item)
#
#         # Додаємо до каталогів відповідні параметр-ітеми
#         for i in range(len(catalogs)):
#             cat_name = catalogs[i].text()
#             for j in range(len(device_config)):
#                 config_string = device_config[j]
#                 # Разделение записи на поля по символу ';'
#                 fields = config_string.split(';')
#                 if fields[1] == cat_name:
#                     param_attributes = {}
#                     parameter_name = fields[0]
#                     param_attributes['name'] = parameter_name
#                     param_attributes['modbus_reg'] = int(fields[2])
#                     param_attributes['read_func'] = int(fields[4])
#                     if fields[5] == '-':
#                         param_attributes['R_Only'] = 1
#                         param_attributes['W_Only'] = 0
#                     else:
#                         param_attributes['write_func'] = int(fields[5])
#
#                     if fields[7] != '' and fields[7] != '-':
#                         param_attributes['min_limit'] = int(fields[7])
#                     if fields[8] != '' and fields[8] != '-':
#                         param_attributes['max_limit'] = int(fields[8])
#                     param_attributes['unit'] = fields[9]
#                     parts = fields[6].split(' ')
#                     param_type = parts[0]
#                     if param_type == 'enum' or param_type == 'string':
#                         param_size = int(parts[1])
#                     else:
#                         param_size = int(parts[1]) // 8
#                     param_attributes['type'] = param_type
#                     param_attributes['param_size'] = param_size
#
#                     if fields[10] != '' and fields[10] != '-':
#                         if param_type == 'float':
#                             param_attributes['def_value'] = float(fields[10])
#                         else:
#                             param_attributes['def_value'] = int(fields[10])
#
#                     if param_type == 'enum' or param_type == 'float_enum':
#                         enum_strings = fields[11].split('/')
#
#                         enum_str_dict = {}
#                         for row in range(len(enum_strings)):
#                             string_key = enum_strings[row].split('=')
#                             enum_str_dict[int(string_key[0])] = string_key[1]
#
#                         param_attributes['enum_strings'] = enum_str_dict
#
#                     if param_type == 'signed_to_float' or param_type == 'unsigned_to_float':
#                         if fields[11] != '':
#                             enum_strings = fields[11].split('/')
#
#                             enum_str_dict = {}
#                             for row in range(len(enum_strings)):
#                                 string_key = enum_strings[row].split('=')
#                                 enum_str_dict[int(string_key[0])] = string_key[1]
#
#                             param_attributes['enum_strings'] = enum_str_dict
#
#                         multiply = float(fields[12])
#                         param_attributes['multiply'] = multiply
#
#                     param_item = get_item_by_type(param_attributes.get('type', ''), parameter_name, self.packer)
#                     param_item.setData(param_attributes, Qt.UserRole)
#                     catalogs[i].appendRow(param_item)
#
#         device_tree = AQ_TreeItemModel()
#         root = device_tree.invisibleRootItem()
#         for row in range(len(catalogs)):
#             root.appendRow(catalogs[row])
#         return device_tree
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return 'parsing_err'