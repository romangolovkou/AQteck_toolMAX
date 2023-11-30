from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QDialog

from DeviceModels import AqDeviceParamListModel

AqDevice


class AqParamListWidget(QDialog):
    def __init__(self, _ui, dev_info: AqDeviceParamListModel = None, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.tableView.horizontalHeader().sectionResized.connect(self.customAdjustSize)
        self.customAdjustSize()
        connect = ConnectManager.CreateConnect(settings)

    def customAdjustSize(self, *args):
        self.ui.tableView.adjustSize()
        self.adjustSize()


class AqParamListInfoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


class AqParamListTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    """Base item list class
    provide functionality by add data to table, set size, resize, etc"""

    def adjustSize(self):
        content_height = self.horizontalHeader().height()
        content_width = self.verticalHeader().width()
        for i in range(self.rowCount()):
            content_height += self.rowHeight(i)

        for i in range(self.columnCount()):
            content_width += self.columnWidth(i)

        self.setFixedSize(content_width, content_height)

        self.parent().adjustSize()

class AqModbusParamListTableWidget(AqParamListTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    """Here we will parse only items with ModbusItem type
    this class will require some attributes from items"""


class AqOwenParamListTableWidget(AqParamListTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    """Here we will parse only items with OwenItem type
    this class will require some attributes from items"""


class AqTestParamListTableWidget(AqParamListTableWidget):
    def __init__(self, parent=None, rows=None, columns=None, maxItemLen=None):
        super().__init__(parent)
    """This class generate data for test AqParamListTableWidget with different
    count rows and columns"""

    def generateData(self):
        pass








