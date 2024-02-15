from PySide6.QtWidgets import QWidget

from ui_NoDeviceWidget import Ui_NoDeviceWidget


class NoDeviceWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_NoDeviceWidget()
        self.ui.setupUi(self)
