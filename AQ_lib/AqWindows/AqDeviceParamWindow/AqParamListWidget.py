from PySide6.QtWidgets import QWidget, QFrame, QTableWidget

from DeviceModels import AqDeviceParamListModel


class AqParamListWidget(QWidget):
    def __init__(self, _ui, dev_info: AqDeviceParamListModel = None, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)


class AqParamListInfoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


class AqParamListTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    """Base item list class
    provide functionality by add data to table, set size, resize, etc"""


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








