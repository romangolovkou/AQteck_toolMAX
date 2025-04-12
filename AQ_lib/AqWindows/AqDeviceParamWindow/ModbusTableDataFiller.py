from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from typing import List

from AqBaseTreeItems import AqModbusItem

def set_modbus_header(table: QTableWidget):

    header_lables = [u"Parameter",
                     u"Group",
                     u"Address (dec)",
                     u"Address (hex)",
                     u"Number of registers",
                     u"Read function",
                     u"Write function",
                     u"Data type"]

    table.setColumnCount(8)

    for index in range(8):
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText(QCoreApplication.translate("DeviceParamListWidget", header_lables[index], None))
        table.setHorizontalHeaderItem(index, __qtablewidgetitem)


def fill_table_with_modbus_items(table: QTableWidget, param_list: List[AqModbusItem]):

    set_modbus_header(table)

    table.setRowCount(len(param_list))

    for index in range(len(param_list)):
        row = create_new_row_for_table_view(param_list[index])
        for column in range(8):
            table.setItem(index, column, row[column])


def create_new_row_for_table_view(item):
    parameter_attributes = item.data(Qt.UserRole)

# Parameter
    param_item = QTableWidgetItem(parameter_attributes.get('name', 'name_error'))

# Group
    catalog_item = item.parent()
    cat_attributes = catalog_item.data(Qt.UserRole)
    group_name = cat_attributes.get('name', 'err_name')

    group_item = QTableWidgetItem(group_name)

# Address (dec)
    reg_num_dec = parameter_attributes.get('modbus_reg', 'reg_error')
    adr_dec_item = QTableWidgetItem(str(reg_num_dec))
    adr_dec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# Address (hex)
    if reg_num_dec != 'reg_error':
        reg_num_hex = '0x{:04X}'.format(reg_num_dec)
    else:
        reg_num_hex = 'reg_error'
    adr_hex_item = QTableWidgetItem(reg_num_hex)
    adr_hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# Number of registers
    param_size = parameter_attributes.get('param_size', None)
    param_type = parameter_attributes.get('type', "type_error")
    # TODO: снова этот костыль тут
    if param_type == 'enum':
        if param_size > 16:
            reg_count = 2
            byte_size = 4
        else:
            reg_count = 1
            byte_size = 1
    else:
        byte_size = param_size
        if byte_size < 2:
            reg_count = 1
        else:
            reg_count = byte_size // 2
    reg_count_item = QTableWidgetItem(str(reg_count))
    reg_count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# Read function
    read_func_item = QTableWidgetItem(str(parameter_attributes.get('read_func', '-')))
    read_func_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# Write function
    write_func_item = QTableWidgetItem(str(parameter_attributes.get('write_func', '-')))
    write_func_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# Data type
    if param_type == 'type_error':
        bit_size = ''
    if param_type == 'enum':
        max_limit = parameter_attributes.get('max_limit', None)
        if max_limit is not None:
            bit_size = max_limit + 1
        else:
            bit_size = parameter_attributes.get('param_size', None)
            if bit_size is not None:
                bit_size = 2 ** bit_size - 1
            else:
                bit_size = 'err'
    else:
        byte_size = parameter_attributes.get('param_size', None)
        if byte_size is not None:
            bit_size = byte_size * 8
        else:
            bit_size = 'err'
    data_type_item = QTableWidgetItem(param_type + ' ' + str(bit_size))

    row_items = [param_item, group_item, adr_dec_item, adr_hex_item,
                 reg_count_item, read_func_item, write_func_item, data_type_item]

    for item in row_items:
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    return row_items
