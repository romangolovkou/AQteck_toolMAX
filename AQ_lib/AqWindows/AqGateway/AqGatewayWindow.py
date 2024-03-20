from PySide6.QtCore import Signal, QPoint, Qt
from PySide6.QtWidgets import QTableWidget, QFrame, QPushButton, QRadioButton, QStackedWidget, QWidget, QTableWidgetItem

from AqWindowTemplate import AqDialogTemplate


class AqGatewayWindow(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Gateway'
        self.prepare_ui()

    def prepare_ui(self):
        # Устанавливаем ширину столбцов в таблице справа
        cur_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(cur_width * 0.05))
        self.ui.tableWidget.setColumnWidth(1, int(cur_width * 0.15))
        self.ui.tableWidget.setColumnWidth(2, int(cur_width * 0.5))
        self.ui.tableWidget.setColumnWidth(3, int(cur_width * 0.15))
        self.ui.tableWidget.setColumnWidth(4, int(cur_width * 0.15))
        self.ui.tableFrame.hide()

        self.ui.mainWidget.prepare_ui()

        self.ui.mainWidget.uiChanged.connect(self.custom_resize)

    def custom_resize(self):
        self.resize(self.width(), self.ui.mainWidget.sizeHint().height())


class AqGatewayFrame(QFrame):
    uiChanged = Signal()
    close_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_ui_elements = None

        self.saveBtn = None
        self.cancelBtn = None
        self.ethRadioBtn = None
        self.rsRadioBtn = None
        self.stackedWidget = None
        self.tableFrame = None
        self.tableWidget = None
        self.masterRsPage = None
        self.masterEthPage = None

    def prepare_ui(self):
        self.saveBtn = self.findChild(QPushButton, 'saveBtn')
        self.cancelBtn = self.findChild(QPushButton, 'cancelBtn')
        self.ethRadioBtn = self.findChild(QRadioButton, 'ethRadioBtn')
        self.rsRadioBtn = self.findChild(QRadioButton, 'rsRadioBtn')
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.tableWidget = self.findChild(QTableWidget, 'tableWidget')
        self.tableFrame = self.findChild(QFrame, 'tableFrame')
        self.masterRsPage = self.findChild(QWidget, 'masterRsPage')
        self.masterEthPage = self.findChild(QWidget, 'masterEthPage')

        self.main_ui_elements = [
            self.saveBtn,
            self.cancelBtn,
            self.ethRadioBtn,
            self.rsRadioBtn,
            self.stackedWidget,
            self.tableWidget,
            self.masterRsPage,
            self.masterEthPage
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element: ')

        self.ethRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
        self.rsRadioBtn.clicked.connect(self.change_ui_by_selected_mode)

        self.saveBtn.clicked.connect(self.save_btn_clicked)
        self.cancelBtn.clicked.connect(self.close_signal.emit)

    def change_ui_by_selected_mode(self):
        if self.rsRadioBtn.isChecked():
            self.show_rs_master_if()
        else:
            self.show_eth_master_if()

        self.uiChanged.emit()

    def show_rs_master_if(self):
        widget = getattr(self, "masterRsPage")
        self.stackedWidget.setCurrentWidget(widget)
        self.tableFrame.show()


    def show_eth_master_if(self):
        self.tableFrame.hide()
        widget = getattr(self, "masterEthPage")
        self.stackedWidget.setCurrentWidget(widget)

    def save_btn_clicked(self):
        pass


class AqGatewayTableWidget(QTableWidget):
    clickedRow = Signal(int, QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
                                                           QTableWidget::item { padding-left: 3px; }""")
        self.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self, row, col):
        item = self.item(row, col)
        if item:
            item_rect = self.visualItemRect(item)
            pos = self.viewport().mapTo(self.parent(), item_rect.topLeft())
            self.clickedRow.emit(row, pos)

    def append_device_to_table(self, row, status='ok'):
        if status == 'ok':
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#429061"))
        elif status == 'need_pass':
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#807c7c"))
        else:
            for i in range(self.columnCount()):
                self.item(row, i).setBackground(QColor("#9d4d4f"))

        new_height = self.get_sum_of_rows_height() + 30
        self.setFixedHeight(new_height)

    def append_row(self):
        # if new_row_index is None:
        #     new_row_index = self.rowCount()
        #     self.setRowCount(self.rowCount() + 1)
        # Создаем элементы таблицы для каждой строки
        number_item = QTableWidgetItem(str(self.rowCount() + 1))
        number_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        address_item = QTableWidgetItem(device.info('address'))
        address_item.setFlags(address_item.flags() & ~Qt.ItemIsEditable)
        version_item = QTableWidgetItem(device.info('version'))
        version_item.setFlags(version_item.flags() & ~Qt.ItemIsEditable)

        if status == 'need_pass':
            tip_str = 'Enter password. CLick to enter'
            checkbox_item.setToolTip(tip_str)
            name_item.setToolTip(tip_str)
            address_item.setToolTip(tip_str)
            version_item.setToolTip(tip_str)

        # Устанавливаем элементы таблицы
        self.setItem(new_row_index, 0, checkbox_item)
        self.setItem(new_row_index, 1, name_item)
        self.setItem(new_row_index, 2, address_item)
        self.setItem(new_row_index, 3, version_item)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if status == 'ok':
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.setCellWidget(new_row_index, 0, checkbox)
        item = self.item(new_row_index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.append_device_to_table(new_row_index, status)
    #
    # def replace_device_in_row(self, device: AqBaseDevice, row: int):
    #     self.append_device_row(device, row)


    def get_sum_of_rows_height(self):
        sum_height = 0
        for i in range(self.rowCount()):
            sum_height += self.rowHeight(i)

        return sum_height
