from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel


class AQ_TreeItemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device = None

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device


class AQ_TreeViewItemModel(QStandardItemModel):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.device = device
        self.event_manager = event_manager

    def update_parameter(self, manager_item):
        param_attributes = manager_item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = manager_item.rowCount()
            for row in range(row_count):
                child_item = manager_item.child(row)
                self.update_parameter(child_item)
        else:
            manager_item.show_new_value()

    def update_all_params(self):
        root = self.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.update_parameter(child_item)

    def read_parameter(self, index):
        item = self.itemFromIndex(index)
        sourse_item = item.get_sourse_item()
        self.device.read_parameter(sourse_item)
        self.update_parameter(item)
