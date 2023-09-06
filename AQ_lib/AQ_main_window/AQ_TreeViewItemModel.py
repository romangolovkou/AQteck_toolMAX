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
