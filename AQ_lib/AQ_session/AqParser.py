from PySide6.QtCore import Qt

from AQ_CustomTreeItems import AqCatalogItem
from AQ_ParseFunc import get_conteiners_count, get_containers_offset, get_storage_container, parse_tree
from AQ_TreeViewItemModel import AQ_TreeItemModel
from AQ_ModbusGenericItems import *


def parse_config(configuration, conf_type=None):
    if conf_type is not None:
        if conf_type == 'default_prg':
            return parse_default_prg(configuration)
        elif conf_type == 'csv':
            return parse_config_csv(configuration)
        else:
            raise Exception('AqParserError: unknown "conf_type"')
    else:
        if isinstance(configuration, bytes):
            return parse_default_prg(configuration)
        elif isinstance(configuration, list):
            return parse_config_csv(configuration)
        else:
            raise Exception('AqParserError: unknown configuration type')



# Вынести в отдельные файлы:

def parse_default_prg(default_prg):
    try:
        containers_count = get_conteiners_count(default_prg)
        containers_offset = get_containers_offset(default_prg)
        storage_container = get_storage_container(default_prg, containers_offset)
        device_tree = parse_tree(storage_container)
        return device_tree
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 'parsing_err'

def parse_parameter(config_string: str):
    try:
        # Разделение записи на поля по символу ';'
        attributes = config_string.split(';')
        param_attributes = {}
        # Аттрибут з індексом 0 - ім'я параметру
        parameter_name = attributes[0]
        param_attributes['name'] = parameter_name
        # Аттрибут з індексом 2 - номер регістру
        param_attributes['modbus_reg'] = int(attributes[2])
        # Аттрибут з індексом 4 - номер функції для вичитки
        param_attributes['read_func'] = int(attributes[4])
        # Аттрибут з індексом 5 - номер функції для запису (необов'язковий)
        if attributes[5] == '-':
            param_attributes['R_Only'] = 1
            param_attributes['W_Only'] = 0
        else:
            param_attributes['R_Only'] = 0
            param_attributes['W_Only'] = 0
            param_attributes['write_func'] = int(attributes[5])

        # Аттрибут з індексом 7 - мінимально можливе значення (необов'язковий)
        if attributes[7] != '' and attributes[7] != '-':
            param_attributes['min_limit'] = int(attributes[7])
        # Аттрибут з індексом 8 - максимально можливе значення (необов'язковий)
        if attributes[8] != '' and attributes[8] != '-':
            param_attributes['max_limit'] = int(attributes[8])
            # Аттрибут з індексом 9 - умовні одиниці виміру параметру.
            # Має декоративне значення (необов'язковий). Приклад 'mV' '%' 'мкА' 'сек'
        param_attributes['unit'] = attributes[9]
        # Аттрибут з індексом 6 - ім'я классу параметру та розмір параметру у бітах
        parts = attributes[6].split(' ')
        param_type = parts[0]
        if param_type == 'AqModbusEnumParamItem' or param_type == 'AqModbusStringParamItem' or \
                param_type == 'AqModbusDiscretParamItem':
            param_size = int(parts[1])
        else:
            param_size = int(parts[1]) // 8
        # param_attributes['type'] = param_type
        param_attributes['param_size'] = param_size

        if attributes[10] != '' and attributes[10] != '-':
            if param_type == 'AqModbusFloatParamItem':
                param_attributes['def_value'] = float(attributes[10])
            else:
                param_attributes['def_value'] = int(attributes[10])

        if param_type == 'AqModbusEnumParamItem' or param_type == 'AqModbusFloatEnumParamItem':
            enum_strings = attributes[11].split('/')

            enum_str_dict = {}
            for row in range(len(enum_strings)):
                string_key = enum_strings[row].split('=')
                enum_str_dict[int(string_key[0])] = string_key[1]

            param_attributes['enum_strings'] = enum_str_dict

        if param_type == 'AqModbusSignedToFloatParamItem' or \
                param_type == 'AqModbusUnsignedToFloatParamItem':
            if attributes[11] != '':
                enum_strings = attributes[11].split('/')

                enum_str_dict = {}
                for row in range(len(enum_strings)):
                    string_key = enum_strings[row].split('=')
                    enum_str_dict[int(string_key[0])] = string_key[1]

                param_attributes['enum_strings'] = enum_str_dict

            multiply = float(attributes[12])
            param_attributes['multiply'] = multiply

        item_class = param_type
        if item_class is not None:
            return build_item(item_class, param_attributes)
        else:
            raise Exception('AqParserError: "item_class" not exist')
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 'parsing_err'


def build_item(item_class: str, param_attributes: dict):
    try:
        param_item = globals()[str(item_class)](param_attributes)
        return param_item
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise Exception(e)
