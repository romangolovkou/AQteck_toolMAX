from PyQt5.QtCore import QObject, Qt, QTimer
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFrame, QTreeView


class AQ_treeView_frame(QFrame):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.setStyleSheet("background-color: transparent;")
        self.tree_view = QTreeView(self)
        self.tree_view.setGeometry(0, 0, self.width(), self.height())
        self.tree_view_manager = AQ_treeView_manager(self.event_manager, self.tree_view, self)

    def add_tree_view(self):
        try:
            device_data = self.devices[-1]
            device_tree = device_data.get('device_tree')
            # Створення порожнього массиву параметрів
            self.parameter_list = []
            root = device_tree.invisibleRootItem()
            traverse_items(root, self.parameter_list)

            if isinstance(device_tree, QStandardItemModel):
                # Устанавливаем модель для QTreeView и отображаем его
                address = device_data.get('address')
                device_data['tree_view'] = AQ_TreeView(len(self.devices) - 1, device_tree, address, self.main_field_frame)
                device_data.get('tree_view').show()
                root = device_tree.invisibleRootItem()
                device_data.get('tree_view').traverse_items_show_delegate(root)
                device_data.get('tree_view').read_all_tree_by_modbus(root)
                self.add_dev_widget_to_left_panel(len(self.devices) - 1, device_data)

        # except:
            # print(f"Помилка парсінгу")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tree_view.setGeometry(0, 0, self.width(), self.height())

        event.accept()

