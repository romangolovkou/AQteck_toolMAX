from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QFrame, QStackedWidget

from AQ_TreeViewItemModel import AQ_TreeViewItemModel
from AQ_custom_tree_items import AQ_param_manager_item
from AQ_tree_view import AQ_TreeView


class AQ_TreeViewFrame(QFrame):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.setStyleSheet("background-color: transparent;")
        self.tree_view_manager = AQ_treeView_manager(self.event_manager, self)
        self.tree_view_manager.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tree_view_manager.setGeometry(0, 0, self.width(), self.height())

        event.accept()

class AQ_treeView_manager(QStackedWidget):
    def __init__(self, event_manager, parent):
        super().__init__(parent)
        self.event_manager = event_manager
        self.event_manager.register_event_handler("new_devices_added", self.add_new_devices_trees)
        self.event_manager.register_event_handler('set_active_device', self.set_active_device_tree)
        self.event_manager.register_event_handler("current_device_data_updated", self.update_device_data)
        self.event_manager.register_event_handler("delete_device", self.delete_device_view)
        self.devices_views = {}

    def add_new_devices_trees(self, new_devices_list):
        for i in range(len(new_devices_list)):
            tree_view = AQ_TreeView()
            tree_view.setGeometry(0, 0, self.width(), self.height())
            device_view_tree_model = self.create_device_tree_for_view(new_devices_list[i])
            tree_view.setModel(device_view_tree_model)
            self.devices_views[new_devices_list[i]] = tree_view
            self.update_device_data(new_devices_list[i])
            self.addWidget(tree_view)
            self.show()

    def set_active_device_tree(self, device):
        if device is not None:
            try:
                widget = self.devices_views.get(device, None)
                if widget is not None:
                    self.setCurrentWidget(widget)
                    self.update_device_data(device)
            except:
                # Устанавливаем задержку в 50 м.сек и затем повторяем
                QTimer.singleShot(50, lambda: self.set_active_device_tree(device))

    def delete_device_view(self, device):
        tree_view = self.devices_views.get(device, None)
        if tree_view is not None:
            self.removeWidget(tree_view)
            tree_view.deleteLater()

    def update_device_data(self, device):
        tree_view = self.devices_views.get(device, None)
        if tree_view is not None:
            tree_view.model().update_all_params()

    def create_device_tree_for_view(self, device):
        device_data = device.get_device_data()
        device_tree = device_data.get('device_tree', None)
        if device_tree is not None:
            tree_model_for_view = AQ_TreeViewItemModel(device, self.event_manager)
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
                        catalog = AQ_param_manager_item(child_item)
                        catalog.setData(parameter_attributes, Qt.UserRole)
                        catalog.setFlags(catalog.flags() & ~Qt.ItemIsEditable)
                        self.traverse_items_create_new_tree_for_view(child_item, catalog)
                        new_item.appendRow(catalog)
                    else:
                        new_item.appendRow(self.create_new_row_for_tree_view(child_item))

    def create_new_row_for_tree_view(self, item):
        parameter_attributes = item.data(Qt.UserRole)
        name = parameter_attributes.get('name', 'err_name')

        parameter_item = AQ_param_manager_item(item)
        parameter_item.setData(parameter_attributes, Qt.UserRole)
        value_item = QStandardItem()
        min_limit_item = self.get_min_limit_item(parameter_attributes)
        max_limit_item = self.get_max_limit_item(parameter_attributes)
        unit_item = self.get_unit_item(parameter_attributes)
        default_item = self.get_default_value_item(parameter_attributes)
        # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
        parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
        value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
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
        else:
            param_type = param_attributes.get('type', '')
            visual_type = param_attributes.get('visual_type', '')
            if param_type == 'enum' or visual_type == 'ip_format':
                min_limit_item = QStandardItem('')
            else:
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
        else:
            param_type = param_attributes.get('type', '')
            visual_type = param_attributes.get('visual_type', '')
            if param_type == 'enum' or visual_type == 'ip_format':
                max_limit_item = QStandardItem('')
            else:
                max_limit_item = QStandardItem(str(param_attributes.get('max_limit', '')))

            return max_limit_item

    def get_unit_item(self, param_attributes):
        param_type = param_attributes.get('type', '')
        visual_type = param_attributes.get('visual_type', '')
        if param_type == 'enum' or visual_type == 'ip_format':
            unit_item = QStandardItem('')
        else:
            unit_item = QStandardItem(str(param_attributes.get('unit', '')))

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
