from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QTableWidgetItem

import ModbusTableDataFiller
from AqCustomDialogWindow import QDialog, loadDialogJsonStyle
from DeviceModels import AqDeviceParamListModel


class AqParamListWidget(QDialog):
    def __init__(self, _ui, dev_info: AqDeviceParamListModel = None, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self)
        loadDialogJsonStyle(self, self.ui)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QScreen()
        # Получаем размер экрана и возвращаем высоту
        self.setMaximumHeight(screen.size().height())
        # getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

        # if isinstance(AqDeviceParamListModel.param_list[0], AqModbusItem):
        #     self.ui.tableView = AqModbusParamListTableWidget()
        self.ui.tableView.fillModbusData(dev_info.param_list)

        self.ui.tableView.horizontalHeader().sectionResized.connect(self.customAdjustSize)
        self.customAdjustSize()

    def customAdjustSize(self, *args):
        self.ui.tableView.adjustSize()
        self.adjustSize()


class AqParamListInfoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


class AqParamListTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def fillModbusData(self, param_list: list):
        self.clear()
        ModbusTableDataFiller.fill_table_with_modbus_items(self, param_list)



    """Base item list class
    provide functionality by add data to table, set size, resize, etc"""

    def adjustSize(self):
        content_height = self.horizontalHeader().height()
        content_width = self.verticalHeader().width()
        for i in range(self.rowCount()):
            content_height += self.rowHeight(i)

        for i in range(self.columnCount()):
            content_width += self.columnWidth(i)

        if content_height > self.parent().maximumHeight():
            content_height = self.parent().maximumHeight()

        self.setFixedSize(content_width, content_height)

        self.parent().adjustSize()









