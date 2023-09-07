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

    def update_parameter(self, item):
        param_attibutes = item.get_param_attributes()
        if param_attibutes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.update_parameter(child_item)
        else:
            value = item.get_value()
            item_index = self.indexFromItem(item)
            view_value_item_index = item_index.sibling(item_index.row(), 1)
            view_value_item = self.itemFromIndex(view_value_item_index)
            view_value_item.setData(value, Qt.DisplayRole)

    def update_all_params(self):
        root = self.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.update_parameter(child_item)
