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
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device

    def update_parameter(self, manager_item):
        param_attributes = manager_item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = manager_item.rowCount()
            for row in range(row_count):
                child_item = manager_item.child(row)
                self.update_parameter(child_item)
        else:
            value = manager_item.get_value()
            manager_item.show_new_value(value)
            # item_index = self.indexFromItem(item)
            # view_value_item_index = item_index.sibling(item_index.row(), 1)
            # view_value_item = self.itemFromIndex(view_value_item_index)
            # if not (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
            #     view_value_item.setData(value, Qt.EditRole)
            # else:
            #     view_value_item.setData(value, Qt.DisplayRole)

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
