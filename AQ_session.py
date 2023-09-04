from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from AQ_window_AddDevices import AQ_DialogAddDevices
from AQ_Device import AQ_Device


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.event_manager.register_event_handler("open_AddDevices", self.open_AddDevices)
        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices)
        self.devices = []
        self.current_active_dev_index = 0

    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices(self.event_manager, self.parent)
        AddDevices_window.exec_()

    def add_new_devices(self, new_devices_list):
        for i in range(len(new_devices_list)):
            self.devices.append(new_devices_list[i])

    # def create_device_tree_for_view(self, device_tree):
    #     tree_model_for_view = QStandardItemModel()
    #     tree_model_for_view.setColumnCount(6)
    #     tree_model_for_view.setHorizontalHeaderLabels(
    #                                         ["Name", "Value", "Lower limit", "Upper limit", "Unit", "Default value"])
    #     donor_root_item = device_tree.invisibleRootItem()
    #     new_root_item = tree_model_for_view.invisibleRootItem()
    #     self.traverse_items_create_new_tree_for_view(donor_root_item, new_root_item)
    #     return
    #
    # def traverse_items_create_new_tree_for_view(self, item, new_item):
    #     for row in range(item.rowCount()):
    #         child_item = item.child(row)
    #         if child_item is not None:
    #             parameter_attributes = child_item.data(Qt.UserRole)
    #             if parameter_attributes is not None:
    #                 if parameter_attributes.get('is_catalog', 0) == 1:
    #                     name = parameter_attributes.get('name', 'err_name')
    #                     catalog = QStandardItem(name)
    #                     catalog.setData(parameter_attributes, Qt.UserRole)
    #                     self.traverse_items_create_new_tree_for_view(child_item, catalog)
    #                     new_item.appendRow(catalog)
    #                 else:
    #                     new_item.appendRow(self.create_new_row_for_tree_view(child_item))
    #
    #
    # def create_new_row_for_tree_view(self, item):
    #     parameter_attributes = item.data(Qt.UserRole)
    #     name = parameter_attributes.get('name', 'err_name')
    #     parameter_item = QStandardItem(name)
    #     parameter_item.setData(parameter_attributes, Qt.UserRole)
    #     value_item = QStandardItem()
    #     min_limit_item = self.get_min_limit_item(parameter_attributes)
    #     max_limit_item = self.get_max_limit_item(parameter_attributes)
    #     unit_item = parameter_attributes.get('unit', '')
    #     default_item = self.get_default_value_item(parameter_attributes)
    #     # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
    #     parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
    #     min_limit_item.setFlags(min_limit_item.flags() & ~Qt.ItemIsEditable)
    #     max_limit_item.setFlags(max_limit_item.flags() & ~Qt.ItemIsEditable)
    #     unit_item.setFlags(unit_item.flags() & ~Qt.ItemIsEditable)
    #     default_item.setFlags(default_item.flags() & ~Qt.ItemIsEditable)
    #
    #     return [parameter_item, value_item, min_limit_item, max_limit_item, unit_item, default_item]
    #
    # def get_min_limit_item(self, param_attributes):
    #     if param_attributes.get('min_limit', '') == '':
    #         param_type = param_attributes.get('type', '')
    #         size = param_attributes.get('param_size', 0)
    #         cur_par_min = ''
    #         if param_type == 'float':
    #             if size == 4:
    #                 cur_par_min = '-3.402283E+38'
    #             elif size == 8:
    #                 cur_par_min = '-1.7976931348623E+308'
    #         elif param_type == 'signed':
    #             if size == 1:
    #                 cur_par_min = '-127'
    #             elif size == 2:
    #                 cur_par_min = '-32768'
    #             elif size == 4:
    #                 cur_par_min = '-2147483648'
    #             elif size == 8:
    #                 cur_par_min = '-9223372036854775808'
    #         elif param_type == 'unsigned':
    #             if param_attributes.get('visual_type', '') == 'ip_format':
    #                 cur_par_min = ''
    #             else:
    #                 cur_par_min = '0'
    #         elif param_type == 'enum':
    #             cur_par_min = ''
    #         elif param_type == 'date_time':
    #             cur_par_min = '01.01.2000 0:00:00'
    #         else:
    #             cur_par_min = ''
    #         # Якщо min_limit у параметра немає, додаємо розрахунковий і у сам параметр
    #         param_attributes['min_limit'] = cur_par_min
    #
    #     min_limit_item = QStandardItem(str(param_attributes.get('min_limit', '')))
    #
    #     return min_limit_item
    #
    # def get_max_limit_item(self, param_attributes):
    #     if param_attributes.get('max_limit', '') == '':
    #         param_type = param_attributes.get('type', '')
    #         size = param_attributes.get('param_size', 0)
    #         cur_par_max = ''
    #         if param_type == 'float':
    #             if size == 4:
    #                 cur_par_max = '3.402283E+38'
    #             elif size == 8:
    #                 cur_par_max = '1.7976931348623E+308'
    #         elif param_type == 'signed':
    #             if size == 1:
    #                 cur_par_max = '128'
    #             elif size == 2:
    #                 cur_par_max = '32767'
    #             elif size == 4:
    #                 cur_par_max = '2147483647'
    #             elif size == 8:
    #                 cur_par_max = '9223372036854775807'
    #         elif param_type == 'unsigned':
    #             if param_attributes.get('visual_type', '') == 'ip_format':
    #                 cur_par_max = ''
    #             elif size == 1:
    #                 cur_par_max = '255'
    #             elif size == 2:
    #                 cur_par_max = '65535'
    #             elif size == 4:
    #                 cur_par_max = '4294967295'
    #             elif size == 6:  # MAC address
    #                 cur_par_max = 'FF:FF:FF:FF:FF:FF'
    #             elif size == 8:
    #                 cur_par_max = '18446744073709551615'
    #         elif param_type == 'enum':
    #             cur_par_max = ''
    #         elif param_type == 'date_time':
    #             cur_par_max = '07.02.2136 6:28:15'
    #         else:
    #             cur_par_max = ''
    #         # Якщо max_limit у параметра немає, додаємо розрахунковий і у сам параметр
    #         param_attributes['max_limit'] = cur_par_max
    #
    #     max_limit_item = QStandardItem(str(param_attributes.get('max_limit', '')))
    #
    #     return max_limit_item
    #
    # def get_default_value_item(self, param_attributes):
    #     cur_par_default = ''
    #     if param_attributes.get('type', '') == 'enum':
    #         string_num = param_attributes.get('string_num', '')
    #         r_only = param_attributes.get('R_Only', 0)
    #         w_only = param_attributes.get('W_Only', 0)
    #         if string_num == '' or (r_only == 1 and w_only == 0):
    #             cur_par_default = ''
    #         else:
    #             enum_strings = param_attributes.get('enum_strings', [])
    #             if len(enum_strings) > 0:
    #                 def_str = enum_strings[string_num]
    #                 cur_par_default = def_str
    #     elif param_attributes.get('visual_type', '') == 'ip_format':
    #         cur_par_default = ''
    #     else:
    #         cur_par_default = param_attributes.get('def_value', '')
    #
    #     default_value_item = QStandardItem(str(cur_par_default))
    #
    #     return default_value_item

    def read_cur_active_device(self):
        return

    def write_cur_active_device(self):
        return