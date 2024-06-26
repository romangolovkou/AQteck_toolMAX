from PySide6.QtGui import QStandardItemModel

from AqTranslateManager import AqTranslateManager
# import AqUiWorker
from TreeBranchToListConv import param_convert_tree_to_list


class AqTreeItemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device = None

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device


class AqTreeViewItemModel(QStandardItemModel):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.device = device
        self.event_manager = event_manager
        self.event_manager.register_event_handler('current_device_data_updated', self.update_params_values, True)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([AqTranslateManager.tr("Name"),
                                       AqTranslateManager.tr("Value"),
                                       AqTranslateManager.tr("Lower limit"),
                                       AqTranslateManager.tr("Upper limit"),
                                       AqTranslateManager.tr("Unit"),
                                       AqTranslateManager.tr("Default value")])
        AqTranslateManager.subscribe(self.retranslate)

    def update_parameter_value(self, manager_item):
        manager_item.show_new_value()
        manager_item.update_status()

    def update_params_catalog(self, manager_item):
        row_count = manager_item.rowCount()
        for row in range(row_count):
            child_item = manager_item.child(row)
            param_attributes = child_item.get_param_attributes()
            if param_attributes.get('is_catalog', 0) == 1:
                self.update_params_catalog(child_item)
            else:
                self.update_parameter_value(child_item)

    def update_params_values(self, device, param_stack=None):
        if self.device == device:
            if param_stack is None:
                root = self.invisibleRootItem()
                for row in range(root.rowCount()):
                    child_item = root.child(row)
                    self.update_params_catalog(child_item)
            else:
                for i in range(len(param_stack)):
                    sourse_item = param_stack[i]
                    manager_item = self.travers_find_manager_by_sourse_item(sourse_item)
                    if manager_item is not None:
                        try:
                            manager_item.show_new_value()
                            manager_item.update_status()
                        except Exception as e:
                            print(e)

    def travers_find_manager_by_sourse_item(self, sourse_item):
        manager_item = None
        root = self.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            param_attributes = child_item.get_param_attributes()
            if param_attributes.get('is_catalog', 0) == 1:
                manager_item = self.travers_find_sourse_item_in_items(sourse_item, root)
            else:
                manager_item = self.travers_find_sourse_item_in_items(sourse_item, child_item)

        return manager_item

    def travers_find_sourse_item_in_items(self, sourse_item, item):
        manager_item = None
        for row in range(item.rowCount()):
            child_item = item.child(row)
            param_attributes = child_item.get_param_attributes()
            if param_attributes.get('is_catalog', 0) == 1:
                manager_item = self.travers_find_sourse_item_in_items(sourse_item, child_item)
                if manager_item is not None:
                    break
            else:
                if sourse_item == child_item.get_sourse_item():
                    manager_item = child_item
                    break

        return manager_item

    def update_parameter_status(self, manager_item):
        param_attributes = manager_item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = manager_item.rowCount()
            for row in range(row_count):
                child_item = manager_item.child(row)
                self.update_parameter_status(child_item)
        else:
            manager_item.update_status()

    def update_all_params_statuses(self):
        root = self.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.update_parameter_status(child_item)

    def read_parameter(self, index):
        item = self.itemFromIndex(index)
        sourse_item = item.get_sourse_item()
        self.device.read_parameters(sourse_item, message_feedback_address='main')

    def write_parameter(self, index):
        item = self.itemFromIndex(index)
        sourse_item = item.get_sourse_item()
        self.device.write_parameters(sourse_item, message_feedback_address='main')

    def add_parameter_to_watch_list(self, index):
        item = self.itemFromIndex(index)
        sourse_item = item.get_sourse_item()
        from AqWatchListCore import AqWatchListCore
        from AqUiWorker import show_watch_list_window
        show_watch_list_window()
        #TODO:: rework imports
        param_attributes = sourse_item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            item_list = param_convert_tree_to_list(sourse_item)
            # for sourse_child_item in item_list:
            AqWatchListCore.addItem(self.device, item_list)
        else:
            AqWatchListCore.addItem(self.device, sourse_item)

    def de_init(self):
        self.event_manager.unregister_event_handler('current_device_data_updated', self.update_params_values)
        AqTranslateManager.de_subscribe(self.retranslate)

    def retranslate(self):
        self.setHorizontalHeaderLabels([AqTranslateManager.tr("Name"),
                                        AqTranslateManager.tr("Value"),
                                        AqTranslateManager.tr("Lower limit"),
                                        AqTranslateManager.tr("Upper limit"),
                                        AqTranslateManager.tr("Unit"),
                                        AqTranslateManager.tr("Default value")])
