from PySide6.QtGui import QStandardItemModel

import AqUiWorker
from AQ_EventManager import AQ_EventManager
from AqWatchListCore import AqWatchListCore


class AqWatchListTreeViewModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        # self.device = device
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.event_manager.register_event_handler('current_device_data_updated', self.update_params_values, True)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Name", "Value"])

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
        for watchItem in AqWatchListCore.watched_items:
            if watchItem.device == device:
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
                            manager_item.show_new_value()
                            manager_item.update_status()

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
