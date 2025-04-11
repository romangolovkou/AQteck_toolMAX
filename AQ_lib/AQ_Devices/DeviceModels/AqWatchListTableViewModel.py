from PySide6.QtGui import QStandardItemModel


class AqWatchListTableViewModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Parameter", "Value"])