class AQ_treeView_manager(QObject):
    def __init__(self, event_manager, tree_view, parent):
        super().__init__()
        self.event_manager = event_manager
        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices_trees)
        self.event_manager.register_event_handler('set_active_device', self.set_active_device_tree)
        self.tree_view = tree_view
        self.devices_view_trees = {}

    def add_new_devices_trees(self, new_devices_list):
        for i in range(len(new_devices_list)):
            device_data = new_devices_list[i].get_device_data()
            device_tree = device_data.get('device_tree', None)
            if device_tree is not None:
                device_view_tree_model = self.create_device_tree_for_view(device_tree)
                self.devices_view_trees[new_devices_list[i]] = device_view_tree_model

        self.tree_view.setModel(self.devices_view_trees[new_devices_list[-1]])

    def set_active_device_tree(self, device):
        try:
            self.tree_view.setModel(self.devices_view_trees[device])
        except:
            # Устанавливаем задержку в 50 м.сек и затем повторяем
            QTimer.singleShot(3000, lambda: self.set_active_device_tree(device))


    def create_device_tree_for_view(self, device_tree):
        tree_model_for_view = QStandardItemModel()
        tree_model_for_view.setColumnCount(6)
        tree_model_for_view.setHorizontalHeaderLabels(
                                            ["Name", "Value", "Lower limit", "Upper limit", "Unit", "Default value"])
        donor_root_item = device_tree.invisibleRootItem()
        new_root_item = tree_model_for_view.invisibleRootItem()
        self.traverse_items_create_new_tree_for_view(donor_root_item, new_root_item)
        return tree_model_for_view

    def traverse_items_create_new_tree_for_view(self, item, new_item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        name = parameter_attributes.get('name', 'err_name')
                        catalog = QStandardItem(name)
                        catalog.setData(parameter_attributes, Qt.UserRole)
                        self.traverse_items_create_new_tree_for_view(child_item, catalog)
                        new_item.appendRow(catalog)
                    else:
                        new_item.appendRow(self.create_new_row_for_tree_view(child_item))


    def create_new_row_for_tree_view(self, item):
        parameter_attributes = item.data(Qt.UserRole)
        name = parameter_attributes.get('name', 'err_name')
        parameter_item = QStandardItem(name)
        parameter_item.setData(parameter_attributes, Qt.UserRole)
        value_item = QStandardItem()
        min_limit_item = self.get_min_limit_item(parameter_attributes)
        max_limit_item = self.get_max_limit_item(parameter_attributes)
        unit_item = self.get_unit_item(parameter_attributes)
        default_item = self.get_default_value_item(parameter_attributes)
        # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
        parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
        min_limit_item.setFlags(min_limit_item.flags() & ~Qt.ItemIsEditable)
        max_limit_item.setFlags(max_limit_item.flags() & ~Qt.ItemIsEditable)
        unit_item.setFlags(unit_item.flags() & ~Qt.ItemIsEditable)
        default_item.setFlags(default_item.flags() & ~Qt.ItemIsEditable)

        return [parameter_item, value_item, min_limit_item, max_limit_item, unit_item, default_item]

    def get_min_limit_item(self, param_attributes):
        if param_attributes.get('min_limit', '') == '':
            param_type = param_attributes.get('type', '')
            size = param_attributes.get('param_size', 0)
            cur_par_min = ''
            if param_type == 'float':
                if size == 4:
                    cur_par_min = '-3.402283E+38'
                elif size == 8:
                    cur_par_min = '-1.7976931348623E+308'
            elif param_type == 'signed':
                if size == 1:
                    cur_par_min = '-127'
                elif size == 2:
                    cur_par_min = '-32768'
                elif size == 4:
                    cur_par_min = '-2147483648'
                elif size == 8:
                    cur_par_min = '-9223372036854775808'
            elif param_type == 'unsigned':
                if param_attributes.get('visual_type', '') == 'ip_format':
                    cur_par_min = ''
                else:
                    cur_par_min = '0'
            elif param_type == 'enum':
                cur_par_min = ''
            elif param_type == 'date_time':
                cur_par_min = '01.01.2000 0:00:00'
            else:
                cur_par_min = ''
            # Якщо min_limit у параметра немає, додаємо розрахунковий і у сам параметр
            param_attributes['min_limit'] = cur_par_min

        min_limit_item = QStandardItem(str(param_attributes.get('min_limit', '')))

        return min_limit_item

    def get_max_limit_item(self, param_attributes):
        if param_attributes.get('max_limit', '') == '':
            param_type = param_attributes.get('type', '')
            size = param_attributes.get('param_size', 0)
            cur_par_max = ''
            if param_type == 'float':
                if size == 4:
                    cur_par_max = '3.402283E+38'
                elif size == 8:
                    cur_par_max = '1.7976931348623E+308'
            elif param_type == 'signed':
                if size == 1:
                    cur_par_max = '128'
                elif size == 2:
                    cur_par_max = '32767'
                elif size == 4:
                    cur_par_max = '2147483647'
                elif size == 8:
                    cur_par_max = '9223372036854775807'
            elif param_type == 'unsigned':
                if param_attributes.get('visual_type', '') == 'ip_format':
                    cur_par_max = ''
                elif size == 1:
                    cur_par_max = '255'
                elif size == 2:
                    cur_par_max = '65535'
                elif size == 4:
                    cur_par_max = '4294967295'
                elif size == 6:  # MAC address
                    cur_par_max = 'FF:FF:FF:FF:FF:FF'
                elif size == 8:
                    cur_par_max = '18446744073709551615'
            elif param_type == 'enum':
                cur_par_max = ''
            elif param_type == 'date_time':
                cur_par_max = '07.02.2136 6:28:15'
            else:
                cur_par_max = ''
            # Якщо max_limit у параметра немає, додаємо розрахунковий і у сам параметр
            param_attributes['max_limit'] = cur_par_max

        max_limit_item = QStandardItem(str(param_attributes.get('max_limit', '')))

        return max_limit_item

    def get_unit_item(self, param_attributes):
        unit_item = QStandardItem(str(param_attributes.get('max_limit', '')))
        return unit_item

    def get_default_value_item(self, param_attributes):
        cur_par_default = ''
        if param_attributes.get('type', '') == 'enum':
            def_value = param_attributes.get('def_value', '')
            r_only = param_attributes.get('R_Only', 0)
            w_only = param_attributes.get('W_Only', 0)
            if def_value == '' or (r_only == 1 and w_only == 0):
                cur_par_default = ''
            else:
                enum_strings = param_attributes.get('enum_strings', [])
                if len(enum_strings) > 0:
                    def_str = enum_strings[def_value]
                    cur_par_default = def_str
        elif param_attributes.get('visual_type', '') == 'ip_format':
            cur_par_default = ''
        else:
            cur_par_default = param_attributes.get('def_value', '')

        default_value_item = QStandardItem(str(cur_par_default))

        return default_value_item
