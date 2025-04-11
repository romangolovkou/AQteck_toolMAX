from PySide2.QtGui import QStandardItemModel


class AQ_WatchListTableViewItemModel(QStandardItemModel):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Parameter", "Value", "Device"])
        