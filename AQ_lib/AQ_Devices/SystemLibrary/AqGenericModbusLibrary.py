import csv
from dataclasses import dataclass

from AQ_CustomTreeItems import AqCatalogItem
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AqParser import parse_parameter

@dataclass
class AqModbusGenericConfiguration:
    dev_descr_dict: dict
    system_params: list
    params_tree: AQ_TreeItemModel


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

    if dev_descr_dict.get('Name') is None or \
            dev_descr_dict.get('Type') is None or \
            not isinstance(params_tree, AQ_TreeItemModel):
        raise Exception('AqGenericModbusError: Configuration can`t read. "Name" or "Type" or "params_tree" not exist')

    return AqModbusGenericConfiguration(dev_descr_dict, system_params, params_tree)


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
        # єлемент з індексом 0 - ключ, єлемент з індексом 1 - значення-
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
        catalogs_name_list = list()
        for i in range(start + 1, end):
            config_string = data[i]
            # Разделение записи на поля по символу ';'
            fields = config_string.split(';')
            if fields[1] not in catalogs_name_list:
                catalogs_name_list.append(fields[1])

        # створюємо список з каталог-ітемами
        catalogs = []
        for i in range(len(catalogs_name_list)):
            param_attributes = dict()
            param_attributes['name'] = catalogs_name_list[i]
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