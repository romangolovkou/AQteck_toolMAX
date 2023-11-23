from PySide2.QtGui import QStandardItemModel


class AQ_TableViewItemModel(QStandardItemModel):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.device = device
        self.event_manager = event_manager
