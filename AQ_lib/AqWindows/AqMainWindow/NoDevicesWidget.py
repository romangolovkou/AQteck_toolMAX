from PySide2.QtWidgets import QWidget

from AqTranslateManager import AqTranslateManager
from ui_NoDeviceWidget import Ui_NoDeviceWidget


class NoDeviceWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_NoDeviceWidget()
        self.ui.setupUi(self)
        AqTranslateManager.subscribe(self.retranslate)

    def retranslate(self):
        self.ui.retranslateUi(self)
