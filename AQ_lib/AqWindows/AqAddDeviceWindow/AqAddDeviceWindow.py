from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QDialog, QWidget


class AqAddDeviceWidget(QDialog):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())


class AqAddDeviceTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
